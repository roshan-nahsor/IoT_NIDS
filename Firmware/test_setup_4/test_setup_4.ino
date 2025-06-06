#include <U8g2lib.h>
#include <Wire.h>
#include <SPI.h>
#include <SD.h>

// Use 1-byte page buffer mode for low RAM on Nano
U8G2_SSD1306_128X64_NONAME_1_HW_I2C u8g2(U8G2_R0, U8X8_PIN_NONE);

const int SD_CS = 10;

void setup() {
  Serial.begin(9600);
  delay(500);
  Serial.println("Starting...");

  // Init SPI bus early
  SPI.begin();

  // Setup SD_CS pin as output and deselect SD card
  pinMode(SD_CS, OUTPUT);
  digitalWrite(SD_CS, HIGH);

  Serial.println("Initializing SD card...");
  if (!SD.begin(SD_CS)) {
    Serial.println("SD initialization failed!");
    while (1); // Halt here if SD init fails
  }
  Serial.println("SD initialized successfully.");

  // Init I2C and OLED display
  Wire.begin();
  u8g2.begin();

  // Display startup message
  u8g2.firstPage();
  do {
    u8g2.setFont(u8g2_font_6x10_tr);
    u8g2.drawStr(0, 15, "SD + OLED working");
  } while (u8g2.nextPage());
}

void loop() {
  // Display running time on OLED
  u8g2.firstPage();
  do {
    u8g2.setCursor(0, 20);
    u8g2.print("Time: ");
    u8g2.print(millis() / 1000);
    u8g2.print(" s");
  } while (u8g2.nextPage());

  delay(1000);

  String dataString = "";
    dataString =    "step,speed,c;";

    File dataFile = SD.open("logs/f_2.csv", FILE_WRITE);

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
