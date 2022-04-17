import json
import requests

import psutil

# Constants
file_path = 'credentials.txt'


def main():
    data = collect_metrics()
    data['credentials'] = get_credentials()
    send_metrics(data)


def send_metrics(data):
    r = requests.post('http://127.0.0.1:5000/api/send_data', json=json.dumps(data))
    print(f"Status Code: {r.status_code}, Response: {r.text}")


def collect_metrics():
    data = {'cpu': (psutil.cpu_freq()._asdict()), 'memory': (psutil.virtual_memory()._asdict()),
            'disk': (psutil.disk_usage('/')._asdict())}
    # Store relevant data in json object

    process_data = {}
    for process in psutil.process_iter():
        if process.is_running():
            pid = process.pid
            name = process.name()
            cpu = process.cpu_percent(interval=0.1)
            mem = process.memory_percent()
            disk = disk_usage(process)
            threads = process.num_threads()
            process_data[pid] = {'name': name, 'cpu': cpu, 'memory': mem, 'disk': disk, 'threads': threads}
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
        print("Error: File was not found.")
        print("Read documentation to learn how to download credentials.txt")
        return {}


if __name__ == '__main__':
    main()
