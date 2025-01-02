#include <Arduino.h>
#include "global.h"
#include "pins.h"
#include "wave_generator.h"
#include <BluetoothSerial.h> // Biblioteca para Bluetooth        

BluetoothSerial SerialBT; // Objeto para Bluetooth
#define PWM_RESOLUTION 8 // Resolução de 8 bits (0-255)
void processCommand(const String &command);
String receivedCommand;   // String para armazenar o comando recebido


void setup() {
  Serial.begin(115200);  // Inicializa o Serial para debugging
  SerialBT.begin("WaveForge"); // Nome do dispositivo Bluetooth

  // Configuração do PWM
  setupPWM(PIN_RPM, CHANNEL_RPM, PWM_RESOLUTION);
  setupPWM(PIN_INJECTOR_A, CHANNEL_INJECTOR_A, PWM_RESOLUTION);
  setupPWM(PIN_INJECTOR_B, CHANNEL_INJECTOR_B, PWM_RESOLUTION);
  setupPWM(PIN_INJECTOR_C, CHANNEL_INJECTOR_C, PWM_RESOLUTION);
  setupPWM(PIN_INJECTOR_D, CHANNEL_INJECTOR_D, PWM_RESOLUTION);
  setupPWM(PIN_MANOMETER, CHANNEL_MANOMETER, PWM_RESOLUTION);
  setupPWM(PIN_MAP_REDUCTOR, CHANNEL_MAP_REDUCTOR, PWM_RESOLUTION);
  setupPWM(PIN_MAP_COLECTOR, CHANNEL_MAP_COLECTOR, PWM_RESOLUTION);
  setupPWM(PIN_TEMP_GNV, CHANNEL_TEMP_GNV, PWM_RESOLUTION);
  setupPWM(PIN_HPS, CHANNEL_HPS, PWM_RESOLUTION);
  setupPWM(PIN_LPS, CHANNEL_LPS, PWM_RESOLUTION);

  // Setando como saida
  pinMode(PIN_RPM, OUTPUT);
  pinMode(PIN_INJECTOR_A, OUTPUT);
  pinMode(PIN_INJECTOR_B, OUTPUT);
  pinMode(PIN_INJECTOR_C, OUTPUT);
  pinMode(PIN_INJECTOR_D, OUTPUT);
  pinMode(PIN_MANOMETER, OUTPUT);
  pinMode(PIN_MAP_REDUCTOR, OUTPUT);
  pinMode(PIN_MAP_COLECTOR, OUTPUT);
  pinMode(PIN_TEMP_GNV, OUTPUT);
  pinMode(PIN_HPS, OUTPUT);
  pinMode(PIN_LPS, OUTPUT);
}

void loop() {
  // Verifica se há comandos recebidos via Bluetooth
  if (SerialBT.available()) {
    char incomingChar = SerialBT.read();
    if (incomingChar == '\n') {
      processCommand(receivedCommand); // Processa o comando completo
      receivedCommand = "";            // Limpa a string
    } else {
      receivedCommand += incomingChar; // Adiciona o caractere recebido
    }
  }
  delay(50); // Pequeno delay para evitar uso excessivo de CPU
}

// Função para processar os comandos recebidos via Bluetooth
void processCommand(const String &command) {
  int channel, freq, duty;
  if (sscanf(command.c_str(), "%d,%d,%d", &channel, &freq, &duty) == 3) {
    setPWM(channel, freq, duty);
    SerialBT.printf("Channel: %d, Frequency: %d Hz, Duty: %d%%\n", channel, freq, duty);
  } else {
    SerialBT.println("Invalid command. Use format: channel,freq,duty");
  }
}