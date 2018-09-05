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
  Serial.begin(9600);
  uint16_t ID = tft.readID();
  if (ID == 0xD3) ID = 0x9481;
  tft.begin(ID);
  tft.setRotation(3);
  tft.fillScreen(BLACK);
  text(350,20,1,&FreeSans9pt7b,"00:00 AM");
  text(20,40,1, &FreeSerif12pt7b, "player type ");
  text(20,70,1, &FreeSerif12pt7b, "label ");
    
    
}

char com[7];
int sa;
void loop()
{
  sa=Serial.available()-2;
  while (Serial.available()){
    for (int i=0; i<5; i++){
      com[i]=Serial.read();
      //    Serial.print(Serial.available());
      Serial.print(com[i]);
     delay(20);
    }
  }
  
  

 
  delay(20);
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
  tft.setTextColor(GREEN);
  tft.setTextSize(sz);
  tft.print(msg);
//    delay(100);
}

