#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        pattClient.py
#
# Purpose:     This module create a file PATT check client and feed back the 
#              PATT value when the server connect and send address list to it.
#              
# Author:       Yuancheng Liu
#
# Created:     2020/03/16
# Copyright:   YC @ Singtel Cyber Security Research & Development Laboratory
# License:     YC
#-----------------------------------------------------------------------------

import udpCom
import pattChecker as patt

UDP_PORT = 5006
CONFIG_FILE = 'pattClientConfig.txt'

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class pattClient(object):
    def __init__(self, parent):
        """ Create a UDP server and feed back the checked file's PATT value 
            when the client connect to it.
            Init example: checker = pattClient(None)
        """
        self.paramDict = self.loadConfig()
        self.tester = patt.pattChecker(self.paramDict['BLKNU'], self.paramDict['FMPAT'])
        self.server = udpCom.udpServer(None, UDP_PORT)

    #-----------------------------------------------------------------------------
    def loadConfig(self):
        """ load the config parameter from the config file."""
        paramDict = {   'BLKNU': 4,                 # display frame rate
                        'FMPAT': 'firmwareSample',  # Checked firmware name
        }
        with open(CONFIG_FILE, "r") as fh:
            lines = fh.readlines()
            for line in lines:
                line = line.rstrip()
                if line == '' or line[0] == '#': continue
                key, val = line.split(':')
                paramDict[key] = int(val) if key == 'BLKNU' else val
        return paramDict

    #-----------------------------------------------------------------------------
    def run(self):
        print("PATT checker client run() start.")
        self.server.serverStart(handler=self.msgHandler)
        print("PATT checker client run() end.")

    #-----------------------------------------------------------------------------
    def msgHandler(self, msg):
        """ Calculate the 
        """
        print("Incomming address list: %s" % str(msg))
        addrList = msg.decode('utf-8').split(';')
        testChSm = self.tester.getCheckSum(address_list=[int(i) for i in addrList])
        return testChSm

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    checker = pattClient(None)
    checker.run()

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()



