#ifndef WAVE_GENERATOR_H
#define WAVE_GENERATOR_H

#include <Arduino.h>

// Declarações
void setupPWM(int pin, int channel, int resolution);
void setPWM(int channel, int freq, int duty);

#endif // WAVE_GENERATOR_H