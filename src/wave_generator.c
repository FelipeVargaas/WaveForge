#include "wave_generator.h"

// Configura o PWM em um pino e canal específico
void setupPWM(int pin, int channel, int resolution) {
    ledcAttachPin(pin, channel);          // Associa o canal ao pino
    ledcSetup(channel, 5000, resolution); // Configura frequência inicial de 5 kHz e resolução
}

// Configura frequência e duty cycle para o canal
void setPWM(int channel, int freq, int duty) {
    ledcSetup(channel, freq, 8); // Configura nova frequência
    ledcWrite(channel, duty);    // Define o duty cycle
}