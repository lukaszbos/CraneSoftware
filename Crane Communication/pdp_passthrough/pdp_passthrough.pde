//HI! This sketch does the following: It reads the serial stream, and each time it finds a message starting char 'S', it checks if there is a valid message arriving.
//Valid message in this sketch is S,0,0,0,0,0,0,00,E
//where first S is start char, next 6 numbers represents the movements in order: turn CCW, turn CW, Trolley Forward, Trolley backward, Hook up, Hook down. They are separated by ','-sign.
//each of the movement numbers can have value 0-3, where 0 = no movement, 1=slow movement, 2=med movement, 3=full speed. You are free to adjust those. Last double-zeros at the end
//is a very simple checksum. You just use it to verify that the message is unchanged in serial communication. You can choose whatevery method You like or make your own. Idea is just to build a
//unique 'verification code' to compare the rest of the message with.

//Suppose You send a message S,1,0,2,0,0,1,00,E from arduino mega to PC. That would mean: turn slowly CCW & mid-move trolley forward & slowly lower the hook. 

import processing.serial.*;
import processing.net.*;

//This blok includes the variables You need to set up. Adding more cranes is simple: You just need to create new similar instances to other cranes.
String srPort = "COM8";             // just set this to match the port connected to your arduino with pads. Later on, it is of course possible to make a method that just scans all the ports.
int baudRate = 115200;               // set this to match Your pad-arduino baudrate
//String craneIP1 = "192.168.1.177";     // what is the IP address of your first crane You want to communicate with?
String craneIP1 = "192.168.0.101";

int cranePort1 = 80;               // how about port? This is not COM port, but a IP network service port. You can set it up in arduino sketch.
  

Serial serial;
Client client;

boolean srConnected = false;
boolean craneConnected = false;

void setup(){
  size(600,600);
  serial = new Serial(this,srPort,baudRate);
  client = new Client(this,craneIP1,cranePort1);        //  COMMENT THIS LINE OUT IF YOU DONT WANT TO SEND ANYTHING, JUST PRINT

}

//draw-method gets called over and over again, just like loop() in arduino. Basically it gathers a input-string from serial port stream,
//starting with char 'S', and then passes the whole command string unchanged to craneIP1 address and port cranePort1, as spesified above.
//if You want to simulate Anti-collision,You can just edit the command before you pass it to send-method.

void draw(){
  background(0);   //background color of window, 0 = black
  textSize(20);
  fill(255);        //text color, 255=white
  if(!srConnected) {
    text("Connected serial port: "+srPort,50,200);
  }
  if(!craneConnected) {
    text("Connected IP server: "+craneIP1+" : "+cranePort1,50,300);
  }
  
  String input = "";
  if(serial.available()>0){       //there should be at least 18 chars in serial buffer
    char c = (char) serial.read();
    if(c=='S'){
      input += 'S';
      for(int i=0; i<17;i+=1){
        input += (char) serial.read();
      }
    }
    if(messageOk(input)){        //messageOk-method is for Your possible checksum-implementation. For now it just returns true so every message will be passed. You should have check for good message
      println(input);              //prints received message
      send(input,1);               //COMMENT THIS LINE OUT IF YOU ONLY WANT TO PRINT MESSAGES, NOT SEND THEM FORWARD
    }
  }
}

//sending method. It is a separate method so it is easy for you to send to multiple targets.
void send(String msg, int toWho){
  if(toWho==1){
    try{
      client.write(msg);
      println("message sent to arduino" );
    } catch(Exception e){
      println("nie udalo sie wyslac wiadomosci do klienta");
    }
  }
}

//method to check if message is valid. I.E. it has correct length, order and maybe that checksum is ok. 
boolean messageOk(String input){ 
  //text(input, 50 ,200);
  //println("message ok");
  return true;
}
