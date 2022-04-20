"""
Encapsulates all test cases for expected unit
behavior of Matrix Systems.

@date 4.15.22
@author Christian Saltarelli
"""
import sys
import pytest
import sqlalchemy

sys.path.append("..")
from app import models


def test_create_valid_user(test_client, test_user):
    """
    GIVEN the Matrix System configured for Testing
    WHEN A User object is created w/ valid data
    THEN check the email and password_hash are defined correctly
    """
    assert test_user.email == 'test@gmail.com'
    assert test_user.password_hash != 'testtesttest'


def test_create_invalid_user(test_client, init_database):
    """
    GIVEN the Matrix System configured for Testing
    WHEN A user object is created w/ invalid data
    THEN verify that the attempted user wasn't created
    """
    invalid_user = models.User(email=2)

    with pytest.raises(sqlalchemy.exc.OperationalError):
        init_database.session.add(invalid_user)
        init_database.session.commit()


def test_assign_user_role(test_client, init_database, test_user):
    """
    GIVEN the Matrix System configured for Testing
    WHEN A user object is created w/ valid data
    THEN Verify we can assign a role to the user
    """
    test_role = models.Role(role_name='Test', role_desc='Test Role.')
    init_database.session.add(test_role)
    init_database.session.commit()

    test_user_role = models.UserRole(role_id=test_role.role_id, user_id=test_user.id)
    init_database.session.add(test_user_role)
    init_database.session.commit()

    result = models.UserRole.query.filter_by(user_id=test_user.id).first().user_id

    assert result == test_user.id


def test_create_valid_device(test_client, test_device):
    """
    GIVEN the Matrix System configured for Testing
    WHEN A device object is created w/ valid data
    THEN Verify we can query for the expected device
    """
    assert models.Device.query.filter_by(device_id=test_device.device_id).first() is not None


def test_create_invalid_device(test_client, init_database):
    """
    GIVEN the Matrix System configured for Testing
    WHEN A device object is created w/ invalid data
    THEN Verify that the attempted device wasn't created
    """
    invalid_device = models.Device()

    with pytest.raises(sqlalchemy.exc.OperationalError):
        init_database.session.add(invalid_device)
        init_database.session.commit()


def test_create_valid_cpu_record(test_client, init_database, test_device):
    """
    GIVEN the Matrix System configured for Testing
    WHEN A CPU record is created w/ valid data
    THEN Verify we can query for the expected CPU record by device
    """
    cpu_data = models.CPUReport(speed_curr=0.0,
                                speed_min=0.0,
                                speed_max=0.0,
                                device_id=test_device.device_id)
    init_database.session.add(cpu_data)
    init_database.session.commit()

    assert models.CPUReport.query.filter_by(device_id=test_device.device_id).first() is not None


def test_create_invalid_cpu_record(test_client, init_database):
    """
    GIVEN the Matrix System configured for Testing
    WHEN A CPU record is created w/ invalid data
    THEN Verify that the attempted record wasn't created
    """
    invalid_cpu_data = models.CPUReport(speed_curr=0.0,
                                        speed_min=0.0,
                                        speed_max=0.0)

    with pytest.raises(sqlalchemy.exc.OperationalError):
        init_database.session.add(invalid_cpu_data)
        init_database.session.commit()


def test_create_valid_memory_record(test_client, init_database, test_device):
    """
    GIVEN the Matrix System configured for Testing
    WHEN A Memory Record is created w/ valid data
    THEN Verify we can query for the expected Memory record by device
    """
    memory_data = models.MemoryReport(memory_used=0.0,
                                      memory_total=0.0,
                                      device_id=test_device.device_id)
    init_database.session.add(memory_data)
    init_database.session.commit()

    assert models.MemoryReport.query.filter_by(device_id=test_device.device_id).first() is not None


def test_create_invalid_memory_record(test_client, init_database):
    """
    GIVEN the Matrix System configured for Testing
    WHEN A Memory record is created w/ invalid data
    THEN Verify that the attempted record wasn't created
    """
    invalid_memory_data = models.MemoryReport(memory_used=0.0,
                                              memory_total=0.0)

    with pytest.raises(sqlalchemy.exc.OperationalError):
        init_database.session.add(invalid_memory_data)
        init_database.session.commit()


def test_create_valid_disk_record(test_client, init_database, test_device):
    """
    GIVEN the Matrix System configured for Testing
    WHEN A Disk record is created w/ valid data
    THEN Verify we can query for the expected Disk record by device
    """
    disk_data = models.DiskReport(disk_size=0.0,
                                  disk_used=0.0,
                                  disk_free=0.0,
                                  device_id=test_device.device_id)
    init_database.session.add(disk_data)
    init_database.session.commit()

    assert models.DiskReport.query.filter_by(device_id=test_device.device_id).first() is not None


def test_create_invalid_disk_record(test_client, init_database):
    """
    GIVEN the Matrix System configured for Testing
    WHEN A Disk record is created w/ invalid data
    THEN verify that the attempted record wasn't created
    """
    invalid_disk_data = models.DiskReport(disk_size=0.0,
                                          disk_used=0.0,
                                          disk_free=0.0)

    with pytest.raises(sqlalchemy.exc.OperationalError):
        init_database.session.add(invalid_disk_data)
        init_database.session.commit()


def test_create_valid_process_record(test_client, init_database, test_device):
    """
    GIVEN the Matrix System configured for Testing
    WHEN a Process record is created w/ valid data
    THEN verify we can query for the expected Process record by device
    """
    process_data = models.ProcessReport(cpu_usage=0.0,
                                        mem_usage=0.0,
                                        disk_usage=0.0,
                                        thread_count=0.0,
                                        device_id=test_device.device_id)
    init_database.session.add(process_data)
    init_database.session.commit()

    assert models.ProcessReport.query.filter_by(device_id=test_device.device_id).first() is not None


def test_create_invalid_process_record(test_client, init_database):
    """
    GIVEN the Matrix System configured for Testing
    WHEN a Process record is created w/ invalid data
    THEN verify that the attempted record wasn't created
    """
    invalid_process_data = models.ProcessReport(cpu_usage=0.0,
                                                mem_usage=0.0,
                                                disk_usage=0.0,
                                                thread_count=0.0)

    with pytest.raises(sqlalchemy.exc.OperationalError):
        init_database.session.add(invalid_process_data)
        init_database.session.commit()
