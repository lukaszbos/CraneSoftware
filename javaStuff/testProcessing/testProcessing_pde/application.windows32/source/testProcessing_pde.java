import processing.core.*; 
import processing.data.*; 
import processing.event.*; 
import processing.opengl.*; 

import java.util.HashMap; 
import java.util.ArrayList; 
import java.io.File; 
import java.io.BufferedReader; 
import java.io.PrintWriter; 
import java.io.InputStream; 
import java.io.OutputStream; 
import java.io.IOException; 

public class testProcessing_pde extends PApplet {

String input ="";
boolean msgComplete=false;

public void setup() {
  
}

public void draw() {
  background(0);
  stroke(255);
  fill(255);

  text(input,100,100);
  if(msgComplete) {
    /*do here what you want to do with input-message*/
    input="Input";
    msgComplete=false;
  } 
}

public void keyPressed() {
  if(keyCode==UP) {
    msgComplete=true;
  }else{
    input+=key;
  } 
}
  public void settings() {  size(500,500); }
  static public void main(String[] passedArgs) {
    String[] appletArgs = new String[] { "--present", "--window-color=#666666", "--stop-color=#cccccc", "testProcessing_pde" };
    if (passedArgs != null) {
      PApplet.main(concat(appletArgs, passedArgs));
    } else {
      PApplet.main(appletArgs);
    }
  }
}
