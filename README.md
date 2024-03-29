# spyserver-influxdb
Collect SpyServer Usage information and feed into InfluxDB

# SpyServer User Count to InfluxDB Collector
Very quickly developed SpyServer User Count to InfluxDB data collector.

## Setup
```
python3 -m venv venv
pip install -r requirements.txt
```

Edit spyserver_stats.sh and update env vars with appropriate settings.

Setup crontab to run spyserver_stats.sh every minute.

## InfluxDB Data Point

Data is added in the following format:
```
{
    'measurement': 'spyserver_users', 
    'tags': {'name': '160m'}, 
    'fields': {
        'users': 2
        }
}
```