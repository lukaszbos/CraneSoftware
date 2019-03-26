String input ="";
boolean msgComplete=false;

void setup() {
  size(500,500);
}

void draw() {
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

void keyPressed() {
  if(keyCode==UP) {
    msgComplete=true;
  }else{
    input+=key;
  } 
}
