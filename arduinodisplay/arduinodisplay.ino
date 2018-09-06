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

//Material Design
//RED
#define RED1  0xfc4f //A100
#define RED2  0xfa8a //A200
#define RED3  0xf8c8 //A400
#define RED4  0xd000 //A700
//Pink
#define PINK1  0xfc15
#define PINK2  0xfa10
#define PINK3  0xf00a
#define PINK4  0xc08c
//PURPLE
#define PUR1  0xe41f
#define PUR2  0xda1e
#define PUR3  0xd01e
#define PUR4  0xa81f
//DEEP PURPLE
#define DP1   0xb43f
#define DP2   0x7a7f
#define DP3   0x611f
#define DP4   0x601c
//INDIGO
#define IN1   0x8cff
#define IN2   0x537f
#define IN3   0x3ade
#define IN4   0x327e
//BLUE
#define BL1   0x859f
#define BL2   0x445f
#define BL3   0x2bdf
#define BL4   0x2b1f
//LIGHT BLUE
#define LB1   0x86bf
#define LB2   0x461f
#define LB3   0x059f
#define LB4   0x049c
//CYAN
#define CY1   0x87ff
#define CY2   0x1fff
#define CY3   0x071f
#define CY4   0x05ba
//TEAL
#define TE1   0xa7fc
#define TE2   0x67fb
#define TE3   0x1f3a
#define TE4   0x05f4
//GREEN
#define GR1   0xb7b9
#define GR2   0x6f95
#define GR3   0x072e
#define GR4   0x062a
//LIGHT GREEN
#define LG1   0xcfb2
#define LG2   0xb7eb
#define LG3   0x77e1
#define LG4   0x66c3
//LIME
#define LI1   0xf7f0
#define LI2   0xefe8
#define LI3   0xc7e0
#define LI4   0xaf40
//YELLOW
#define YE1   0xfff1
#define YE2   0xffe0
#define YE3   0xff40
#define TE4   0xfea0
//AMBER
#define AM1   0xff2f
#define AM2   0xfea8
#define AM3   0xfe20
#define AM4   0xfd40
//ORANGE
#define OR1   0xfe90
#define OR2   0xfd48
#define OR3   0xfc80
#define OR4   0xfb60
//DEPP ORANGE
#define DO1   0xfcf0
#define DO2   0xfb68
#define DO3   0xf9e0
#define DO4   0xd960
//BROWN
#define BR1   0xbd54
#define BR2   0x8b6c
#define BR3   0x6a68
#define BR4   0x49a4
//GREY
#define GR1   0xef7d
#define GR2   0xbdf7
#define GR3   0x630c
#define GR4   0x2104
//BLUE GREY
#define BG1   0xb5f8
#define BG2   0x63f1
#define BG3   0x42ec
#define BG4   0x2987



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

