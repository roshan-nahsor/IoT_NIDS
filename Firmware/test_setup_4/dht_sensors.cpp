#include "globals.h"
#include "DHT.h"
#define evaporator_pin 14     // Digital pin connected to the DHT sensor
#define coat_pin 15     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22   // DHT 11
DHT evaporator(evaporator_pin, DHTTYPE);
DHT coat(coat_pin, DHTTYPE);


void init_dht_sensors() {
    // Serial.println(F("DHTxx test!"));

    evaporator.begin();
    coat.begin();
}

void get_dht_values() {
    eh = evaporator.readHumidity();
    et = evaporator.readTemperature();
    
    ch = coat.readHumidity();
    ct = coat.readTemperature();

        // Serial.println(et);
        // Serial.println(eh);
        // Serial.println(ct);
        // Serial.println(ct);
}