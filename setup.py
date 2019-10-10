import os

from setuptools import setup, find_packages

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
    packages=find_packages(),
    platforms='any',
    zip_safe=True,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'bme680-exporter-push=bme680_exporter.push:start_push_service',
            'bme680-exporter-pull=bme680_exporter.service:start_web_service'
        ],
    }
)
