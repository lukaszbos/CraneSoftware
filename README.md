# GibCrane 
## Quick GibCrane Usage guide

#### Requirements

Python version: python3.6
> _GibCrane wont work with earlier versions of Python so that is quite necessary thing to have_

Necessary modules:
- [pygame](https://www.pygame.org/news)

Potentially usefull:
- [Geographic lib](https://geographiclib.sourceforge.io/1.49/python/code.html) for python. Might be usefull for converting       data from cranes into geographical coordinates. Unfortunately, we did not manage to make this part work on time.

#### Usage and configuration

Very importat thing for configuration of testbed is to have correct ip adresses (and ports) both in GibCrane python code and arduino code. That's why each time arduino is uploaded with new code, it is necessary to either change ip for each crane or use value ***myIP*** as last significant bit of IP (it is saved in each crane arduino EPROM memory). In case 2 or more cranes have same IP, they will be controlled with one controller. Last number of ip address matches number of a crane. Each arduino has it's ip and port hardcoded in following lines in file [functions.ino](https://github.com/lukaszbos/CraneSoftware/blob/jib/jib/functions.ino).

```cpp

Ethernet.init(10);   // Ethernet shield CS pin
//EEPROM.update(0,174);
const byte myIP=EEPROM.read(0);
if(myIP==171) led.updateLength(47); // because jib number one has more leds
IPAddress ip(192, 168, 0, myIP);
byte mac[] = {0xA3, 0xAD, 0xBE, 0x16, 0x47, myIP};
Ethernet.begin(mac, ip);

```
Next part of configuration is checking list of ip adresses in [GibCrane.py](https://github.com/lukaszbos/CraneSoftware/blob/MageCodeReadableAgain/GibCraneFinal/GibCrane.py). 

```python

#  Chosen port used for local communication, and list of IP adresses hardcoded in arduino
PORT = 10000
listOfIpAddresses = ['192.168.0.171', '192.168.0.173', '192.168.0.172', '192.168.0.174']

```
When it comes to Game-pad connection, first pad connected to the computer will controll crane with first ip addresses on list. That means that if you want to use only 2 cranes, their ip should be placed on position 0 and 1 in listOfIpAddresses

#### How to run it

To run program on Linux, it is one has be in project directory and run following command:
```bash
python3.6 GibCrane.py
```
We have decided not to generate any .exe files because you will probably modify it anyway. 

## Some info about the code structure

All files are as clean as we managed to make them so it should be pretty easy to understand what is going on in them just from *names* and comments. That's why all I'm going to include here, will be short descriptio of what is where and what should it do:
- [GibCrane.py](https://github.com/lukaszbos/CraneSoftware/blob/MageCodeReadableAgain/GibCraneFinal/GibCrane.py): main class     of program. It creates and manages all threads and connection between UDP clients 
    As program includes Threading module, in classes: Crane client, and PadClient, method run() is one that actually 
    is being run as thread. 
- [CraneClient.py](https://github.com/lukaszbos/CraneSoftware/blob/MageCodeReadableAgain/GibCraneFinal/CraneClient.py): Crane client thread object is defined here. It handles all calculations 
    that happen after getting data from cranes.
- [SupportThreads.py](https://github.com/lukaszbos/CraneSoftware/blob/MageCodeReadableAgain/GibCraneFinal/SupportThreads.py): File contains           definitions of 2 essential methods running as separate threads:
    - communicateThreads - thread handling communication between threads
    - loggingThreadFunction - thread responsible for logging information about status of all running threads
- [PadClient.py](https://github.com/lukaszbos/CraneSoftware/blob/MageCodeReadableAgain/GibCraneFinal/PadClient.py): it           contains definition of PadClient() class. It is responsible for handling getting information from 
    game-pads, and adding commands from each pad to pad command queue    
- [GpsObjects.py](https://github.com/lukaszbos/CraneSoftware/blob/MageCodeReadableAgain/GibCraneFinal/GpsObjects.py):  File     containing classes later used for coordinates calculation

**____________________________________________________________________________________________________________________________________________________________________________________________________**


Usefull stuff (download is probably necessary):
    geographic lib for python, quite crucial IMO:: https://geographiclib.sourceforge.io/1.49/python/code.html 

    project of UDP multithread Server client:: https://gist.github.com/arthurafarias/7258a2b83433dfda013f1954aaecd50a


