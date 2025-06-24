#include "globals.h"

void init_compressor() {
    // pinMode(compressor_en,OUTPUT);
    // digitalWrite(compressor_en, EN);
    speed = 0;
    step = 0;
    analogWrite(compressor_sp, (speed & EN));
}


void safety_check() {
    if(c>32) {
        // speed = 0;
        // step = 0;
        init_compressor();
        // WARNING_FLAG=true;
    }
    else{
        // WARNING_FLAG=false;
    }
}