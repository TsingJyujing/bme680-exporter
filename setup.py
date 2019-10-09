import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'README.md'), encoding='utf-8').read()
except:
    README = ""

setup(
    name="bme680-exporter",
    version=0.1,
    author="Tsing Jyujing",
    author_email="tsingjyujing@163.com",
    url="https://github.com/TsingJyujing/bme680-exporter",
    description="Export BME680 sensor data to Prometheus",
    install_requires=[
        "bme680",
        "smbus",
        "flask",
        "prometheus_client",
        "requests"
    ],
    long_description=README,
    packages=[
        "bme680_exporter"
    ],
    platforms='any',
    zip_safe=True,
    include_package_data=True,
    scripts=[
        "bin/bme680-exporter-push"
    ]
)
