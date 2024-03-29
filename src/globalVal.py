#-----------------------------------------------------------------------------
# Name:        globalVal.py
#
# Purpose:     This module is used set the Local config file as global value 
#              which will be used in the other modules.
# Author:      Yuancheng Liu
#
# Created:     2019/05/17
# Copyright:   Copyright (c) 2020 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
import os

dirpath = os.getcwd()
print("Camera firmware attesttion: Current working directory is : %s" %dirpath)

#-------<GLOBAL PARAMTERS>-----------------------------------------------------

# parameters used by PATT firmware attestation.
RANDOM_RANGE_MAX = 10000
RANDOM_RANGE_MIN = 1000
FULL_MEMORY_SIZE_NODE_MCU = 64
WORD_SIZE = 16
BOOT_LOADER_OFFSET = 256
