# GibCrane 
## Quick GibCrane Usage guide

#### Requirements

Python version: python3.7 
> _GibCrane wont work with earlier versions of Python so that is quite necessary thing to have_

Necessary modules:
- pygame
   
#### Usage and configuration

Very importat thing for configuration of testbed, is to have correct ip adresses (and ports) both in GibCrane python code, and arduino code. That's why, each time arduino is uploaded with new code, it is necessary to change ip for each crane. In case 2 or more cranes have same IP, they will be controlled with one controller. Last number of ip address matches number of a crane. Each arduino has it's ip and port hardcoded in following lines in file [jib.ino](https://github.com/lukaszbos/CraneSoftware/blob/jib/jib/jib.ino).
```cpp

#include <EthernetUdp.h>
IPAddress ip_server(192, 168, 0, 102);
word localPort = 10000; // local port to listen on

```
Next part of configuration is checking list of ip adresses in [GibCrane.py](https://github.com/lukaszbos/CraneSoftware/blob/MageCodeReadableAgain/GibCraneFinal/GibCrane.py). 

```python

#  Chosen port used for local communication, and list of IP adresses hardcoded in arduino
PORT = 10000
listOfIpAddresses = ['192.168.0.171', '192.168.0.173', '192.168.0.172', '192.168.0.174']

```
When it comes to Game-pad connection, first pad connected to the computer will controll crane with first ip addresses on list. That means that if you want to use only 2 cranes, their ip should be placed on position 0 and 1 in listOfIpAddresses


**_______________________________________________________________________________________________________________________**

update on branches
Hi. I created jib branch.



Usefull stuff (download is probably necessary):
    geographic lib for python, quite crucial IMO:: https://geographiclib.sourceforge.io/1.49/python/code.html 

    project of UDP multithread Server client:: https://gist.github.com/arthurafarias/7258a2b83433dfda013f1954aaecd50a


Hey Mateusz here. 
In the begining, sorry for my english ^^
GitHub is pretty simple once you get a hang of it.

Let's start from branches as they are quite intuitive  (at least in my opinion)

Basically you have:
    master - which is code ready for using, and only ready programs and features should be uploaded to master 

    Developement - splits from master, all code under current developement is stored there. also, it should be only branch that is being merged to master.
    every feature branch splits from dev, ad merges to it

    feature branches - eq. featureDos in our project. Last week together with lukasz, we have cleaned our code a bit, so we have deleted unnecessary branches.


okay, now some theory.
Basic idea of using branches is all about writting all new features in separate branches. 
This way, if yout accidentally mess something up, you will not break working code. And when you are 
sure that your code is working correctly, you are merging your feature branch, into developement branch.

As an example you can look at our current project. In master branch, you can see that the README.md file is 
almost empty, and in developement you can read what you are reading :P And it will stay this way, unless one of us will 
merge it into master branch.
It works in the same way with every other branch. You can enter either one, and then split new branch from it. 
And again, this new branch will contain exact same code as branch you are splitting it from, in the moment of split.

For example, right now, im developing new gpsSimulator program. When I'm writting this tutorial, i did't yet split new branch from Developement.
But i will do it just after i finish. Then i will update changes to this branch, and you won't be able to see them from Developement branch. but if i merge these two, 
all changes will be added to Developement. 

Now, you have added changes to pad.py and somthing to arduino soft. Now you should create new branch, called for example craneControllDev (that's only suggestiong :D ). 
New branch will contain all code untill the moment of creating it, but all changes will be held separately. Now if you finish adding any changes, 
you should commit changes you included, and then if code has no major errors, push the branch to repository. After that will be able to use your code from your branch, 
but it will not change anything in Developement unless you merge. 

If it would happen, that me or lukasz also have changes something 
in the same file you have modified, and we would do it in separate branch, we would be able to see both changes without messing with your
work. Then you could merge you changes into Developement branch, and if somebody wyould like to also merge his changes in the same file,
github would detect conflicts in version, and help to merge 2 versions of same file into one. 
That's basically why git repositories are also called Version Controll Tools



TLDR:   You should only upload unfinished code into separate branch, commit all changes regulary to it, and merge when something is ready to use, 
when one of us will need using your code, or you will need using ours. If merging informs you about any conflicts, you should consult it with person that also has been 
developing coflicting file, to avoid deleting something usefull.  

Ok, I hope it will help you.

Here is tutorial, how to create new branch, 
    https://help.github.com/en/articles/creating-and-deleting-branches-within-your-repository

You don't have to learn using git from linux terminal (or windows cmd / powershell). It is possible to do everything either on github website,
or using any of desktop git client applications. I personally recommend GitKraken, as it is easy to use, does not require using commands at all, 
and looks cool :P Also it uses great way to visualise project developement flow, and in my opinion it actually helps to get better idea of what 
was happening in the project so far. Here is link for GitKraken: 
    https://www.gitkraken.com 
of course it's free to use :P 
