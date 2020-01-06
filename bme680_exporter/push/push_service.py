import atexit
import logging
import signal

import requests
from bme680 import FieldData
from prometheus_client import CollectorRegistry, generate_latest

from bme680_exporter.core import SensorUpdater, create_update_function, MotionDataGenerator
from bme680_exporter.util import get_base_arg_parser, parse_key_value_pairs

log = logging.getLogger(__file__)


def parse_args():
    parser = get_base_arg_parser()
    parser.add_argument(
        "-s", "--service",
        required=True, type=str,
        help="Prometheus Pushgateway address",
    )
    return parser.parse_args()


def start_push_service():
    args = parse_args()

    registry = CollectorRegistry()

    labels = parse_key_value_pairs(args.label)
    update_fun = create_update_function(
        args.sensor_name,
        labels,
        registry
    )

    service = args.service

    def push_metrics(data: FieldData):
        update_fun(data)
        data = generate_latest(registry)
        resp = requests.post(service, data=data)
        resp.raise_for_status()

    sensor_read_thread = SensorUpdater(
        update_data_fun=push_metrics,
        i2c_address=int(args.i2c_address, base=16) if args.i2c_address is not None else None,
        update_period=args.update_period
    )

    motion_data_generator = MotionDataGenerator(
        update_period=args.sensor_period,
        sensor_name=args.sensor_name,
        port_id=int(args.port_id),
        labels=labels,
        registry=registry
    )

    def signal_handler(*args):
        sensor_read_thread.stop_update()
        requests.delete(service).raise_for_status()

    for signal_id in (signal.SIGINT, signal.SIGTERM):
        signal.signal(signal_id, signal_handler)

    atexit.register(signal_handler)
    motion_data_generator.start()
    sensor_read_thread.run()
