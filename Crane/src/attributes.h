// Arduino Nano pin connections. These you can rewire freely. Each TMC2130 needs its own pins.
// To reduce the number of pins needed, i have wired EN and DIR to GND.
#define EN_PIN    0xFFFF  //enable (CFG6). I want driver always enabled, so connect EN --> GND
#define DIR_PIN   0xFFFF //direction can also be controlled through SPI, so connect DIR --> GND
#define STEP_PIN  3   //step
#define CS_PIN    2   //chip select

#define HALL_PIN  A7 //Hall-effect sensor pin
#define JIB_JOYSTICK_PIN A0
//it s becouse of c++
