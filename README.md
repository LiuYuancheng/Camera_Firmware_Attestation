# Camera Firmware Attestation

#### 1. Introduction

This project contains two sections: 

**Camera Detection** : In this section we will create a camera video/image capture program(client) running on raspberry PI and send the camera image to the motion detection programming(server) running on the computer which connected to the raspberry PI. 

**Firmware attestation**: In this section we will create a firmware checker and verifier program to do the firmware attestation by using PATT algorithm.  The check running in raspberry PI will calculate the camera firmware( camera Client) 's PATT value based on the random bytes address send from the verifier. The verifier will compare the firmware's PATT value with its local file's calculation result to give the attestation result. 

###### Test Situation and Program UI View

![](doc/RM_testRun.gif)



![](doc/RM_testSituation.png)

------

#### 2. Program Setup

###### Development Environment

> Python 3.7.4, C

###### Additional Lib Need

1.  Python OpenCV (need to install for motion detection and target tracking)

   ```
   Raspberry PI install opencv: 
   
   sudo pip3 install opencv-contrib-python==3.4.3.18
   sudo apt-get install libhdf5-dev
   sudo apt-get install libatlas-base-dev
   sudo apt-get install libjasper-dev
   sudo apt-get install libqt4-test
   sudo apt-get install libqtgui4
   sudo apt-get update
   ```

2. numpy (need for image encode/decode)

   ```
   pip install numpyHardware (Raspberry PI3B+ with Camera module)
   ```

###### Hardware Need

Raspberry PI3B+ with Camera module. https://projects.raspberrypi.org/en/projects/getting-started-with-picamera

![](doc/RM_camera.jpg)

------

#### 3. System Design

Communication Protocol 

| The camera client+server and the PATT check+verifier will communicate with each other by UDP with different port. |
| ------------------------------------------------------------ |
| Camera client [ UDP server port: 5005]  <= image request <= Camera server [UDP client] |
| Camera client [ UDP server port: 5005]  => encoded image => Camera server [UDP client] |
| PATT checker [ UDP server port: 5006]  <= Random address list <= PATT verifier [UDP client] |
| PATT checker [ UDP server port: 5006]  => cameraClient PATT value => PATT verifier [UDP client] |













> Last edit by LiuYuancheng(liu_yuan_cheng@hotmail.com) at 18/03/2020