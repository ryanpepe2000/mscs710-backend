"""
ORM Configuration for the Tables used in the Matrix DB Schema. Organizes intermediate tables
into separate classes with explicitly defined back-population variables.

@date 3.23.22
@author Ryan Pepe
"""
import logging
from datetime import datetime
from . import db, bcrypt, login_manager
from flask_login import UserMixin

logger = logging.getLogger(__name__)

"""
Login Manager
"""


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


"""
Matrix Systems Schema Definitions
"""


class Role(db.Model):
    # Overriding the default name "Role" with role
    __tablename__ = 'role'

    # Describing the columns
    role_id = db.Column(db.Integer(), primary_key=True)
    role_name = db.Column(db.String(length=50), nullable=False)
    role_desc = db.Column(db.String(length=50), nullable=False)

    # Back Reference to User Model
    users = db.relationship('UserRole', backref='role', lazy='dynamic')

    # How it should look if we call print
    def __repr__(self):
        return f"Role(id={self.role_id!r}, role_name={self.role_id!r}, role_desc={self.role_desc!r})"


class UserRole(db.Model):
    # Overriding the default name UserRole with user_role
    __tablename__ = 'user_role'

    # Describe the columns
    role_id = db.Column(db.Integer(), db.ForeignKey('role.role_id'), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), primary_key=True)


# Describing the User Table
class User(db.Model, UserMixin):
    # Overriding the default name "User" with user
    __tablename__ = 'user'

    # Describing the columns
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(length=50), nullable=False)
    last_name = db.Column(db.String(length=50), nullable=False)
    email = db.Column(db.String(length=50), nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)

    # Back Reference to Role Model
    roles = db.relationship('UserRole', backref='user', lazy='dynamic')
    # devices = db.relationship('DeviceAssignment', backref='device', lazy='dynamic')

    # User Authentication Properties
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def validate_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


# class DeviceAssignment(db.Model):
#     # Overriding the default name DeviceAssignment with device_assignment
#     __tablename__ = 'device_assignment'
#
#     # Describe the columns
#     device_id = db.Column(db.Integer, db.ForeignKey('device.device_id'), primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
#     registration_date = db.Column(db.DateTime, index=True, default=datetime.utcnow())
#     is_registered = db.Column(db.Boolean, nullable=False, default=False)
#     is_active = db.Column(db.Boolean, nullable=False, default=False)

    # Foreign Key References
    # user = db.relationship('User', backref='user')
    # device = db.relationship('Device', backref='device')


class Device(db.Model):
    # Overriding the default name "Device" with device
    __tablename__ = 'device'

    # Describing the columns
    device_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    machine_name = db.Column(db.String(length=25), nullable=False)
    mac_address = db.Column(db.String(length=17), nullable=True)
    os_version = db.Column(db.String(length=7), nullable=True)
    registration_date = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    is_active = db.Column(db.Boolean, nullable=False, default=False)

    # Back Reference to User Model
    # users = db.relationship('DeviceAssignment', backref='user', lazy='dynamic')


class CPUReport(db.Model):
    # Overriding the default name "Device" with device
    __tablename__ = 'cpu_report'

    # Column definition
    cpu_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sys_time = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow())
    device_time = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow())
    speed_curr = db.Column(db.Float, nullable=False)
    speed_min = db.Column(db.Float, nullable=False)
    speed_max = db.Column(db.Float, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.device_id'), nullable=False)

    # Foreign Key Reference
    device = db.relationship('Device', backref='cpu_reports')


class MemoryReport(db.Model):
    # Overriding the default name "MemoryReport" with memory_report
    __tablename__ = 'memory_report'

    # Column definition
    memory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sys_time = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow())
    device_time = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow())
    memory_used = db.Column(db.Float, nullable=False)
    memory_total = db.Column(db.Float, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.device_id'), nullable=False)

    # Foreign Key Reference
    device = db.relationship('Device', backref='memory_reports')


class DiskReport(db.Model):
    # Overriding the default name "Device" with device
    __tablename__ = 'disk_report'

    # Column definition
    disk_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sys_time = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow())
    device_time = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow())
    disk_size = db.Column(db.Float, nullable=False)
    disk_used = db.Column(db.Float, nullable=False)
    disk_free = db.Column(db.Float, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.device_id'), nullable=False)

    # Foreign Key Reference
    device = db.relationship('Device', backref='disk_reports')


class ProcessReport(db.Model):
    # Overriding the default name "Device" with device
    __tablename__ = 'process_report'

    # Column definition
    proc_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sys_time = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow())
    device_time = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow())
    pid = db.Column(db.Integer, nullable=False, autoincrement=True)
    process_name = db.Column(db.String(length=100), nullable=False)
    cpu_usage = db.Column(db.Float, nullable=False)
    mem_usage = db.Column(db.Float, nullable=False)
    disk_usage = db.Column(db.Float, nullable=False)
    thread_count = db.Column(db.Integer, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.device_id'), nullable=False)

    # Foreign Key Reference
    device = db.relationship('Device', backref='process_reports')
