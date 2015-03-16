from setuptools import setup
from setuptools import find_packages

setup(
    name='GeobricksGeostatistics',
    version='0.0.4',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=find_packages(),
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    description='Geobricks geostatistics library.',
    install_requires=[
        'watchdog',
        'flask',
        'flask-cors',
        'multiprocessing',
        'GeobricksCommon',
        'GeobricksGISRaster',
        'GeobricksSpatialQuery',
    ],
    url='http://pypi.python.org/pypi/GeobricksGISRaster/',
    keywords=['geobricks', 'geoserver', 'gis', 'raster']
)
