#include <Adafruit_GFX.h>    // Core graphics library
#include <MCUFRIEND_kbv.h>   // Hardware-specific library
MCUFRIEND_kbv tft;

#include <Fonts/FreeSans9pt7b.h>
#include <Fonts/FreeSans12pt7b.h>
#include <Fonts/FreeSerif12pt7b.h>

#include <FreeDefaultFonts.h>

#define BLACK   0x0000
#define RED     0xF800
#define GREEN   0x07E0
#define WHITE   0xFFFF
#define GREY    0x8410

#define RES_W 480
#define RES_H 320




void setup()
{
  tft.reset();
  Serial.begin(115200);
  uint16_t ID = tft.readID();
  if (ID == 0xD3) ID = 0x9481;
  tft.begin(ID);
  tft.setRotation(3);
  tft.fillScreen(BLACK);   
    
}

//char com[7];
//int sa;
String command;
String value;
void loop()
{
  if(Serial.available()>0){
    command = Serial.readStringUntil(':');
    Serial.print("command : ");
    Serial.println(command);
    value = Serial.readStringUntil('\r\n');
    Serial.print("value : ");
    Serial.println(value);
    if (command=="track"){
      playerTrack(value);
    }
    if (command=="title"){
      playerTitle(value);
    }  
    
  }
  
//  delay(200);
}

void playerTrack(String str){
//  positition at 20,30
  tft.fillRect(10,10,50,50,BLACK);
  tft.setFont(&FreeSerif12pt7b);
  tft.setCursor(20, 30);
  tft.setTextColor(WHITE);
  tft.setTextSize(1.5);
  tft.print(str);
//  delay(200);
}

void playerTitle(String str){
//  posisition at 50,30
  tft.fillRect(50,10,400,50,BLACK);
  tft.setFont(&FreeSerif12pt7b);
  tft.setCursor(70, 30);
  tft.setTextColor(WHITE);
  tft.setTextSize(1.5);
  tft.print(str);
//  delay(200);
}

void label(String str)
{
  //erase label
//  tft.drawRect(150,40,300,30,RED);
  tft.fillRect(150,50,300,30,BLACK);
  tft.setFont(&FreeSerif12pt7b);
  tft.setCursor(150, 70);
  tft.setTextColor(GREEN);
  tft.setTextSize(1);
  tft.print(str);
//    delay(100);
}


void text(int x, int y, int sz, const GFXfont *f, const char *msg)
{
//    int16_t x1, y1;
//    uint16_t wid, ht;
//    tft.drawFastHLine(0, y, tft.width(), WHITE);
  tft.setFont(f);
  tft.setCursor(x, y);
  tft.setTextColor(WHITE);
  tft.setTextSize(sz);
  tft.print(msg);
//    delay(100);
}

