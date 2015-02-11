from setuptools import setup
from setuptools import find_packages

setup(
    name='GeobricksGeostatistics',
    version='0.0.2',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=find_packages(),
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    description='Geobricks geostatistics library.',
    install_requires=[
        'flask',
        'flask-cors',
        'GeobricksCommon',
        'GeobricksGISRaster',
        'GeobricksSpatialQuery',
    ],
    url='http://pypi.python.org/pypi/GeobricksGISRaster/',
    keywords=['geobricks', 'geoserver', 'gis', 'raster']
)
