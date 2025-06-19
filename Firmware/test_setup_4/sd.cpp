#include "globals.h"

#include <Arduino.h>
#include <SPI.h>
#include <SD.h>

// const int SD_CS = 10;
#define cs_pin 10

#define file_location "logs/f_5.csv"

void init_sd() {
    if (!SD.begin(cs_pin)) {
        Serial.println(F("SD initialization failed!"));
            // while (1); // Halt here if SD init fails
    }
}

void init_file() {
    // String dataString = "---new log---";
    String dataString = "step,speed,c,ci,co,pi,po,ei,eo,lf,rf,et,eh,ct,ch;";

    File dataFile = SD.open(file_location, FILE_WRITE);

        // if the file is available, write to it:
    if (dataFile) {
        dataFile.println(dataString);
        dataFile.close();
            // print to the serial port too:
        // Serial.println(dataString);
    }
        // if the file isn't open, pop up an error:
    else {
        Serial.println(F("loop(): error opening datalog.txt"));
    }
}

void add_log() {
    String dataString = "";
//              mode spd c    ci   co   pi   po   ei   eo   lf   rf   et   eh   ct   ch
    // dataString = "15,255,45.3,25.6,25.6,25.6,25.6,25.6,25.6,25.6,25.6,25.6,25.6,25.6,14.6;";

    dataString =    String(step)+","+
                    String(speed)+","+
                    String(c)+","+
                    String(ci)+","+
                    String(co)+","+
                    String(pi)+","+
                    String(po)+","+
                    String(ei)+","+
                    String(eo)+","+
                    String(lf)+","+
                    String(rf)+","+
                    String(et)+","+
                    String(eh)+","+
                    String(ct)+","+
                    String(ch)+";";


    File dataFile = SD.open(file_location, FILE_WRITE);

    // if the file is available, write to it:
    if (dataFile) {
        dataFile.println(dataString);
        dataFile.close();
        // print to the serial port too:
        // Serial.println(dataString);
    }
    // if the file isn't open, pop up an error:
    else {
        Serial.println(F("loop(): error opening datalog.txt"));
    }
}