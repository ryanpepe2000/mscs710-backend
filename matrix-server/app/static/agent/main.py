#!/usr/bin/python3
import json
import requests
import time
import platform
import uuid

from datetime import datetime

import psutil

# Constants
file_path = r'credentials.txt'
api_route = "api/send_data"

DEBUG = False


def main():
    data = collect_metrics()
    data['credentials'] = get_credentials()
    if data['credentials'].get('url', None) is not None:
        base_url = data['credentials'].get('url')
        if not base_url.endswith("/"):
            base_url += "/"
        data['credentials'].pop('url')
    else:
        base_url = "http://matrixsystems.info/"
    send_metrics(data, base_url)


def collect_metrics():
    # Store relevant data in json object
    data = {}
    # General system info
    data['system'] = {
        "os_version": platform.system() + " " + platform.version(),
        "mac_address": (
            ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])),
        "is_active": True
    }
    # CPU Data
    data['cpu'] = psutil.cpu_freq()._asdict()
    data['cpu'].update(psutil.cpu_times_percent(interval=1)._asdict())
    data['cpu']['time'] = str(datetime.utcnow())
    # Memory Data
    data['memory'] = psutil.virtual_memory()._asdict()
    data['memory']['time'] = str(datetime.utcnow())
    # Disk Data
    data['disk'] = psutil.disk_io_counters()._asdict()
    data['disk'].update(psutil.disk_usage('/')._asdict())
    data['disk']['time'] = str(datetime.utcnow())

    if DEBUG:
        print("cpu:", data['cpu'])
        print("memory:", data['memory'])
        print("disk:", data['disk'])

    process_data = {}
    processes = [p for p in psutil.process_iter()]

    for process in processes[:]:
        try:
            process.cpu_percent()
            process._io_before = process.io_counters()
        except psutil.Error:
            processes.remove(process)
            continue
        except AttributeError:
            continue
    disk_io_before = psutil.disk_io_counters()

    # Sleep for one second so we can get io per sec
    time.sleep(1)

    disk_total_read, disk_total_write = 0, 0
    # Go through processes and get updated info
    for process in processes[:]:
        with process.oneshot():
            try:
                pid = process.pid
                name = process.name()
                cpu = process.cpu_percent()
                mem = process.memory_percent()
                disk = None
                threads = process.num_threads()
                process_data[pid] = {
                    'name': name, 'cpu': cpu, 'memory': mem, 'disk': disk,
                    'threads': threads, 'time': str(datetime.utcnow())
                }
                try:
                    disk = disk_usage(process)
                    process._io_after = process.io_counters()
                    read_per_sec = (process._io_after.read_bytes - process._io_before.read_bytes)
                    write_per_sec = (process._io_after.write_bytes - process._io_before.write_bytes)
                    disk_total_read += read_per_sec
                    disk_total_write += write_per_sec
                    process_data[pid].update({'disk_read_per_sec': read_per_sec, 'disk_write_per_sec': write_per_sec, 'disk': disk})
                except AttributeError:
                    continue
            except (psutil.NoSuchProcess, psutil.ZombieProcess):
                continue

    # Disk operations after interval
    disk_io_after = psutil.disk_io_counters()
    if disk_total_read > 0 or disk_total_write > 0:
        disks_read_per_sec = disk_total_read
        disks_write_per_sec = disk_total_write
    else:
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


def send_metrics(data, url):
    try:
        requests.get(url)
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to web-server.")
    else:
        r = requests.post(url + api_route, json=json.dumps(data))
        print(f"Status Code: {r.status_code}, Response: {r.text}")


if __name__ == '__main__':
    main()
