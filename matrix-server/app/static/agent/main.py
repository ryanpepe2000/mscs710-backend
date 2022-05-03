#!/usr/bin/python3
import json
import requests
import time
from datetime import datetime

import psutil

# Constants
file_path = r'credentials.txt'
base_url = "http://127.0.0.1:5000/"
api_route = "api/send_data"

DEBUG = False


def main():
    data = collect_metrics()
    data['credentials'] = get_credentials()
    send_metrics(data)


def collect_metrics():
    # Store relevant data in json object
    data = {}
    # CPU Data
    data['cpu'] = psutil.cpu_freq()._asdict()
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

    processes = []
    process_data = {}

    for process in psutil.process_iter():
        if process.is_running():
            process.cpu_percent()
            processes.append(process)
    time.sleep(1)
    for process in processes:
        try:
            pid = process.pid
            name = process.name()
            cpu = process.cpu_percent()
            mem = process.memory_percent()
            disk = disk_usage(process)
            threads = process.num_threads()
            process_data[pid] = {'name': name, 'cpu': cpu, 'memory': mem, 'disk': disk, 'threads': threads, 'time': str(datetime.utcnow())}
        except psutil.NoSuchProcess:
            continue
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
