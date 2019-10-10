# bme680-exporter

## Introduction

A prometheus exporter to export BME680 sensor data.

## Hardware

For my option, I'm using RaspberryPiZero + BME680 (with I2C protocol).

Connect you sensor module to pi, and [enable your I2C](https://www.raspberrypi.org/forums/viewtopic.php?t=168787)

## Software

It support 2 ways to collect your data:

- Start a web server and http://ip:port/metrics will expose your sensor data
    - Then it can be pulled by [Prometheus](https://prometheus.io/)
- Push your data to [pushgateway](https://github.com/prometheus/pushgateway)
    - And use prometheus to pull data from push gateway
    - (todo) Save to database by some [service](https://github.com/quickstats/quickstats-django)

### Install

```bash
pip3 install git+https://github.com/TsingJyujing/bme680-exporter.git
```

### Public Parameters

These parameters both works on push/pull service.

|name|required|default|type|example|comment|
|-|-|-|-|-|-|
|-u/--update-period|no|5.0|float(second)|3.0|The time gap to update/push the data|
|-i/--i2c-address|no|null|str|0x76|The I2C address of your BME680 chip, default will auto select|
|-n/--sensor-name|yes|-|str|home|The name of sensor, it will effect metrics name|
|-l/--label|no||str|key1=value1,key2=value2|Metric labels key-value pairs|


### Start Server

```bash
bme680-exporter-pull [options]
```

|name|required|default|type|example|comment|
|-|-|-|-|-|-|
|-p/--port|no|8080|int|8080|The port to listen|
|-h/--host|no|0.0.0.0|str|127.0.0.1|The host name to listen|

### Start Push Service

```bash
bme680-exporter-push [options]
```

|name|required|default|type|example|comment|
|-|-|-|-|-|-|
|-s/--service|yes|-|str|http://pushgateway.xxx.com/metrics/job/my_job|The URL to push|

## Reference

- [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
- [BME680 Datasheet](https://raw.githubusercontent.com/SeeedDocument/Grove-Temperature-Humidity-Pressure-Gas-Sensor_BME680/master/res/BME680.pdf)
- [BME680 Official Driver](https://github.com/BoschSensortec/BME680_driver)
