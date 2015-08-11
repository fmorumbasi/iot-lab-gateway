#! /usr/share/env python
# -*- coding:utf-8 -*-

"""
setup.py deployement script

Install all the `gateway code` on a gateway

    python setup.py release

It runs the `install` command and the `post_install` procedure.

Tests commands:

    python setup.py nosetests
    python setup.py integration

Pylint and pep8 checker:

    python setup.py lint
    python setup.py pep8


"""

from setuptools import setup, Command, Extension, find_packages
from setuptools.command.build_ext import build_ext

import sys
import os
import subprocess
import shutil
from glob import glob

# pylint: disable=attribute-defined-outside-init
# pylint <= 1.3
# pylint: disable=too-many-public-methods
# pylint >= 1.4
# pylint: disable=too-few-public-methods

PACKAGE = 'gateway_code'


def get_version(package):
    """ Extract package version without importing file
    Importing cause issues with coverage,
        (modules can be removed from sys.modules to prevent this)
    Importing __init__.py triggers importing rest and then requests too

    Inspired from pep8 setup.py
    """
    with open(os.path.join(package, '__init__.py')) as init_fd:
        for line in init_fd:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])  # pylint:disable=eval-used


SCRIPTS = glob('bin/scripts/*')
SCRIPTS += ['control_node_serial/control_node_serial_interface']

INSTALL_REQUIRES = ['argparse', 'bottle', 'paste', 'pyserial']

UDEV_RULES = glob('bin/rules.d/*.rules')


class BuildExt(build_ext):
    """ Overwrite build_ext to build control node serial """

    def run(self):
        """ Build control node serial interface """
        # Don't build for Pylint
        if self.distribution.script_args == ['lint']:
            return

        args = ['make', '-C', 'control_node_serial', 'realclean', 'all']
        try:
            subprocess.check_call(args)
        except subprocess.CalledProcessError as err:
            exit(err.returncode)


class Release(Command):
    """ Install and do the 'post installation' procedure too.
    Meant to be used directly on the gateways """
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            subprocess.check_call(['python', 'setup.py', 'install'])
        except subprocess.CalledProcessError as err:
            exit(err.returncode)
        self.post_install()

    @staticmethod
    def post_install():
        """ Install init.d script
        Install the udev rules files
        Add www-data user to dialout group """

        # setup init script
        init_script = 'gateway-server-daemon'
        update_rc_d_args = ['update-rc.d', init_script,
                            'start', '80', '2', '3', '4', '5', '.',
                            'stop', '20', '0', '1', '6', '.']
        shutil.copy('bin/init_script/' + init_script, '/etc/init.d/')
        os.chmod('/etc/init.d/' + init_script, 0755)
        subprocess.check_call(update_rc_d_args)

        # Udev rules
        for rule in UDEV_RULES:
            shutil.copy(rule, '/etc/udev/rules.d/')

        #  add `www-data` user to `dialout` group
        subprocess.check_call(['usermod', '-a', '-G', 'dialout', 'www-data'])


setup(name=PACKAGE,
      version=get_version(PACKAGE),
      description='Linux Gateway code',
      author='IoT-Lab Team',
      author_email='admin@iot-lab.info',
      url='http://www.iot-lab.info',
      packages=find_packages(),

      scripts=SCRIPTS,
      include_package_data=True,
      package_data={'static': ['static/*']},
      ext_modules=[Extension('control_node_serial_interface', [])],

      cmdclass={
          'build_ext': BuildExt,
          'release': Release,
      },
      install_requires=INSTALL_REQUIRES)
