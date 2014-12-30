from setuptools import setup
from setuptools import find_packages

setup(
    name='GeobricksGeostatistics',
    version='0.1.4',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=find_packages(),
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    description='Geobricks geostatistics library.',
    install_requires=[
        'flask',
        'flask-cors',
        #'pygdal', #this will throw an error because is based on the currently installed gdal version
        # this is not a real dependendency, it's just passed on the method
        'GeobricksCommon',
        'GeobricksGISRaster',
        'GeobricksDBMS',
    ],
    url='http://pypi.python.org/pypi/GeobricksGISRaster/',
    keywords=['geobricks', 'geoserver', 'gis', 'raster']
)
