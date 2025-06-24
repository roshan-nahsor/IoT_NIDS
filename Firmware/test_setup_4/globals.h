// #ifndef Adruino_H
#include <Arduino.h>


#ifndef GLOBALS_H
#define GLOBALS_H

#define compressor_sp 9
#define compressor_en 7
inline uint8_t EN = 0;

#define start_speed 75
#define end_speed 255
#define steps 18
#define step_size ((end_speed - start_speed) / (steps - 1))

// Declare variables as `inline` to avoid multiple definition errors
inline uint8_t speed = 0;
inline uint8_t step = 0;

inline float c, ci, co, ei, eo, lf, rf, et, eh, ct, ch, pi, po;

inline bool c_en;

inline bool WARNING_FLAG=false;

#endif
