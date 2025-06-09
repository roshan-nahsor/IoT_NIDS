// #include <U8g2lib.h>
// #include <Wire.h>
// #include <SPI.h>
// #include <SD.h>

// #include "sd.cpp"



// Use 1-byte page buffer mode for low RAM on Nano
// U8G2_SSD1306_128X64_NONAME_1_HW_I2C u8g2(U8G2_R0, U8X8_PIN_NONE);

// U8X8_SSD1306_128X64_NONAME_HW_I2C u8x8(/* reset=*/ U8X8_PIN_NONE);      
// U8X8_SH1107_64X128_SW_I2C u8x8(/* reset=*/ U8X8_PIN_NONE);      


void init_sd();
void init_file();
void add_log();

void init_display();
void print_display();

void init_buttons();
void check_save();

void setup() {
    Serial.begin(9600);
    delay(500);


  // Serial.println("Starting...");

  // Init SPI bus early
  // SPI.begin();

  // Setup SD_CS pin as output and deselect SD card
  // pinMode(SD_CS, OUTPUT);
  // digitalWrite(SD_CS, HIGH);

  // Serial.println("Initializing SD card...");
//   if (!SD.begin(SD_CS)) {
//     Serial.println("SD initialization failed!");
//     // while (1); // Halt here if SD init fails
//   }
  // Serial.println("SD initialized successfully.");
    init_sd();

    // String dataString = "---new log---";

    // File dataFile = SD.open("logs/f_4.csv", FILE_WRITE);

    // // if the file is available, write to it:
    // if (dataFile) {
    //     dataFile.println(dataString);
    //     dataFile.close();
    //     // print to the serial port too:
    //     Serial.println(dataString);
    // }
    // // if the file isn't open, pop up an error:
    // else {
    //     Serial.println("loop(): error opening datalog.txt");
    // }
    init_file();

  // Init I2C and OLED display
  // Wire.begin();
//   u8g2.begin();

  // Display startup message
//   u8g2.firstPage();
//   do {
//     u8g2.setFont(u8g2_font_6x10_tr);
//     u8g2.drawStr(0, 15, "SD + OLED working");
//   } while (u8g2.nextPage());

    // u8x8.begin();
    // u8x8.setPowerSave(0);
    init_display();
    init_buttons();
}

void loop() {
  // Display running time on OLED
//   u8g2.firstPage();
//   do {
//     u8g2.setCursor(0, 20);
//     u8g2.print("Time: ");
//     u8g2.print(millis() / 1000);
//     u8g2.print(" s");
//   } while (u8g2.nextPage());

    // u8x8.setFont(u8g2_font_doomalpha04_tr);	// choose a suitable font

    // u8x8.setFont(u8x8_font_chroma48medium8_r);
    // u8x8.setCursor(0,1);
    // u8x8.print("Hello World!");
    // // u8x8.drawString(0,1,"Hello World!");
    // // u8x8.setInverseFont(1);
    // u8x8.setCursor(0,0);
    // // u8x8.print("Hello World!");
    // u8x8.print("0123456789");
    // u8x8.setInverseFont(0);
    //u8x8.drawString(0,8,"Line 8");
    //u8x8.drawString(0,9,"Line 9");
    // u8x8.refreshDisplay();		// only required for SSD1606/7  
    // delay(2000);

    print_display();
    delay(1000);

    check_save();

    add_log();
}
