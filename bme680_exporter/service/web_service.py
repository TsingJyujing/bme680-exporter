from flask import Flask, make_response
from prometheus_client import CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST

from bme680_exporter.core import SensorUpdater, create_update_function, MotionDataGenerator
from bme680_exporter.util import get_base_arg_parser, parse_key_value_pairs


def create_metrics_application(name: str, registry: CollectorRegistry):
    """
    Create a flask application to expose prometheus metrics
    :return:
    """
    app = Flask(name)

    @app.route("/metrics", methods=["GET", "POST"])
    def broadcasting_channel_interface():
        response = make_response(generate_latest(registry))
        response.headers["Content-Type"] = CONTENT_TYPE_LATEST
        return response

    return app


def parse_args():
    parser = get_base_arg_parser()
    parser.add_argument(
        "-p", "--port",
        default=8080, type=int,
        help="Service bind port number",
    )
    parser.add_argument(
        "-h", "--host",
        default='0.0.0.0', type=str,
        help="Service bind hostname",
    )
    return parser.parse_args()


def start_web_service():
    args = parse_args()
    registry = CollectorRegistry()
    app = create_metrics_application("BME680-exporter", registry)

    labels = parse_key_value_pairs(args.label)
    sensor_read_thread = SensorUpdater(
        update_data_fun=create_update_function(
            args.sensor_name,
            labels,
            registry
        ),
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
    sensor_read_thread.start()
    motion_data_generator.start()

    app.run(
        host=args.host,
        port=args.port,
    )
