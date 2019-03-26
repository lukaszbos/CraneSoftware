import processing.core.PApplet;

public class Main extends PApplet {

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
        String[] appletArgs = new String[] { "--present", "--window-color=#666666", "--stop-color=#cccccc", "Main" };
        if (passedArgs != null) {
            PApplet.main(concat(appletArgs, passedArgs));
        } else {
            PApplet.main(appletArgs);
        }
    }
}