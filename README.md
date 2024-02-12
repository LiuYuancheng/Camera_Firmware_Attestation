# OT Cyber Attack Case Study [Safety Camera Replay attack and Firmware Attestation]

**Program Design Purpose**: The objective of this cyber attack case study is aim to develop a workshop using the train detection safety camera system and the dynamic firmware attestation algorithm introduced in paper [PAtt: Physics-based Attestation of Control Systems](https://www.usenix.org/system/files/raid2019-ghaeini.pdf) to illustrate a practical demonstration of replay attack on a safety surveillance camera in railway OT-system. In the attack scenario, the replay attack is a advanced OT system cyber attacker based on a successful camera firmware attack and the station docking area train detection camera in the train surveillance system which used as a double safety mechanism of the train detection sensor.  The attack scenario involves a red team attacker planted a malicious firmware in the train detection camera, capturing video footage from the camera,  replaying then sending it back to station control room to mess up the safety surveillance system and station operator.

![](doc/img/overview.png)

**Attacker Vector** : Firmware Attack, Replay Attack

>  Important : The demonstrated attack case is used for education and training for different level of IT-OT cyber security ICS course, please don't apply it on any real world system.

[TOC]

------

### Introduction

This case study aims to develop a train detection surveillance camera which used as a double safety mechanism of the railway station's docking assistant system, then use the platform to demonstrate the potential replay attack impact of the system. This project contains two main sections: 

**Railway OT system station docking  assistant system** :  In our railway emulation system, we will develop a mechanism for the railway station operator the control the rail docking in the station. The system contents a double safety check mechanism both use the train position sensor and the train visual detection camera, when any of the 2 sensor detected a train is moving entering a station, it will active the train brake to slow down the train's speed. 

**OT system replay attack demo** : this section will demo the red team attacker attack the railway docking double safety check mechanism via false data injection attack to the train position sensor-signal control Chain via false data injection (FCI) attack. Then mess up the safety camera detection system via firmware attack and the replay attack.

#### Railway OT system station docking  assistant system 

In our railway OT system at each station, there will be 2 different sensors (position sensor and camera) use detected a train is moving entering a station. The system workflow is shown below: 

![](doc/img/dockingworkflow.png)

The will be a position sensor and a train motion and object detection camera in the safety surveillance system. When a train is moving forward a station and enter the docking prepare range: 

- The position and motion detection sensor which connect to the station control PLC will detect the train and PLC will send the train incoming signal to the station HMI. (As shown in the blue signal part in the work flow diagram)
- The train objective detection train will send the train passing video the the train detection computer, the computer will use CV object detection algorism to detection the train and calculate the train speed, then send the related information to the HMI.  (As shown in the green signal part in the work flow diagram)
- The HMI will process both the data from PLC and the train detection computer, check whether the train is slowing down and flow the station docking procedure. If it detected the train speed is higher than the design speed, it will active the train's brake.



#### OT System Surveillance Camera Replay Attack Demo

As shown in the previous Railway OT system station docking  assistant system introduction workflow, there are 2 safety mechanism train motion detection sensor and train object detection camera. For the motion detection sensor which connect to PLC, the red attacker can modify its sensor state via false data injection attack, but for the train object detection camera, it is hard for hacker to modify the byte data in the video stream via man in the middle attack, so the hacker will implement a firmware attack to the camera to open a "backdoor" of the camera, then do the replay attack under below steps: 

- Do a firmware attack to make the video camera runs a modified firmware with backdoor. 
- Red team attacker use the camera back door record a video which only contents the railway without a train pass. 
- When the attacker start the FDI attack on the PLC-HMI part, he also cut off the video steam send from the camera to the train detection camera video process computer , then replay send the pre-saved video recorded in previous step. 

By using the FDI attack on the PLC and replay attack on the camera, the red team attack is able to mess up the station docking  assistant system which makes the station HMI and operator not able to detect the docking train to the station.



#### Key Tactics, techniques, and procedures (TTP) of replay attack

The tactics, techniques, and procedures (TTP) of a surveillance camera replay attack involve several steps that an attacker might take to intercept, manipulate, and replay video footage from a surveillance camera in an OT (Operational Technology) system. 

**Reconnaissance**:

- **Tactics**: Identify the target surveillance camera or cameras within the OT system.
- **Techniques**: Gather information about the camera's make and model, location, network configuration, and any existing security measures.
- **Procedures**: The red team attacker will scan the network service to find the video server host by the camera, based on the camera admin page to find the camera's model then understand some of the camera API. 

**Interception and Analysis **: 

- **Tactics**: Monitor the communication between the surveillance camera and the monitoring/recording system.
- **Tactics**: Capture video footage and associated data packets as they are transmitted over the network.
- **Procedures**: The red team attacker will analyze the the camera connection client detail to find the connected video process computer to identify the replay attack target. 

**Replay**:

- Replay the manipulated video footage to the monitoring/recording system or operators.
- Ensure that the replayed footage aligns with the attacker's objectives, such as concealing unauthorized access, tampering, or other malicious activities.
- **Procedures** : The red team attack will send the pre-saved fake video to the video process computer to mess up the train detection safety mechanism. 



------

### Background Knowledge

In this section, we will introduce the basic knowledge of the replay attack and the Real Time Streaming Protocol we used to send the camera video to the image CV train detection computer.

#### Replay Attack

In the OT System cyber attack, the replay attack is often used to attack the communication channel or control chain which use complex protocol and contents large data flow which is different to use the normal attach method such as  FDI/FCI or MItm. 

A replay attack is a type of network attack in which an attacker captures a valid network transmission and then retransmit it later. **The main objective is to trick the system into accepting the retransmission of the data as a legitimate one.** Additionally, replay attacks are hazardous because it’s challenging to detect. Furthermore, it can be successful even if the original transmission was encrypted.

An attacker can lunch a replay attack to gain unauthorized access to systems or networks. Furthermore, a replay attack can disrupt the regular operation of a system by inundating it with repeated requests. An attacker can plan to carry out this attack by intercepting and retransmitting data packets over a network. Additionally, a successful replay attack can be performed by replaying recorded audio or video transmissions.

A simple replay diagram is shown below: 

![](doc/img/replayAttackDiagram.png)

Reference : https://www.baeldung.com/cs/replay-attacks

A replay attack on a camera in an OT (Operational Technology) system involves capturing video footage from the camera, altering it or replaying it, and then sending it back to deceive the system or its operators. This type of attack can have various implications depending on the specific application of the camera within the OT system. 



#### Real Time Streaming Protocol

To make the replay attack can be easily implemented, the video protocol we use for the camera is the RTSP (unencrypted).  

The **Real-Time Streaming Protocol** (**RTSP**) is an [application-level](https://en.wikipedia.org/wiki/Application_layer) network [protocol](https://en.wikipedia.org/wiki/Communications_protocol) designed for [multiplexing](https://en.wikipedia.org/wiki/Multiplexing) and [packetizing](https://en.wikipedia.org/wiki/Network_packet#MPEG_packetized_stream) [multimedia](https://en.wikipedia.org/wiki/Multimedia) transport streams (such as [interactive media](https://en.wikipedia.org/wiki/Interactive_media), [video](https://en.wikipedia.org/wiki/Video) and [audio](https://en.wikipedia.org/wiki/Digital_audio)) over a suitable [transport protocol](https://en.wikipedia.org/wiki/Transport_layer). RTSP is used in entertainment and communications systems to control [streaming media](https://en.wikipedia.org/wiki/Streaming_media) [servers](https://en.wikipedia.org/wiki/Web_server). [RealNetworks](https://realnetworks.com/) developed RTSP in 1996, designed to control the entertainment and communication systems in a streaming server RTSP utilizes User Datagram Protocol ([UDP](https://getstream.io/blog/communication-protocols/#understanding-tcp-and-udp)) and Real-time Transport Protocol (RTP). RTSP is the standard [protocol used for streaming video](https://getstream.io/blog/streaming-protocols/) data from IP cameras and supports reliable segmented streaming, enabling users to watch streams while it's still being downloaded. The protocol also provides extensive customization options to help you build your own streaming applications and add new features. The main disadvantage of RTSP is that it isn't widely used for broadcasting multimedia over the Internet.

An example of RTSP in action with the video and audio data being delivered over a separate UDP-based RTP stream is shown below 

![](doc/img/rtsp.gif)

The protocol is used for establishing and controlling media sessions between endpoints. Clients of media servers issue commands such as *play*, *record* and *pause*, to facilitate real-time control of the media streaming from the server to a client ([video on demand](https://en.wikipedia.org/wiki/Video_on_demand)) or from a client to the server. 

Reference 

https://www.informit.com/articles/article.aspx?p=169578&seqNum=3



------

### System Design 

#### Railway OT system station docking  assistant system

The train safety surveillance camera is build by using the raspberry PI3B+ with the camera module. In the real world model, before the railway station under the train slow down distance, there will be 2 thermal reflection sensors which connect to the PLC to detection the train, and next to the sensors, we installed our camera to detect the train. The camera will send the video stream to the video processing computer, our program will use the CV to do the motion and the train object detection.  

The position of the camera and the sensor is shown below:

![](doc/img/surveillanceSysDetail.png)

In the digital twin real world emulator, we did the same config. 

When a train is passing the sensor and camera detection area: 

PLC to convert the sensor electrical signal to digital signal and send to the HMI, HMI will show the train detection result and based on the detection time and train length calculate the train speed (speed-val-1). 

The camera video processing computer's  motion detection program will trigger the train object detection algo to confirm the train is passing, then calculate the train speed (speed-val-2)

If any of the 2 speed value speed-val-1and speed-val-2 is higher than the designed train docking speed, the station control HMI will send the train slow down signal to the train. 

The detail operation scenario is shown below : 

![](doc/img/RM_testRun.gif)

 

#### OT System Surveillance Camera Replay Attack Demo Design 

As shown in the previous Railway OT system station docking  assistant system introduction workflow, there are 2 safety mechanism train motion detection sensor and train object detection camera. For the motion detection sensor which connect to PLC, the red attacker can modify its sensor state via false data injection attack, but for the train object detection camera, it is hard for hacker to modify the byte data in the video stream via man in the middle attack, so the hacker will implement a firmware attack to the camera to open a "backdoor" of the camera, then do the replay attack under below steps: 

- Do a firmware attack to make the video camera runs a modified firmware with backdoor. 
- Red team attacker use the camera back door record a video which only contents the railway without a train pass. 
- When the attacker start the FDI attack on the PLC-HMI part, he also cut off the video steam send from the camera to the train detection camera video process computer , then replay send the pre-saved video recorded in previous step. 

The detail attack flow is shown below:

![](doc/img/attackFlow.png)

By using the FDI attack on the PLC and replay attack on the camera, the red team attack is able to mess up the station docking  assistant system which makes the station HMI and operator not able to detect the docking train to the station.



------

### Program Setup

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

![](doc/img/RM_camera.jpg)



##### Program File List 

| Program File    | Execution Env | Description                                                  |
| --------------- | ------------- | ------------------------------------------------------------ |
| cameraClient.py | python3.7     | This module will create a client program running on raspberry PI to capture the camera image and feed the image back to connected camera server. |
| cameraServer.py | python3.7     | This module will create a camera viewer server to connect to the <camClient> by UDP client, get the camera video and do the motion detection and simple target tracking. |
| pattChecker.py  | python3.7     | This module will create a camera firmware PATT checking function. |
| pattClient.py   | python3.7     | This module create a file PATT check client and feed back the PATT value when the server connect and send address list to it. |
| pattServer.py   | python3.7     | This module will create a PATT file checker program. It will send the PATT bytes check list to the client and compare the feedback PATT value. |
| udpCom.py       | python3.7     | This module will provide a UDP client and server communication API. |
| udpComTest.py   | python3.7     | This module will provide a muti-thread test case program to test  the UDP communication modules by using port 5005. |
| firmwareSample  |               | firmware sample file used in test mode.                      |
| my_video.h264   |               | H264 video used to show the attacked situation.              |



------

### Program Usage/Execution

##### Communication Protocol 

The system use UDP to do the camera video stream control and attestation checkout.

| The camera client+server and the PATT check+verifier will communicate with each other by UDP with different port. |
| ------------------------------------------------------------ |
| Camera client [ UDP server port: 5005]  <= image request <= Camera server [UDP client] |
| Camera client [ UDP server port: 5005]  => encoded image => Camera server [UDP client] |
| PATT checker [ UDP server port: 5006]  <= Random address list <= PATT verifier [UDP client] |
| PATT checker [ UDP server port: 5006]  => cameraClient PATT value => PATT verifier [UDP client] |

**Communication detail diagram is shown below**: 

![](doc/img/RM_comm.png)

##### Run the Program

**Firmware Update Attestation**: In this section we will create a firmware checker and a verifier program to do the firmware attestation by using PATT(Physics-based Attestation of Control Systems) algorithm.  The checker running in Raspberry PI will calculate the camera firmware (camera Client) 's PATT hash value based on the random bytes address send from the verifier. The verifier will compare the firmware's PATT value with its local file's calculation result to give the attestation result. 

Run the program on `Raspberry PI` : 

```
IOT IP camera program: python cameraClient.py
Attestation program checker: python pattClient.py
```

Run the program on `Host Computer` : 

```
IOT camera targets detection program: python cameraServer.py
Attestation program verifier: python pattServer.py
```

The Attestation program verifier will shown result as below: 

![](doc/img/2022-01-29_173826.png)

Detail usage please check the `Usage menu.pdf` in the doc folder. 



------

### Problem and Solution

N.A

------

### Reference

- PATT firmware attestation:  https://www.usenix.org/system/files/raid2019-ghaeini.pdf
- RTSP video protocol: https://www.informit.com/articles/article.aspx?p=169578&seqNum=3
- Replay attack :  https://www.baeldung.com/cs/replay-attacks

------

> Last edit by LiuYuancheng(liu_yuan_cheng@hotmail.com) at 26/03/2020