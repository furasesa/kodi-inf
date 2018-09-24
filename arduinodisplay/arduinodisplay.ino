//text size is approximately 34 of char in scale textSize = 2

#define LCD_CS A3 // Chip Select goes to Analog 3
#define LCD_CD A2 // Command/Data goes to Analog 2
#define LCD_WR A1 // LCD Write goes to Analog 1
#define LCD_RD A0 // LCD Read goes to Analog 0
#define LCD_RESET A4 // Can alternately just connect to Arduino's

#include <Adafruit_GFX.h>    // Core graphics library
#include <MCUFRIEND_kbv.h>   // Hardware-specific library
MCUFRIEND_kbv tft;

#include <FreeDefaultFonts.h>

#include <Fonts/FreeMono9pt7b.h>
#include <Fonts/FreeMono12pt7b.h>
#include <Fonts/FreeMonoBold9pt7b.h>
#include <Fonts/FreeMonoBold12pt7b.h>
#include <Fonts/FreeMonoBoldOblique9pt7b.h>
#include <Fonts/FreeMonoBoldOblique12pt7b.h>
#include <Fonts/FreeMonoOblique9pt7b.h>
#include <Fonts/FreeMonoOblique12pt7b.h>
#include <Fonts/FreeSans9pt7b.h>
#include <Fonts/FreeSans12pt7b.h>
#include <Fonts/FreeSansBold9pt7b.h>
#include <Fonts/FreeSansBoldOblique9pt7b.h>
#include <Fonts/FreeSansOblique9pt7b.h>
#include <Fonts/FreeSerif9pt7b.h>
#include <Fonts/FreeSerifBold9pt7b.h>
#include <Fonts/FreeSerifBoldItalic9pt7b.h>
#include <Fonts/FreeSerifBoldItalic12pt7b.h>
#include <Fonts/FreeSerifItalic9pt7b.h>
#include <Fonts/Org_01.h>
#include <Fonts/Picopixel.h>
#include <Fonts/TomThumb.h>

//#define BLACK   0x0000
//#define RED     0xF800
//#define GREEN   0x07E0
//#define WHITE   0xFFFF
//#define GREY    0x8410

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


#define MARGIN 20
#define SPACING 30

int bg_color = BR4;

uint16_t wd,h;

void setup()
{
  Serial.begin(9600);
  uint16_t ID = tft.readID();
  if (ID == 0xD3) ID = 0x9481;
  tft.begin(ID);
  tft.setRotation(3);
//  clear the screen
}

#if defined(MCUFRIEND_KBV_H_)
uint16_t scrollbuf[320];    // my biggest screen is 320x480
#define READGRAM(x, y, buf, w, h)  tft.readGRAM(x, y, buf, w, h)
#else
uint16_t scrollbuf[320];    // Adafruit only does 240x320
// Adafruit can read a block by one pixel at a time
int16_t  READGRAM(int16_t x, int16_t y, uint16_t *block, int16_t w, int16_t h)
{
    uint16_t *p;
    for (int row = 0; row < h; row++) {
        p = block + row * w;
        for (int col = 0; col < w; col++) {
            *p++ = tft.readPixel(x + col, y + row);
        }
    }
}
#endif

int playerId;
int partId;
String header_title;
String content_msg;
String videoType;
String showTitle;
String season;
int episode;
int votes;
//  music
//header
int track;
String title;
//content
String artist;
String album;
String genre;
int year;
int duration;
int current_duration;
//footer
int percentage;

void loop()
{ 
  if(Serial.available()>0){
//    tft.fillScreen(bg_color);
    playerId = Serial.readStringUntil(':').toInt();
    switch (playerId) {
      case 1:
//        message = str(1)+":"+v.videoType+":"+v.showTitle+":"+v.season+":"+v.episode+":"+v.votes
        videoType=Serial.readStringUntil(':');
        showTitle=Serial.readStringUntil(':');
        season=Serial.readStringUntil(':'); 
        episode=Serial.readStringUntil(':').toInt(); 
        votes=Serial.readStringUntil(':').toInt();

        header_title = String(episode)+". "+showTitle;
        header(header_title);
//        videoUI();
        break;
      case 0:
        partId = Serial.readStringUntil(':').toInt();
        switch (partId) {
          case 2:
            // content
            artist=Serial.readStringUntil(':');
            album=Serial.readStringUntil(':');
            genre=Serial.readStringUntil(':');
            year=Serial.readStringUntil(':').toInt();
            duration=Serial.readStringUntil(':').toInt();
            content(0);
            Serial.flush();
            break;

          case 1:
            // header
            track=Serial.readStringUntil(':').toInt();
            title=Serial.readStringUntil(':');
            header_title = String(track)+". "+title;
            header(header_title);
            Serial.flush();
            break;

          case 0:
            // footer
            percentage = Serial.readStringUntil(':').toInt();
            Serial.flush();
            break;
        }
        
        break;
    }
  }
  delay (1000);
  if (duration > 0 & percentage >0){
    current_duration = duration * percentage /100 +1;
  }
  
  footer (current_duration);
}

void windowScroll(int16_t x, int16_t y, int16_t wid, int16_t ht, int16_t dx, int16_t dy, uint16_t *buf)
{
    if (dx) for (int16_t row = 0; row < ht; row++) {
            READGRAM(x, y + row, buf, wid, 1);
            tft.setAddrWindow(x, y + row, x + wid - 1, y + row);
            tft.pushColors(buf + dx, wid - dx, 1);
            tft.pushColors(buf + 0, dx, 0);
        }
    if (dy) for (int16_t col = 0; col < wid; col++) {
            READGRAM(x + col, y, buf, 1, ht);
            tft.setAddrWindow(x + col, y, x + col, y + ht - 1);
            tft.pushColors(buf + dy, ht - dy, 1);
            tft.pushColors(buf + 0, dy, 0);
        }
}

void header(String msg){
  wd = tft.width();
  h = tft.height();
  uint16_t header_w = wd;
  uint16_t header_h = 60;
  tft.setFont(&FreeSerifBoldItalic12pt7b);
  tft.setAddrWindow(0,0,header_w,header_h);
  tft.drawRect(0,0,header_w,header_h,BR3);
  tft.fillRect(0,0,header_w,header_h,BR3);
  tft.setCursor(30,35);
  tft.print(msg);
  // diagonal scroll of block
//  for (int16_t i = header_h, dx = 0, dy = header_h/10; i > 0; i -= dy) {
//      windowScroll(0, 0, header_w, header_h, dx, dy, scrollbuf);
//  }
//  for (uint16_t i = 1; i <= 64; i++) {
//    tft.vertScroll(0, header_h, i);
//    delay(20);
//  }
  
}

void content (int mode){
  uint16_t content_w = tft.width();
  uint16_t content_h = 200;
  tft.setAddrWindow(0,60,content_w,content_h);
  tft.drawRect(0,60,content_w,content_h,BR4);
  tft.fillRect(0,60,content_w,content_h,BR4);

  switch (mode){
    case 1:
      // video mode
      break;
    case 0:
      uint16_t x = 30;
      uint16_t y = 80;
      if (artist){
        printmsg(x,y,&FreeMono12pt7b,artist);
      }
      if (album){
        y += 20;
        printmsg(x,y,&FreeMono12pt7b,album);
      }
      if (year > 1000){
        y += 20;
        printmsg(x,y, &FreeMono12pt7b, String(year));
      }
      if (duration>0){
        y += 20;
        int minutes = duration/60;
        int seconds = duration%60;
    
        String str_minutes,str_seconds,str_duration;
        if (minutes <10) {
          str_minutes = "0"+String(minutes);
        } else {
          str_minutes = String(minutes);
        }
        if (seconds <10) {
          str_seconds = "0"+String(seconds);
        } else {
          str_seconds = String(seconds);
        }
    
        str_duration = str_minutes+":"+str_seconds;
        printmsg(x,y,&FreeMono12pt7b, str_duration);
      }
        
  }

}

void printmsg (uint16_t x, uint16_t y, const GFXfont *font, String message){
  tft.setFont(font);
  tft.setCursor(x,y);
  tft.print(message);
}

void footer (int i){
  wd = tft.width();
  h = tft.height();
  uint16_t footer_w = wd;
  uint16_t footer_h = 60;
  
  uint16_t bar = wd / duration * i;
  
  tft.fillRect(0,270, bar ,40, PINK2); 
 
}

void videoUI(){
  tft.fillScreen(bg_color);
}


