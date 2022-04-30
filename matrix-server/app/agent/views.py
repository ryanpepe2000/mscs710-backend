import json
import logging
from flask import request
from . import agent
from ..models import *

logger = logging.getLogger(__name__.split(".", 1)[1])


@agent.route('/api/send_data', methods=['POST'])
def post_data():
    data = json.loads(request.get_json())
    credentials = data['credentials']
    print(data)

    if credentials['email'] is not None and credentials['password'] is not None and credentials['device_id'] is not None:
        user = User.query.filter_by(email=credentials['email']).first()
        device = Device.query.filter_by(device_id=credentials['device_id'], user_id=user.id).first()
        if user and user.validate_password(attempted_password=credentials['password']) and device:
            # CPU Report
            cpu_data = data['cpu']
            cpu_report = CPUReport(speed_curr=cpu_data['current'],
                                   speed_min=cpu_data['min'],
                                   speed_max=cpu_data['max'],
                                   device_id=device.device_id)
            db.session.add(cpu_report)
            db.session.commit()

            # Memory Report
            memory_data = data['memory']
            memory_report = MemoryReport(memory_used=memory_data['used'],
                                         memory_total=memory_data['total'],
                                         device_id=device.device_id)
            db.session.add(memory_report)
            db.session.commit()

            # Disk Report
            disk_data = data['disk']
            disk_report = DiskReport(disk_size=disk_data['total'],
                                     disk_used=disk_data['used'],
                                     disk_free=disk_data['free'],
                                     device_id=device.device_id)
            db.session.add(disk_report)
            db.session.commit()

            # Process Reports
            processes = data['processes']
            for proc_id, process_data in processes.items():
                process_report = ProcessReport(pid=proc_id,
                                               process_name=process_data['name'],
                                               cpu_usage=process_data['cpu'],
                                               mem_usage=process_data['memory'],
                                               disk_usage=process_data['disk'],
                                               thread_count=process_data['threads'],
                                               device_id=device.device_id)
                db.session.add(process_report)
            db.session.commit()
            return "Worked", 200
        else:
            logger.debug("Incorrect credentials/device ID have been provided.")
            return 'Incorrect credentials', 400
    else:
        logger.debug("Credentials have not been provided.")
        return 'Missing credentials', 400
