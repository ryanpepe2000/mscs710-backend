"""
ORM Configuration for the Tables used in the Matrix DB Schema. Organizes intermediate tables
into separate classes with explicitly defined back-population variables.

@date 3.23.21
@author Ryan Pepe
"""
import logging
from datetime import datetime
from . import db

logger = logging.getLogger(__name__)

# Describing the Role Table
class Role(db.Model):
    # Overriding the default name "Role" with role
    __tablename__ = 'role'

    # Describing the columns
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.NVARCHAR(length=50), nullable=False)
    role_desc = db.Column(db.NVARCHAR(length=50), nullable=False)

    # Back Reference to User Model
    users = db.relationship('UserRole', back_populates='role', lazy='dynamic')

    # How it should look if we call print
    def __repr__(self):
        return f"Role(id={self.role_id!r}, role_name={self.role_id!r}, role_desc={self.role_desc!r})"


class UserRole(db.Model):
    # Overriding the default name UserRole with user_role
    __tablename__ = 'user_role'

    # Describe the columns
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)

    # Foreign Key References
    user = db.relationship('User', back_populates='users')
    role = db.relationship('Role', back_populates='roles')


# Describing the User Table
class User(db.Model):
    # Overriding the default name "User" with user
    __tablename__ = 'user'

    # Describing the columns
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.NVARCHAR(length=50), nullable=False)
    last_name = db.Column(db.NVARCHAR(length=50), nullable=False)
    m_initial = db.Column(db.NVARCHAR(length=50), nullable=True)
    email = db.Column(db.NVARCHAR(length=50), nullable=False)
    password = db.Column(db.NVARCHAR(length=50), nullable=False)
    phone_num = db.Column(db.NVARCHAR(length=50), nullable=False)

    # Back Reference to Role Model
    roles = db.relationship('UserRole', back_populates='role', lazy='dynamic')
    devices = db.relationship('DeviceAssignment', back_populates='device', lazy='dynamic')


class DeviceAssignment(db.Model):
    # Overriding the default name DeviceAssignment with device_assignment
    __tablename__ = 'device_assignment'

    # Describe the columns
    device_id = db.Column(db.Integer, db.ForeignKey('device.device_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    registration_date = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    is_registered = db.Column(db.Boolean, nullable=False, default=False)
    is_active = db.Column(db.Boolean, nullable=False, default=False)

    # Foreign Key References
    user = db.relationship('User', back_populates='users')
    device = db.relationship('Device', back_populates='devices')


class Device(db.Model):
    # Overriding the default name "Device" with device
    __tablename__ = 'device'

    # Describing the columns
    device_id = db.Column(db.Integer, primary_key=True)
    mac_address = db.Column(db.NVARCHAR(length=50), nullable=True)
    os_version = db.Column(db.NVARCHAR(length=50), nullable=True)
    machine_name = db.Column(db.NVARCHAR(length=50), nullable=False)

    # Back Reference to Role Model
    users = db.relationship('DeviceAssignment', back_populates='device', lazy='dynamic')

    # Foreign Key Values
    cpu_reports = db.relationship('CPUReport', back_populates='device')
    disk_reports = db.relationship('MemoryReport', back_populates='device')
    memory_reports = db.relationship('DiskReport', back_populates='device')
    process_reports = db.relationship('ProcessReport', back_populates='device')


class CPUReport(db.Model):
    # Overriding the default name "Device" with device
    __tablename__ = 'cpu_report'

    # Column definition
    cpu_id = db.Column(db.Integer, primary_key=True)
    sys_time = db.Column(db.Integer, primary_key=True, default=datetime.utcnow())
    device_time = db.Column(db.Integer, primary_key=True, default=datetime.utcnow())
    speed_curr = db.Column(db.Float, nullable=False)
    speed_min = db.Column(db.Float, nullable=False)
    speed_max = db.Column(db.Float, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.device_id'))

    # Foreign Key Reference
    device = db.relationship('Device', back_populates='cpu_reports')


class MemoryReport(db.Model):
    # Overriding the default name "MemoryReport" with memory_report
    __tablename__ = 'memory_report'

    # Column definition
    memory_id = db.Column(db.Integer, primary_key=True)
    sys_time = db.Column(db.Integer, primary_key=True, default=datetime.utcnow())
    device_time = db.Column(db.Integer, primary_key=True, default=datetime.utcnow())
    memory_used = db.Column(db.Float, nullable=False)
    memory_total = db.Column(db.Float, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.device_id'))

    # Foreign Key Reference
    device = db.relationship('Device', back_populates='memory_reports')


class DiskReport(db.Model):
    # Overriding the default name "Device" with device
    __tablename__ = 'disk_report'

    # Column definition
    cpu_id = db.Column(db.Integer, primary_key=True)
    sys_time = db.Column(db.Integer, primary_key=True, default=datetime.utcnow())
    device_time = db.Column(db.Integer, primary_key=True, default=datetime.utcnow())
    disk_size = db.Column(db.Float, nullable=False)
    disk_used = db.Column(db.Float, nullable=False)
    disk_free = db.Column(db.Float, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.device_id'))

    # Foreign Key Reference
    device = db.relationship('Device', back_populates='disk_reports')


class ProcessReport(db.Model):
    # Overriding the default name "Device" with device
    __tablename__ = 'process_report'

    # Column definition
    cpu_id = db.Column(db.Integer, primary_key=True)
    sys_time = db.Column(db.Integer, primary_key=True, default=datetime.utcnow())
    device_time = db.Column(db.Integer, primary_key=True, default=datetime.utcnow())
    cpu_usage = db.Column(db.Float, nullable=False)
    mem_usage = db.Column(db.Float, nullable=False)
    disk_usage = db.Column(db.Float, nullable=False)
    thread_count = db.Column(db.Integer, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.device_id'))

    # Foreign Key Reference
    device = db.relationship('Device', back_populates='process_reports')
