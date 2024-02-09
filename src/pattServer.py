#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        pattServer.py
#
# Purpose:     This module will create a PATT file checker program. It will 
#              send the PATT bytes check list to the client and compare the 
#              feedback PATT value.
#              
# Author:      Yuancheng Liu
#
# Version:     v_1.0.2
# Created:     2020/03/16
# Copyright:   Copyright (c) 2020 LiuYuancheng
# License:     MIT License
#-----------------------------------------------------------------------------
import time
import udpCom
import pattChecker as patt

UDP_PORT = 5006
TEST_MD = True # test mode flag
CONFIG_FILE = 'pattServerConfig.txt'

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class pattServer(object):
    def __init__(self, parent):
        """ Create a UDP server and feed back the checked file's PATT value 
            when the client connect to it.
            Init example: checker = pattServer(None)
        """
        self.paramDict = self.loadConfig()
        # Init the PATT calculator.
        self.verifier = patt.pattChecker(self.paramDict['BLKNU'], self.paramDict['FMPAT'])
        # Init the communicate UDP client.
        self.client = udpCom.udpClient((self.paramDict['IPADD'], UDP_PORT))

    #-----------------------------------------------------------------------------
    def loadConfig(self):
        """ load the config parameter from the config file."""
        paramDict = {   'IPADD': '127.0.0.1',       # IPaddress
                        'BLKNU': 4,                 # display frame rate
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
        """ Calculate the local file's PATT value and send the check address 
            to the client program, the compare the feed back value.
        """
        # Call the get getAddrList() to generate the random address dynamically 
        addrStr = ';'.join([str(i) for i in self.verifier.getAddrList()])
        verifierChSm = self.verifier.getCheckSum()
        result = self.client.sendMsg(addrStr, resp=True)
        print('Local_PATT: %s' %verifierChSm)
        print('CameraPATT: %s' %result.decode('utf-8'))
        if verifierChSm == result.decode('utf-8'):
            print('Patt check result: verifierChechsum == camreaCheckSum')
            print('The camera firmware attestation successful')
        else:
            print('Patt check result: verifierChechsum != camreaCheckSum')
            print('The camera firmware attestation fail.')

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    pattSer = pattServer(None)
    pattSer.run()
    print('Finished')
    time.sleep(10)

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()


