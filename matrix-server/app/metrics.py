"""
Defines the metrics object that will be created and passed to the dashboard.

@date 4.6.22
@author Ryan Pepe
"""
from sqlalchemy import desc, func

from .models import *


class Metrics:

    def __init__(self, device):
        try:
            self.device = device
            self.new_cpu_report = self.get_cpu_report()
            self.new_mem_report = self.get_mem_report()
            self.new_disk_report = self.get_disk_report()
            self.all_cpu_reports = self.get_all_cpu_reports()
            self.all_mem_reports = self.get_all_mem_reports()
            self.all_disk_reports = self.get_all_disk_reports()
            self.proc_report = self.get_process_report()
        except MetricException:
            logger.info("An error occurred while querying metrics.")
            self.new_cpu_report, self.new_mem_report, self.new_disk_report, self.all_cpu_reports, self.all_mem_reports, \
            self.all_disk_reports = None, None, None, None, None, None

    def is_valid(self):
        return self.device is not None and self.new_cpu_report is not None and self.new_mem_report is not None \
               and self.new_disk_report is not None and self.proc_report is not None

    def get_cpu_report(self):
        cpu_report = CPUReport.query.filter_by(device_id=self.device.device_id).order_by(
            desc(CPUReport.cpu_id)).first()
        if cpu_report is None:
            raise MetricException
        else:
            return cpu_report

    def get_all_cpu_reports(self):
        cpu_reports = CPUReport.query.filter_by(device_id=self.device.device_id).order_by(
            desc(CPUReport.cpu_id)).all()
        if cpu_reports is None:
            raise MetricException
        else:
            return cpu_reports

    def get_mem_report(self):
        memory_report = MemoryReport.query.filter_by(device_id=self.device.device_id).order_by(
            desc(MemoryReport.memory_id)).first()
        if memory_report is None:
            raise MetricException
        else:
            return memory_report

    def get_all_mem_reports(self):
        mem_reports = MemoryReport.query.filter_by(device_id=self.device.device_id).order_by(
            desc(MemoryReport.memory_id)).all()
        if mem_reports is None:
            raise MetricException
        else:
            return mem_reports

    def get_disk_report(self):
        disk_report = DiskReport.query.filter_by(device_id=self.device.device_id).order_by(
            desc(DiskReport.disk_id)).first()
        if disk_report is None:
            raise MetricException
        else:
            return disk_report

    def get_all_disk_reports(self):
        disk_reports = DiskReport.query.filter_by(device_id=self.device.device_id).order_by(
            desc(DiskReport.disk_id)).all()
        if disk_reports is None:
            raise MetricException
        else:
            return disk_reports

    def get_process_report(self):
        # Get the max ID of the available proc reports for that device
        last_process_report = ProcessReport.query.filter_by(device_id=self.device.device_id).order_by(
            desc(ProcessReport.proc_id)).first()
        if last_process_report is None:
            raise MetricException
        else:
            proc_report = ProcessReport.query.filter_by(
                device_id=self.device.device_id, proc_id=last_process_report.proc_id).all()

        if proc_report is None:
            raise MetricException
        else:
            return proc_report


class MetricException(Exception):
    def __init__(self):
        pass
