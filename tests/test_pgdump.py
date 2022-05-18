import pytest
import subprocess

from pgbackup import pgdump

url = "postgres://user:password@example.com:5432/db_one"

def test_dump_calls_pg_dump(mocker):
    """
    Utilize pg_dump with the database URL
    """

    mocker.patch('subprocess.Popen')
    assert pgdump.dump(url)
    subprocess.Popen.assert_called_with(['pg_dump', url], stdout=subprocess.PIPE)


def test_dump_handles_oserror(mocker):
    """
    pgdump.dump returns a reasonable error if pg_dump isn't installed.
    """
    mocker.patch('subprocess.Popen', side_effect=OSError('No such file'))
    with pytest.raises(SystemExit):
        pgdump.dump(url)

def test_dump_file_name_without_timestamp():
    """
    pgdump.dump_file_name returns name of the database
    """
    assert pgdump.dump_file_name(url) == 'db_one.sql'

def test_dump_file_name_with_timestamp():
    """
    pgdump.dump_file_name returns name of the database with timestamp
    """
    timestamp = "2022-05-18T11:00:00"
    assert pgdump.dump_file_name(url, timestamp) == f"db_one-{timestamp}.sql"
