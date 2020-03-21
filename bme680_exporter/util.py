from argparse import ArgumentParser


def get_base_arg_parser() -> ArgumentParser:
    """
    Get a base arg parser for common settings
    :return:
    """
    parser = ArgumentParser(description="BME680 sensor exporter service")
    parser.add_argument(
        "-u", "--update-period",
        default=5.0, type=float,
        help="Period to read sensor and update the metrics",
    )
    parser.add_argument(
        "-i", "--i2c-address",
        default=None, type=str,
        help="I2C address of your BME680 device, it should be 0x76 or 0x77",
    )
    parser.add_argument(
        "-n", "--sensor-name",
        type=str, required=True,
        help="Sensor's name, like home or kitchen.",
    )
    parser.add_argument(
        "-l", "--label",
        default="", type=str,
        help="Metric labels key-value pairs, example: key1=value1,key2=value2",
    )
    parser.add_argument(
        "-r", "--sensor-period",
        default=0.05, type=float,
        help="Period to read motion sensor",
    )
    parser.add_argument(
        "--port-id",
        type=int, required=True,
        help="Wiring port of the motion sensor",
    )
    return parser


def parse_key_value_pairs(kv_pairs: str):
    """
    Convert key value pairs from k1=v1,k2=v2 => {k1:v1,k2,v2} dict
    :param kv_pairs:
    :return:
    """
    return {
        kvs.split("=")[0]: kvs.split("=")[1] for kvs in kv_pairs.split(",") if kvs.find("=") >= 0
    }
