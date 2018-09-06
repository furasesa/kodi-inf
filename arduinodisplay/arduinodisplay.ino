#include <Adafruit_GFX.h>    // Core graphics library
#include <MCUFRIEND_kbv.h>   // Hardware-specific library
MCUFRIEND_kbv tft;

#include <Fonts/FreeSans9pt7b.h>
#include <Fonts/FreeSans12pt7b.h>
#include <Fonts/FreeSerif12pt7b.h>

#include <FreeDefaultFonts.h>

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

#define RES_W 480
#define RES_H 320

#define LCD_W 480
#define LCD_H 320
#define MARGIN 10

int bg_color = BG4;

void setup()
{
  tft.reset();
  Serial.begin(115200);
  uint16_t ID = tft.readID();
  if (ID == 0xD3) ID = 0x9481;
  tft.begin(ID);
  tft.setRotation(3);
  
    
}


//String command;
String playerType;
int track_value;
String title_value;
String artist_value;
String album_value;
String year_value;
String genre_value;
int duration_value;
void loop()
{
  if(Serial.available()>0){
    playerType = Serial.readStringUntil(';');
    track_value=Serial.readStringUntil(';').toInt();
    title_value=Serial.readStringUntil(';');
    artist_value=Serial.readStringUntil(';');
    album_value=Serial.readStringUntil(';');
    year_value=Serial.readStringUntil(';');
    genre_value=Serial.readStringUntil(';');
    duration_value=Serial.readStringUntil(';').toInt();
    
    GUIBuilder();
  }
}



void GUIBuilder(){
  tft.fillScreen(bg_color);
//  tft.fillRect(MARGIN,MARGIN,LCD_W-2*MARGIN,LCD_H-2*MARGIN,bg_color);
  String header_title;
  int spacing   = 30;
  int left_margin = MARGIN*2;
  int header_x  = left_margin;
  int header_y  = MARGIN*3;
  int artist_x  = left_margin;
  int artist_y  = header_y+spacing*2;
  int album_x   = left_margin;
  int album_y   = artist_y+spacing;
  int year_x    = left_margin;
  int year_y    = album_y+spacing;
  int genre_x   = left_margin;
  int genre_y   = year_y+spacing;
  int duration_x    = left_margin;
  int duration_y    = genre_y+spacing;
  
  int rect_detail_x, rect_detail_y, rect_sz_w, rect_sz_h, rect_color;
  
  tft.setFont(&FreeSerif12pt7b);
  Serial.println(track_value);
  Serial.println(title_value);
  
  if (track_value > 0){
    header_title=String(track_value)+". "+title_value;
    
  } else {
    header_title=title_value;
  }
  Serial.println(header_title);
  tft.setTextColor(RED1);
  tft.setTextSize(1.5);
  tft.setCursor(header_x, header_y);
  tft.print(header_title);

  delay(50);
  tft.setTextSize(1);

  if (artist_value){
    tft.setTextColor(LI1);
    tft.setCursor(artist_x, artist_y);
    tft.print("Artist: "+artist_value);
  }

  if (album_value){
    tft.setTextColor(AM1);
    tft.setCursor(album_x, album_y);
    tft.print("Album: "+album_value);
  }

  if (year_value){
    tft.setTextColor(IN1);
    tft.setCursor(year_x, year_y);
    tft.print("Year: "+year_value);
  }
  if (genre_value){
    tft.setTextColor(GR1);
    tft.setCursor(genre_x, genre_y);
    tft.print("Genre: "+genre_value);
  }
  if (duration_value>0){
    int minutes = duration_value/60;
    int seconds = duration_value%60;
    String men,det;
    
    if (minutes > 0){
      men = String(minutes)+" Menit ";
    }
    if (seconds >0) {
      det = String(seconds)+" Detik";
    }
    tft.setTextColor(PUR1);
    tft.setCursor(duration_x, duration_y);
    tft.print("Duration: "+men+det);
  }
    
  
  
//  tft.setFont(&FreeSerif12pt7b);
//  tft.setCursor(title_start, header_top);
//  tft.setTextColor(title_color);
//  tft.setTextSize(header_text_sz);
//  tft.print(str);


}


//
//void showSongDetail(){
//  int posx,posy;
//  tft.drawRect(detail_window_posx,detail_window_posy,detail_window_w,detail_window_h,detail_window_color);
//}
//void playerTrack(String str){
//  tft.setFont(&FreeSerif12pt7b);
//  tft.setCursor(track_start, header_top);
//  tft.setTextColor(track_color);
//  tft.setTextSize(header_text_sz);
//  tft.print(str);
//}
//
//void playerTitle(String str){
//  tft.fillRect(MARGIN,MARGIN,LCD_W-2*MARGIN,LCD_H-2*MARGIN,bg_color);
//  tft.setFont(&FreeSerif12pt7b);
//  tft.setCursor(title_start, header_top);
//  tft.setTextColor(title_color);
//  tft.setTextSize(header_text_sz);
//  tft.print(str);
//  if(playerType=="song"){
////    Serial.println("playerType=song");
//    showSongDetail();
//  }
//}
//
//void playerArtist(String str){
//  tft.setFont(&FreeSerif12pt7b);
//  tft.setCursor(title_start, header_top);
//  tft.setTextColor(title_color);
//  tft.setTextSize(header_text_sz);
//  tft.print(str);
//}

