#include <Arduino.h>
#include <SPI.h>
#include <SD.h>

// const int SD_CS = 10;
#define cs_pin 10

void init_sd() {
    if (!SD.begin(cs_pin)) {
        Serial.println("SD initialization failed!");
        // while (1); // Halt here if SD init fails
    }
}

void init_file() {
    String dataString = "---new log---";

    File dataFile = SD.open("logs/f_4.csv", FILE_WRITE);

    // if the file is available, write to it:
    if (dataFile) {
        dataFile.println(dataString);
        dataFile.close();
        // print to the serial port too:
        Serial.println(dataString);
    }
    // if the file isn't open, pop up an error:
    else {
        Serial.println("loop(): error opening datalog.txt");
    }
}

void add_log() {
    String dataString = "";
//              mode spd c    ci   co   pi   po   ei   eo   lf   rf   et   eh   ct   ch
    dataString = "15,255,45.3,25.6,25.6,25.6,25.6,25.6,25.6,25.6,25.6,25.6,25.6,25.6,04.6;";

    File dataFile = SD.open("logs/f_4.csv", FILE_WRITE);

    // if the file is available, write to it:
    if (dataFile) {
        dataFile.println(dataString);
        dataFile.close();
        // print to the serial port too:
        Serial.println(dataString);
    }
    // if the file isn't open, pop up an error:
    else {
        Serial.println("loop(): error opening datalog.txt");
    }
}