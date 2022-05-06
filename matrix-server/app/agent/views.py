import json
import logging
from flask import request, send_file
from sqlalchemy import desc
from . import agent
from .. import db
from ..models import *

logger = logging.getLogger(__name__.split(".", 1)[1])


@agent.route('/api/send_data', methods=['POST'])
def post_data():
    data = json.loads(request.get_json())
    credentials = data['credentials']

    if credentials['email'] is not None and credentials['password'] is not None and credentials['device_name'] is not None:
        user = User.query.filter_by(email=credentials['email']).first()

        if user is None:
            return "Account Credentials could not be verified", 400

        device = Device.query.filter_by(device_name=credentials['device_name'], user_id=user.id).first()

        if device is None:
            return "Device name could not be verified", 400

        if user and user.validate_password(attempted_password=credentials['password']) and device:
            # Insert New CPU Report to Database
            cpu_data = data['cpu']
            cpu_report = CPUReport(speed_curr=cpu_data['current'],
                                   speed_min=cpu_data['min'],
                                   speed_max=cpu_data['max'],
                                   device_time=cpu_data['time'],
                                   system=cpu_data['system'],
                                   user=cpu_data['user'],
                                   device_id=device.device_id)
            db.session.add(cpu_report)
            db.session.commit()

            # Insert New Memory Report to Database
            memory_data = data['memory']
            memory_report = MemoryReport(memory_used=memory_data['used'],
                                         memory_total=memory_data['total'],
                                         device_time=memory_data['time'],
                                         device_id=device.device_id)
            db.session.add(memory_report)
            db.session.commit()

            # Insert New Disk Report to Database
            disk_data = data['disk']
            disk_report = DiskReport(disk_size=disk_data['total'],
                                     disk_used=disk_data['used'],
                                     read_bytes=disk_data['read_bytes'],
                                     write_bytes=disk_data['write_bytes'],
                                     read_bytes_per_sec=disk_data['read_time'],
                                     write_bytes_per_sec=disk_data['write_time'],
                                     device_time=disk_data['time'],
                                     device_id=device.device_id)
            db.session.add(disk_report)
            db.session.commit()

            # Get the max ID of the available proc reports for that device
            last_process_report = ProcessReport.query.filter_by(device_id=device.device_id).order_by(desc(ProcessReport.proc_id)).first()
            if last_process_report is None:
                next_proc_id = 0
            else:
                next_proc_id = last_process_report.proc_id + 1

            # Process Reports
            processes = data['processes']
            for proc_id, process_data in processes.items():
                process_report = ProcessReport(proc_id=next_proc_id,
                                               pid=proc_id,
                                               process_name=process_data['name'],
                                               cpu_usage=process_data['cpu'],
                                               mem_usage=process_data['memory'],
                                               disk_usage=process_data['disk'],
                                               disk_read_bytes_per_sec=process_data['disk_read_per_sec'],
                                               disk_write_bytes_per_sec=process_data['disk_write_per_sec'],
                                               thread_count=process_data['threads'],
                                               device_time=process_data['time'],
                                               device_id=device.device_id)
                db.session.add(process_report)
            db.session.commit()
            return "Metrics Recorded Successfully", 200
        else:
            logger.debug("Incorrect credentials/device ID have been provided.")
            return 'Invalid Account Credentials', 400
    else:
        logger.debug("Credentials have not been provided.")
        return 'Missing credentials', 400


@agent.route("/api/download-agent")
def download_agent(path='static/agent/agent.zip'):
    try:
        return send_file(path, as_attachment=True)
    except Exception as e:
        logger.debug(e)
        return 'An error has occurred while downloading your file', 400
