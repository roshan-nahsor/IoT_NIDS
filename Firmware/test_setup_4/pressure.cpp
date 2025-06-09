#include "globals.h"
#include <Arduino.h>

#define pi_pin A6
#define po_pin A7

#define sensorMinV  0.5    // Voltage at 0 bar
#define sensorMaxV  4.5    // Voltage at 30 bar
#define pressureMax 30.0  // Max pressure in bar

float pressure_value(uint8_t analog_pin) {
    int analog_value = analogRead(analog_pin);
    delay(100);

        // Serial.println(analog_value);

    float voltage = analog_value * (5.0 / 1023.0);

    float pressure = (voltage - sensorMinV) * (pressureMax / (sensorMaxV - sensorMinV));

    if (pressure < 0) pressure = 0;

    return pressure;
}

void get_pressure() {
    pi=pressure_value(pi_pin);
    po=pressure_value(po_pin);
}