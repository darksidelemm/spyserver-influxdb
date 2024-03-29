#!/bin/bash
#
# Spyserver Status -> InfluxDB Collection Script
#
# Run with cron on whatever update rate you want
#

# Enter the port number of your spyserver, and the name to use with it here.
# Note that this must be run on the same machine as the spyserver.
export SPYSERVER_PORT="5040"
export SPYSERVER_NAME="40m"


# InfluxDB Settings
export INFLUXDB_URL="http://localhost:8086"
export INFLUXDB_TOKEN=""
export INFLUXDB_ORG=""
export INFLUXDB_BUCKET="Spyserver"
export INFLUXDB_MEASNAME="spyserver_status"
 
# Use a local venv if it exists
VENV_DIR=venv
if [ -d "$VENV_DIR" ]; then
    echo "Entering venv."
    source $VENV_DIR/bin/activate
fi

python3 spyserver_status.py
