// Simple I2C test for ebay 128x64 oled.
#include <Arduino.h>
#include <Wire.h>
#include "SSD1306Ascii.h"
#include "SSD1306AsciiWire.h"

// 0X3C+SA0 - 0x3C or 0x3D
#define I2C_ADDRESS 0x3C

// Define proper RST_PIN if required.
#define RST_PIN -1

SSD1306AsciiWire oled;

#include "globals.h"

void init_display() {
    
    Wire.begin();
    Wire.setClock(400000L);

#if RST_PIN >= 0
    oled.begin(&Adafruit128x64, I2C_ADDRESS, RST_PIN);
#else // RST_PIN >= 0
    oled.begin(&Adafruit128x64, I2C_ADDRESS);
#endif // RST_PIN >= 0

    oled.setFont(Adafruit5x7);

}

void print_display() {
    oled.clear();
    oled.set2X();
    oled.print(step);
    oled.print("  C:");
    oled.print(c);
    oled.println(" ");
    oled.set1X();
        // oled.print("C:");
        // oled.print(c);
        // oled.print(" ");
    oled.print("CI:");
    oled.print(ci);
    oled.print(" ");
    oled.print("CO:");
    oled.println(co);
        // oled.print("\t");

    // oled.print("EI:");
    // oled.print(ei);
    // oled.print(" ");
    // oled.print("EO:");
    // oled.print(eo);
    // oled.println(" ");

    // oled.print("LF:");
    // oled.print(lf);
    // oled.print(" ");
    // oled.print("RF:");
    // oled.print(rf);
    // oled.println(" ");

    oled.print("ET:");
    oled.print(et);
    oled.print(" ");
    oled.print("EH:");
    oled.print(eh);
    oled.println(" ");

    oled.print("CT:");
    oled.print(ct);
    oled.print(" ");
    oled.print("CH:");
    oled.print(ch);
    oled.println(" ");
        // oled.println("Hello World!");
}
