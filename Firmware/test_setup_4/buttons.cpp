#include <Arduino.h>
#include "globals.h"

void add_log();


#define pin2 2      // Button pin
#define pin3 3      // Button pin
volatile bool down_pressed = false;
volatile bool up_pressed = false;
volatile unsigned long lastPressTime = 0;
const unsigned long debounceDelay = 500;  // 50ms debounce

#define pin4 4
bool save = true;
#define indicator 5

void init_indicator() {
    pinMode(indicator, OUTPUT);
}

void indicate() {
    digitalWrite(indicator, HIGH);
    delay(1000);
    digitalWrite(indicator, LOW);
}

void check_save() {
    bool save_button = digitalRead(pin4);
    if(save!=save_button) {
        save=save_button;
        if(!(save) && digitalRead(pin2) && digitalRead(pin3)){
            // Serial.println(F("SAVED"));
            add_log();
            indicate();
        }
    }
    // if (save == true && save_button == false) {  // falling edge
    //     Serial.println(F("SAVED"));
    //     add_log();
    //     indicate();
    // }
    // save = save_button;  // update state
}

void down_interrupt(){
    // handleInterrupt(down_pressed);
    unsigned long currentTime = millis();

    // Debounce: check time since last valid press
    if (currentTime - lastPressTime > debounceDelay) {
      down_pressed = true;            // Set flag
      lastPressTime = currentTime;     // Update last press time
    }
    if (down_pressed) {
        down_pressed = false;  // Clear the flag

        // Serial.println(F("1"));

        // Optional: reset speed/step
        // speed = 0;
        // step = 0;
        // analogWrite(compressor_sp, speed);
        // Serial.println(speed);
        // Serial.println(step);

        // Optional function call
        // compressor_speed_canvas();

        if(digitalRead(pin4)) {
            // Serial.print(F("DOWN "));
            if (step > 0) {
                step--;
            }
            // If step reaches 0, set speed to 0
            if (step == 0) {
                speed = 0;
            } 
            else {
                speed = start_speed + step * step_size; // Calculate the speed for the current step
            }
            analogWrite(compressor_sp, (speed & EN));
            delay(100);
            Serial.println(speed);
            // Serial.println(step);
            Serial.println(speed & EN);
        }

        else{
            // Serial.println("Toggle Compressor");
            EN=~EN;
            Serial.println(EN);
            digitalWrite(compressor_en, EN);
        }
    }
}

void up_interrupt(){
    // handleInterrupt(up_pressed);
    unsigned long currentTime = millis();

    // Debounce: check time since last valid press
    if (currentTime - lastPressTime > debounceDelay) {
      up_pressed = true;            // Set flag
      lastPressTime = currentTime;     // Update last press time
    }
    if (up_pressed) {
        up_pressed = false;  // Clear the flag

        // Serial.println(F("2"));

        // Optional: reset speed/step
        // speed = 0;
        // step = 0;
        // analogWrite(compressor_sp, speed);
        // Serial.println(speed);
        // Serial.println(step);

        // Optional function call
        // compressor_speed_canvas();
        if(digitalRead(pin4)) {
            // Serial.print(F("UP "));
            if (step < steps) {
                step++;
            }
            // If step reaches 18, set speed to 255
            if (step == steps) {
                speed = end_speed;
            // } else if(step==1) {
            //     analogWrite(compressor_sp, 100);
            //     delay(2000);
            } else {
                speed = start_speed + step * step_size; // Calculate the speed for the current step
            }
            analogWrite(compressor_sp, (speed & EN));
            Serial.println(speed);
            // Serial.println(step);
            Serial.println(speed & EN);

        } else {
            Serial.println(F("SAVED"));
            add_log();
            indicate();
        }

        // u8g2.setFont(u8g2_font_profont22_tn);	// choose a suitable font
        // // u8g2.drawStr(40,17,"18");	// write something to the internal memory
        // u8g2.setCursor(40, 17);
        // u8g2.print(step);
    }
}

void init_buttons() {
    pinMode(pin2, INPUT_PULLUP);  // Button uses internal pull-up
    attachInterrupt(digitalPinToInterrupt(pin2), down_interrupt, FALLING);
    pinMode(pin3, INPUT_PULLUP);  // Button uses internal pull-up
    attachInterrupt(digitalPinToInterrupt(pin3), up_interrupt, FALLING);

    pinMode(pin4, INPUT_PULLUP);  // Button uses internal pull-up

}