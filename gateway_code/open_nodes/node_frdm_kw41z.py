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

""" Open Node FRDM-KW41Z experiment implementation """

from gateway_code.config import static_path
from gateway_code.open_nodes.common.node_jlink import NodeJLinkBase


class NodeFrdmKw41z(NodeJLinkBase):
    """ Open node FRDM-KW41Z implemention """

    TYPE = 'frdm_kw41z'
    OPENOCD_CFG_FILE = static_path('iot-lab-frdm-kw41z.cfg')
    FW_IDLE = static_path('frdm-kw41z_idle.elf')
    FW_AUTOTEST = static_path('frdm-kw41z_autotest.elf')
    DIRTY_SERIAL = False