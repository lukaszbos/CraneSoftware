#ifndef JOYSITCK_H
#define JOYSITCK_H
/*
 * This file contains joystick controller methods
 *
 */
 ////JOYSTICK CANT SEE  3

#include <Arduino.h>
#include "Atributtes.h"

class Joystick{
public:
  int getGear(const int analogPin); //returns value read from analog pin

  void setGear(const int analogPin);
private:

};
#endif /* end of include guard: JOYSITCK_H */
