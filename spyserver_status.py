#!/usr/bin/env python
#
# Tapo P110 to InfluxDB Collection
#
import sys
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from pprint import pprint
from netstat import *

# Collect Environment Variables
SPYSERVER_PORT = int(os.environ.get("SPYSERVER_PORT"))
SPYSERVER_NAME = os.environ.get("SPYSERVER_NAME")
INFLUXDB_URL = os.environ.get("INFLUXDB_URL")
INFLUXDB_TOKEN = os.environ.get("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.environ.get("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.environ.get("INFLUXDB_BUCKET")
INFLUXDB_MEASNAME = os.environ.get("INFLUXDB_MEASNAME")


print(f"Spyserver Port: \t{SPYSERVER_PORT}")
print(f"Spyserver Name: \t{SPYSERVER_NAME}")

print(f"InfluxDB URL: \t{INFLUXDB_URL}")
print(f"InfluxDB Token: \t{INFLUXDB_TOKEN}")
print(f"InfluxDB Org: \t{INFLUXDB_ORG}")
print(f"InfluxDB Bucket: \t{INFLUXDB_BUCKET}")
print(f"InfluxDB Measurement Name: \t{INFLUXDB_MEASNAME}")

# Collect SpyServer Status Data

def get_spyserver_ports() -> list:
    """ Return a list of currently running spyserver TCP ports """
    return netstat_listeners(program_filter="spyserver").keys()


def get_spyserver_users(ports: list) -> dict:
    """ Get the lists of users connected to each supplied Spyserver port """
    _clients = netstat_users()

    print(_clients)

    _output = {}
    for _port in ports:
        if _port in _clients:
            _output[_port] = _clients[_port]
        else:
            _output[_port] = []

    return _output


users = get_spyserver_users([SPYSERVER_PORT])


meas_point = {
    "measurement": INFLUXDB_MEASNAME,
    "tags": {"name": SPYSERVER_NAME},
    "fields": {"users": len(users[SPYSERVER_PORT])}
}

print(meas_point)

# Push into InfluxDB
write_client = influxdb_client.InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = write_client.write_api(write_options=SYNCHRONOUS)
write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=meas_point)

print("Done!")