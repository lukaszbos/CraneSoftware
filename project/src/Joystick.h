#ifndef JOYSITCK_H
#define JOYSITCK_H
/*
 * This file contains joystick controller methods
 *
 */
 ////JOYSTICK CANT SEE  3

#include <Arduino.h>
#include "atributtes.h"

int sensorValue;
int outputValue;

int getGear(const int analogPin); //returns value read from analog pin

#endif /* end of include guard: JOYSITCK_H */
