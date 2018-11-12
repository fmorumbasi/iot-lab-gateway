#! /usr/bin/env python
# -*- coding:utf-8 -*-

# This file is a part of IoT-LAB gateway_code
# Copyright (C) 2015 INRIA (Contact: admin@iot-lab.info)
# Contributor(s) : see AUTHORS file
#
# This software is governed by the CeCILL license under French law
# and abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# http://www.cecill.info.
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.


""" CLI client for cc2538_cmd

Usage:
        cc2538_cmd flash <node> <firmware_path>

"""
import argparse

from gateway_code.nodes import open_node_class
from gateway_code.utils import cc2538
from gateway_code.utils.cli import log_to_stderr


_NODES = ('FIREFLY',)


def _setup_parser():
    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers()

    flash = sub_parser.add_parser('flash')
    flash.set_defaults(cmd='flash')
    flash.add_argument('node', type=str, choices=_NODES)
    flash.add_argument('firmware', type=str, help="Firmware name")

    reset = sub_parser.add_parser('reset')
    reset.set_defaults(cmd='reset')
    reset.add_argument('node', type=str, choices=_NODES)

    return parser


@log_to_stderr
def main():
    """ cc2538 main function """

    parser = _setup_parser()
    opts = parser.parse_args()
    node = open_node_class(opts.node.lower())
    ret = 0
    config = {'port': node.TTY, 'baudrate': node.BAUDRATE}
    cc2538_tool = cc2538.CC2538(config)

    if opts.cmd == 'flash':
        ret += cc2538_tool.flash(opts.firmware)
    elif opts.cmd == 'reset':
        ret += cc2538_tool.reset()
    else:  # pragma: no cover
        raise ValueError('Uknown Command {}'.format(opts.cmd))

    # Same code as 'openocd'
    # pylint:disable=duplicate-code
    if ret == 0:
        print '%s OK\n' % opts.cmd
        # pylint:disable=duplicate-code
    else:
        print '%s KO: %d\n' % (opts.cmd, ret)
        # pylint:disable=duplicate-code

    return ret