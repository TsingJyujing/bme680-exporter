import logging
import time
import traceback
from threading import Thread
from typing import Optional, Callable

import bme680
from bme680 import FieldData
from prometheus_client import Gauge, CollectorRegistry, generate_latest

log = logging.getLogger(__file__)


def set_gauge(gauge: Gauge, value: float, labels: dict):
    if len(labels) > 0:
        gauge.labels(**labels).set(value)
    else:
        gauge.set(value)


def create_update_function(sensor_name: str, labels: dict, registry: CollectorRegistry):
    """
    Generate function with creating 5 Gauge type metrics
    In the name of sensor_{sensor name}_{metric type}
    :param registry:
    :param labels: metric label names
    :param sensor_name: the name of sensor
    :return:
    """

    temperature_gauge = Gauge(
        "sensor_{}_temperature".format(sensor_name),
        "Temperature metric of {}".format(sensor_name),
        labelnames=list(labels.keys()),
        registry=registry
    )

    humidity_gauge = Gauge(
        "sensor_{}_humidity".format(sensor_name),
        "Humidity metric of {}".format(sensor_name),
        labelnames=list(labels.keys()),
        registry=registry
    )

    pressure_gauge = Gauge(
        "sensor_{}_pressure".format(sensor_name),
        "Pressure metric of {}".format(sensor_name),
        labelnames=list(labels.keys()),
        registry=registry
    )

    gas_resistance_gauge = Gauge(
        "sensor_{}_gas_resistance".format(sensor_name),
        "Gas sensor resistance metric of {}".format(sensor_name),
        labelnames=list(labels.keys()),
        registry=registry
    )

    def update_data(data: FieldData):

        set_gauge(temperature_gauge, data.temperature, labels)
        set_gauge(humidity_gauge, data.humidity, labels)
        set_gauge(pressure_gauge, data.pressure, labels)
        if data.heat_stable:
            set_gauge(gas_resistance_gauge, data.gas_resistance, labels)
        else:
            log.warning("GAS sensor not prepared yet")

    return update_data


class SensorUpdater(Thread):
    def __init__(
            self,
            update_data_fun: Callable[[FieldData], None],
            i2c_address: Optional[int] = None,
            update_period: float = 5.0
    ):
        """
        Sensor to update
        :param i2c_address: Address of your device, it could be 0x76/0x77
        :param update_data_fun: How to deal with updated data
        :param update_period: Update gap
        """
        super().__init__()
        if i2c_address is not None:
            sensor = bme680.BME680(i2c_address)
        else:
            try:
                sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY)
            except IOError:
                sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        self._sensor = sensor
        self._update_data_fun = update_data_fun
        self.update_period: float = update_period
        self._stop: bool = False
        self.init_device()

    def init_device(self):
        self._sensor.set_humidity_oversample(bme680.OS_2X)
        self._sensor.set_pressure_oversample(bme680.OS_4X)
        self._sensor.set_temperature_oversample(bme680.OS_8X)
        self._sensor.set_filter(bme680.FILTER_SIZE_3)
        self._sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)

        for name in dir(self._sensor.data):
            value = getattr(self._sensor.data, name)
            if not name.startswith('_'):
                log.info('Initialize reading: {}={}'.format(name, value))

        self._sensor.set_gas_heater_temperature(320)
        self._sensor.set_gas_heater_duration(150)
        self._sensor.select_gas_heater_profile(0)

    def stop_update(self):
        self._stop = True

    def run(self) -> None:
        while not self._stop:
            try:
                if self._sensor.get_sensor_data():
                    self._update_data_fun(
                        self._sensor.data
                    )
                else:
                    raise Exception("Error while reading sensor, return False.")
            except KeyboardInterrupt as _:
                log.info("Exit manually")
                break
            except Exception as _:
                log.error(
                    "Error while reading sensor data: {}".format(traceback.format_exc())
                )
            finally:
                time.sleep(self.update_period)
