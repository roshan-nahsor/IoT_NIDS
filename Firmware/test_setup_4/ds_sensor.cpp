#include "globals.h"

#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 8
#define TEMPERATURE_PRECISION 9

OneWire oneWire(ONE_WIRE_BUS);

DallasTemperature sensors(&oneWire);

DeviceAddress EI = { 0x28, 0x30, 0xCD, 0x35, 0x00, 0x00, 0x00, 0xF4 };
DeviceAddress C = { 0x28, 0xE2, 0x63, 0x6A, 0x00, 0x00, 0x00, 0x8D };
DeviceAddress CO = { 0x28, 0x97, 0x22, 0x88, 0x00, 0x00, 0x00, 0x94 };
DeviceAddress EO = { 0x28, 0xEE, 0xFD, 0x5A, 0x00, 0x00, 0x00, 0xAD };
DeviceAddress CI = { 0x28, 0x03, 0xE0, 0x94, 0x00, 0x00, 0x00, 0x72 };
DeviceAddress LF = { 0x28, 0xE1, 0x68, 0x56, 0x00, 0x00, 0x00, 0xFE };
DeviceAddress RF = { 0x28, 0xC2, 0xF5, 0x33, 0x00, 0x00, 0x00, 0x5B };
// DeviceAddress CT = { 0x28, 0xAB, 0xEB, 0x87, 0x00, 0x00, 0x00, 0x4F };

// function to print a device address
void printAddress(DeviceAddress deviceAddress) {
    for (uint8_t i = 0; i < 8; i++) {
            // zero pad the address if necessary
        if (deviceAddress[i] < 16) Serial.print("0");
        Serial.print(deviceAddress[i], HEX);
    }
}

void print_ds_value(DeviceAddress deviceAddress) {
    Serial.print(F("Device Address: "));
    printAddress(deviceAddress);
    Serial.print(F(" "));
        // Serial.println(get_ds_value(deviceAddress));
}

float get_ds_value(DeviceAddress deviceAddress) {
    float tempC = sensors.getTempC(deviceAddress);
    if (tempC == DEVICE_DISCONNECTED_C) {
        //   Serial.print(F("Error: Could not read temperature data"));
      return 0;
    }

        // print_ds_value(deviceAddress);
        // Serial.println(tempC);

    return tempC;
}






void init_ds_sensors() {
    sensors.begin();
    // Serial.println(F("Dallas Temperature IC Control Library Demo"));
}

void report_parasite_power () {
    // report parasite power requirements
    Serial.print(F("Parasite power is: "));
    if (sensors.isParasitePowerMode()) Serial.println(F("ON"));
    else Serial.println("OFF");
}

// void

void locate_ds_sensors() {
    // locate devices on the bus
    Serial.print(F("Locating devices..."));
    Serial.print(F("Found "));
    Serial.print(sensors.getDeviceCount(), DEC);
    Serial.println(F(" devices."));

    
    // Search for devices on the bus and assign based on an index. Ideally,
    // you would do this to initially discover addresses on the bus and then
    // use those addresses and manually assign them (see above) once you know
    // the devices on your bus (and assuming they don't change).
    
    // method 1: by index
    // if (!sensors.getAddress(C, 0)) Serial.println(F("Unable to find address for Device 0"));h


    Serial.print(F("Device 0 Address: "));
    printAddress(LF);
    Serial.println();

    Serial.print(F("Device 1 Address: "));
    printAddress(RF);
    Serial.println();
}

void print_ds_resolution() {
    Serial.print(F("Device 0 Resolution: "));
    Serial.print(sensors.getResolution(LF), DEC);
    Serial.println();

    Serial.print(F("Device 1 Resolution: "));
    Serial.print(sensors.getResolution(RF), DEC);
    Serial.println();
}

void set_ds_resolution() {
    // set the resolution to 9 bit per device
    sensors.setResolution(C, TEMPERATURE_PRECISION);
    sensors.setResolution(CI, TEMPERATURE_PRECISION);
    sensors.setResolution(CO, TEMPERATURE_PRECISION);
    sensors.setResolution(EI, TEMPERATURE_PRECISION);
    sensors.setResolution(EO, TEMPERATURE_PRECISION);

    sensors.setResolution(LF, TEMPERATURE_PRECISION);
    sensors.setResolution(RF, TEMPERATURE_PRECISION);
    // sensors.setResolution(CT, TEMPERATURE_PRECISION);

    // print_ds_resolution();
}

void request_ds_values() {
    // call sensors.requestTemperatures() to issue a global temperature
    // request to all devices on the bus
    // Serial.print(F("Requesting temperatures..."));
    sensors.requestTemperatures();
    delay(750);
    // Serial.println(F("DONE"));
}


void assign_ds_values() {
    c=get_ds_value(C);
    ci=get_ds_value(CI);
    co=get_ds_value(CO);
    
    ei=get_ds_value(EI);
    eo=get_ds_value(EO);

    lf=get_ds_value(LF);
    rf=get_ds_value(RF);
}