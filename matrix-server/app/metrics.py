"""
Defines the metrics object that will be created and passed to the dashboard.

@date 4.6.22
@author Ryan Pepe
"""
from typing import List

from sqlalchemy import desc, func
from . import util

from .models import *


class Metrics:

    def __init__(self, device):
        try:
            self.device = device
            self.new_cpu_report: CPUReport = self.get_cpu_report()
            self.new_mem_report: MemoryReport = self.get_mem_report()
            self.new_disk_report: DiskReport = self.get_disk_report()
            self.all_cpu_reports: List[CPUReport] = self.get_all_cpu_reports()
            self.all_mem_reports: List[MemoryReport] = self.get_all_mem_reports()
            self.all_disk_reports: List[DiskReport] = self.get_all_disk_reports()
            self.proc_report: List[ProcessReport] = self.get_process_report()
        except MetricException:
            logger.info("An error occurred while querying metrics.")
            self.new_cpu_report, self.new_mem_report, self.new_disk_report, self.all_cpu_reports, self.all_mem_reports, \
            self.all_disk_reports = None, None, None, None, None, None

    def is_valid(self):
        return self.device is not None and self.new_cpu_report is not None and self.new_mem_report is not None \
               and self.new_disk_report is not None and self.proc_report is not None

    def get_cpu_display_titles(self):
        return ["User Consumption", "System Consumption", "Active Threads", "Process Count"]

    def get_cpu_display_vals(self):
        user_consumption = f'{str(round(self.new_cpu_report.user, 1))}%'
        sys_consumption = f'{str(round(self.new_cpu_report.system, 1))}%'
        num_threads = sum(proc.thread_count for proc in self.proc_report)
        proc_count = len(self.proc_report)
        return [user_consumption, sys_consumption, num_threads, proc_count]

    def get_mem_display_titles(self):
        return ["Percent Used", "Amount Used", "Amount Available"]

    def get_mem_display_vals(self):
        percent_usage = f'{str(round(self.new_mem_report.memory_used / self.new_mem_report.memory_total * 100, 1))}%'
        mem_used = f'{round(self.new_mem_report.memory_used / 1024 / 1024 / 1024, 1)} GB'
        mem_total = f'{round(self.new_mem_report.memory_total / 1024 / 1024 / 1024, 1)} GB'
        return [percent_usage, mem_used, mem_total]

    def get_disk_display_titles(self):
        return ["Disk Read", "Disk Write", "GB Used", "Disk Size"]

    def get_disk_display_vals(self):
        disk_read = f'{util.bytes_to_amt_per_sec(self.new_disk_report.read_bytes_per_sec)}'
        disk_write = f'{util.bytes_to_amt_per_sec(self.new_disk_report.write_bytes_per_sec)}'
        disk_used = f'{round(self.new_disk_report.disk_used / 1024 / 1024 / 1024)} GB'
        disk_total = f'{round(self.new_disk_report.disk_size / 1024 / 1024 / 1024)} GB'
        return [disk_read, disk_write, disk_used, disk_total]

    def get_cpu_report(self):
        cpu_report: CPUReport = CPUReport.query.filter_by(device_id=self.device.device_id).order_by(
            desc(CPUReport.cpu_id)).first()
        if cpu_report is None:
            raise MetricException
        else:
            return cpu_report

    def get_all_cpu_reports(self):
        cpu_reports: List[CPUReport] = CPUReport.query.filter_by(device_id=self.device.device_id).order_by(
            desc(CPUReport.cpu_id)).all()
        if cpu_reports is None:
            raise MetricException
        else:
            return cpu_reports

    def get_mem_report(self):
        memory_report: MemoryReport = MemoryReport.query.filter_by(device_id=self.device.device_id).order_by(
            desc(MemoryReport.memory_id)).first()
        if memory_report is None:
            raise MetricException
        else:
            return memory_report

    def get_all_mem_reports(self):
        mem_reports: List[MemoryReport] = MemoryReport.query.filter_by(device_id=self.device.device_id).order_by(
            desc(MemoryReport.memory_id)).all()
        if mem_reports is None:
            raise MetricException
        else:
            return mem_reports

    def get_disk_report(self):
        disk_report: DiskReport = DiskReport.query.filter_by(device_id=self.device.device_id).order_by(
            desc(DiskReport.disk_id)).first()
        if disk_report is None:
            raise MetricException
        else:
            return disk_report

    def get_all_disk_reports(self):
        disk_reports: List[DiskReport] = DiskReport.query.filter_by(device_id=self.device.device_id).order_by(
            desc(DiskReport.disk_id)).all()
        if disk_reports is None:
            raise MetricException
        else:
            return disk_reports

    def get_process_report(self):
        # Get the max ID of the available proc reports for that device
        last_process_report: ProcessReport = ProcessReport.query.filter_by(device_id=self.device.device_id).order_by(
            desc(ProcessReport.proc_id)).first()
        if last_process_report is None:
            raise MetricException
        else:
            proc_report: List[ProcessReport] = ProcessReport.query.filter_by(
                device_id=self.device.device_id, proc_id=last_process_report.proc_id).order_by(
                ProcessReport.cpu_usage, ProcessReport.mem_usage, ProcessReport.disk_usage).all()

        if proc_report is None:
            raise MetricException
        else:
            return proc_report

    def get_cpu_chart_data(self):

        data = []
        for cpu_report in self.all_cpu_reports:
            time = str(cpu_report.sys_time)[:16]
            percent = round(cpu_report.speed_curr / cpu_report.speed_max * 100, 1)
            data.append((time, percent))

        return data

    def get_mem_chart_data(self):
        data = []
        for mem_report in self.all_mem_reports:
            time = str(mem_report.sys_time)[:16]
            percent = round(mem_report.memory_used / mem_report.memory_total * 100, 1)
            data.append((time, percent))

        return data

    def get_disk_chart_data(self):
        data = []
        for disk_report in self.all_disk_reports:
            time = str(disk_report.sys_time)[:16]
            amt_per_sec = util.bytes_to_amt_per_sec(disk_report.read_bytes_per_sec + disk_report.write_bytes_per_sec)
            data.append((time, amt_per_sec))

        return data


class ChartMetrics:
    def __init__(self, metrics: Metrics):
        self.cpu_data = metrics.get_cpu_chart_data()
        self.mem_data = metrics.get_mem_chart_data()
        self.disk_data = metrics.get_disk_chart_data()

    def get_cpu_labels(self):
        return [row[0] for row in self.cpu_data]

    def get_cpu_values(self):
        return [row[1] for row in self.cpu_data]

    def get_mem_labels(self):
        return [row[0] for row in self.mem_data]

    def get_mem_values(self):
        return [row[1] for row in self.mem_data]

    def get_disk_labels(self):
        return [row[0] for row in self.disk_data]

    def get_disk_values(self):
        return [row[1] for row in self.disk_data]


class MetricException(Exception):
    def __init__(self):
        pass
