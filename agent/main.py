import json
import requests

import psutil

# Constants
file_path = 'credentials.txt'

data = {}


def main():
    collect_metrics()


def collect_metrics():
    # Store relevant data in json object
    data['cpu'] = (psutil.cpu_freq()._asdict())
    data['memory'] = (psutil.virtual_memory()._asdict())
    data['disk'] = (psutil.disk_usage('/')._asdict())
    # for process in psutil.process_iter():
    #     process.cpu_percent(interval=0.1)
    #     pid = process.pid
    #     print(pid, process.name(), process.cpu_percent(interval=0.1))

    r = requests.post('http://10.6.10.81:5000/api/send_data', json=json.dumps(data))
    print(f"Status Code: {r.status_code}, Response: {r.json()}")


def validate_credentials():
    try:
        with open(file_path) as f:
            for line in f:
                print(line, end='')

    except FileNotFoundError:
        print("Error: File was not found.")
        print("Read documentation to learn how to download credentials.txt")


if __name__ == '__main__':
    main()
