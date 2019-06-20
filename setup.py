from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

# fetch values from package.xml
setup_args = generate_distutils_setup(
    name='esiaf_channel_utils',
    version='0.0.1',
    description='Nodes which split and combine channels for the esiaf framework',
    url='---none---',
    author='rfeldhans',
    author_email='rfeldh@gmail.com',
    license='---none---',
    install_requires=[
    ],
    packages=['esiaf_channel_utils']

)

setup(**setup_args)