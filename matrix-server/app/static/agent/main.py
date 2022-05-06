#!/usr/bin/python3
import json
import requests
import time
import platform
from datetime import datetime

import psutil

# Constants
file_path = r'credentials.txt'
base_url = "http://127.0.0.1:5000/"
api_route = "api/send_data"


def main():
    data = collect_metrics()
    data['credentials'] = get_credentials()
    send_metrics(data)


def collect_metrics():
    # Store relevant data in JSON Object
    data = {}

    # Collect Device Information
    data['os'] = platform.system()

    # Collect CPU Data
    data['cpu'] = psutil.cpu_freq()._asdict()
    data['cpu'].update(psutil.cpu_times_percent(interval=1)._asdict())
    data['cpu']['time'] = str(datetime.utcnow())

    # Collect Memory Data
    data['memory'] = psutil.virtual_memory()._asdict()
    data['memory']['time'] = str(datetime.utcnow())

    # Collect Disk Data
    data['disk'] = psutil.disk_io_counters()._asdict()
    data['disk'].update(psutil.disk_usage('/')._asdict())
    data['disk']['time'] = str(datetime.utcnow())

    # Collect Process Data
    processes = [p for p in psutil.process_iter()]
    process_data = {}

    # Determine Collection Method based on Availability (OS)
    available = True if platform.system() == 'Windows' else False
    print(f"Base OS Determined: {available}")

    for process in processes[:]:
        try:
            process.cpu_percent()

            if available:
                # Windows
                process._io_before = process.io_counters()
            else:
                # Linux or MacOS
                process._io_before = 0

        except psutil.Error:
            processes.remove(process)
            continue
    disk_io_before = psutil.disk_io_counters()

    # Sleep for one second so we can get io per sec
    time.sleep(1)

    # Go through processes and get updated info
    for process in processes[:]:
        with process.oneshot():
            try:
                pid = process.pid
                name = process.name()
                cpu = process.cpu_percent()
                mem = process.memory_percent()
                threads = process.num_threads()

                if available:
                    # Collect per Process Disk IO (Windows)
                    disk = disk_usage(process)
                    process.io_after = process.io_counters()
                    read_per_sec = process.io_after.read_bytes - process._io_before.read_bytes
                    write_per_sec = process.io_after.write_bytes - process._io_before.write_bytes
                else:
                    # Collection Method not Available - Default (Linux or MacOS)
                    disk = 0
                    process.io_after = 0
                    read_per_sec = 0
                    write_per_sec = 0

                process_data[pid] = {
                    'name': name, 'cpu': cpu, 'memory': mem, 'disk': disk,
                    'threads': threads, 'time': str(datetime.utcnow()),
                    'disk_read_per_sec': read_per_sec, 'disk_write_per_sec': write_per_sec
                }
            except (psutil.NoSuchProcess, psutil.ZombieProcess):
                continue

    # Disk operations after interval
    disk_io_after = psutil.disk_io_counters()
    disks_read_per_sec = disk_io_after.read_bytes - disk_io_before.read_bytes
    disks_write_per_sec = disk_io_after.write_bytes - disk_io_before.write_bytes
    data['disk']['read_per_sec'] = disks_read_per_sec
    data['disk']['write_per_sec'] = disks_write_per_sec


    # Update processes dict
    data['processes'] = process_data

    return data


def disk_usage(process):
    io_counters = process.io_counters()
    disk_usage_process = io_counters[2] + io_counters[3]  # read_bytes + write_bytes
    disk_io_counter = psutil.disk_io_counters()
    disk_total = disk_io_counter[2] + disk_io_counter[3]  # read_bytes + write_bytes
    return disk_usage_process / disk_total * 100


def get_credentials():
    try:
        credentials = {}
        with open(file_path) as f:
            line = [x.strip().split('=', 1) for x in f]
            for key, val in line:
                credentials[key] = val
            return credentials

    except FileNotFoundError:
        print("Error: File was not found. Attempting to create...")
        try:
            # create file
            with open(file_path, 'x') as f:
                f.write("device_name=\nemail=\npassword=")
                print("Please enter credentials and try again.")
        except:
            print("Something went wrong. Please download credentials.txt")
            return {}
        return {}


def send_metrics(data):
    try:
        requests.get(base_url)
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to web-server.")
    else:
        r = requests.post(base_url + api_route, json=json.dumps(data))
        print(f"Status Code: {r.status_code}, Response: {r.text}")


if __name__ == '__main__':
    main()
