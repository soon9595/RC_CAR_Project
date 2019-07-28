#include "ESP8266.h"
#include <SoftwareSerial.h>



//-----------------------Pin Info-------------------------

#define SignalBrake 4   // 파란색
#define SignalSpeed 5   // 초록색 
#define SignalRight 6   // 보라색
#define SignalLeft 7   // 노란색
#define SignalForward 8    //흰색
#define SignalBackward 9  //주황색

//-------------------------------------------------------------

//-----------------------Wifi Info--------------------------]


//#define SSID        "SOL_PRIME8193"
//#define PASSWORD    "wkdwns7015"
#define SSID        "Ad8032"
#define PASSWORD    "12345678a"
#define PORT 8090

//-------------------------------------------------------------

SoftwareSerial mySerial(2,3); // Rx =2 , Tx=3;
ESP8266 wifi(mySerial);
uint8_t IOflag=0;
uint8_t stack[5];
uint8_t i=0;
uint8_t prev_dir = 0;
uint8_t prev_lr = 0;
void setup()
{
    Serial.begin(9600);
    Serial.print("setup begin\r\n");
    
    Serial.print("FW Version:");
    Serial.println(wifi.getVersion().c_str());
      
    if (wifi.setOprToStationSoftAP()) {
        Serial.print("to station + softap ok\r\n");
    } else {
        Serial.print("to station + softap err\r\n");
    }
 
    if (wifi.joinAP(SSID, PASSWORD)) {
        Serial.print("Join AP success\r\n");
        Serial.print("IP: ");
        Serial.println(wifi.getLocalIP().c_str());    
    } else {
        Serial.print("Join AP failure\r\n");
    }
    
    if (wifi.enableMUX()) {
        Serial.print("multiple ok\r\n");
    } else {
        Serial.print("multiple err\r\n");
    }
    
    if (wifi.startTCPServer(PORT)) {
        Serial.print("start tcp server ok\r\n");
    } else {
        Serial.print("start tcp server err\r\n");
    }
    
    if (wifi.setTCPServerTimeout(10)) { 
        Serial.print("set tcp server timout 10 seconds\r\n");
    } else {
        Serial.print("set tcp server timout err\r\n");
    }
    
    Serial.print("setup end\r\n");

  //------------------Switch Setting-------------------------
  
  pinMode(SignalBrake,OUTPUT); 
  pinMode(SignalSpeed,OUTPUT); 
  pinMode(SignalRight,OUTPUT); 
  pinMode(SignalLeft,OUTPUT); 
  pinMode(SignalForward,OUTPUT);
  pinMode(SignalBackward,OUTPUT);  // 릴레이를 출력으로 설정

  //-----------------------------------------------------------
}


void loop()
{
  
    uint8_t buffer[10] = {};
    uint8_t mux_id;
    uint32_t len = wifi.recv(&mux_id, buffer, sizeof(buffer), 100); 
    if (len > 0) 
    {

        Serial.print("Received from :");
        Serial.println(mux_id);

        /*
        Serial.print("[");
        Serial.print(char(buffer));
        Serial.println("]");
        */
        
        
        Serial.print("[");
        for(uint32_t i = 0; i < len; i++) {
            Serial.print((char)buffer[i]);
            //cmd[i] = (char)buffer[i];
        }
        Serial.print("]\r\n");
        
        
        /*
        if(wifi.send(mux_id, buffer, len)) {
            Serial.print("send back ok\r\n");
        } else {
            Serial.print("send back err\r\n");
        }
        
        
        if (wifi.releaseTCP(mux_id)) {
            Serial.print("release tcp ");
            Serial.print(mux_id);
            Serial.println(" ok");
        } else {
            Serial.print("release tcp");
            Serial.print(mux_id);
            Serial.println(" err");
        }
        
        Serial.print("Status:[");
        Serial.print(wifi.getIPStatus().c_str());
        Serial.println("]");
        //Serial.println();
        */

    }
    if(buffer[0]!=0)
    {
      Serial.print("buffer : ");
      Serial.print(buffer[0]);
      Serial.print("\n");
      /*if(i==4)
      {
        for(int j=0;j<4;j++)
          stack[j] = stack[j+1];
        stack[i] = buffer[0];
      }
      else{
        stack[i] = buffer[0];
        i=i+1;
      }*/
      
    }
    if(char(buffer[0]) == 'O')
    {
      IOflag = 1;
      Serial.print("Out\n");
    }
    if(char(buffer[0]) == 'I')
    {
      IOflag = 0;
      Serial.print("In\n");
    }
    if(IOflag == 0){
      //move(buffer[0]);
      if(char(buffer[0]) == 'R')
      { 
        Serial.print("RRRRR\n");
        digitalWrite(SignalLeft,LOW);      // 7채널 릴레이 OFF
        delay(10);
        digitalWrite(SignalRight,HIGH);
        delay(100);
        prev_lr = 'L';
        //digitalWrite(SignalRight,LOW);     // 6채널 릴레이 ON     
      }
      else if(char(buffer[0]) == 'L')
      {
        Serial.print("LLLL\n");
        digitalWrite(SignalRight,LOW);      // 6채널 릴레이 OFF
        delay(10);
        digitalWrite(SignalLeft,HIGH);     // 7채널 릴레이 ON
        delay(100);
        prev_lr = 'R';
        //delay(100);
        //digitalWrite(SignalLeft,LOW);
      }
      else if(char(buffer[0]) == 'S')
      {
        Serial.print("SSSSSS\n");
        //digitalWrite(SignalForward,LOW);      
        //digitalWrite(SignalBackward,LOW);
        digitalWrite(SignalBrake,HIGH);// 4채널 릴레이 ON
        //delay(10);
        //digitalWrite(SignalBrake,LOW);
      }
      else if(char(buffer[0]) == 'F')
      {
        Serial.print("FFFFFFFFF\n");
        digitalWrite(SignalBackward,LOW);
        delay(10);
        digitalWrite(SignalForward,HIGH);
        prev_dir = 'B';
      }
      else if(char(buffer[0]) == 'B')
      {
        Serial.print("BBBBBBBBBB\n");
        digitalWrite(SignalForward,LOW);
        delay(10);
        digitalWrite(SignalBackward,HIGH);
        prev_dir = 'F';
      }
      else if(char(buffer[0]) == 'N')
      {
        Serial.print("NNNNNN\n");
        digitalWrite(SignalRight,LOW);    
        //delay(10);ㅠ
        digitalWrite(SignalLeft,LOW);
        //delay(10);     
        
      }
      else if(char(buffer[0])=='M')
      {
        Serial.print("MMMMMM\n");
        digitalWrite(SignalForward,LOW);
        delay(10);
        digitalWrite(SignalBackward,LOW);
        digitalWrite(SignalBrake,LOW);
      
      }
      
    }
    else if(IOflag == 1)
    {
      Serial.print("out process\n");
      if(prev_dir == 'F')
      {
        Serial.print("FFFFFFFFF\n");
        digitalWrite(SignalBrake,LOW);
        digitalWrite(SignalBackward,LOW);
        delay(10);
        digitalWrite(SignalForward,HIGH);
        if(prev_lr == 'R')
        {
          digitalWrite(SignalLeft,LOW);
          delay(10);
          digitalWrite(SignalRight,LOW);
          
        }
        else if(prev_lr == 'L')
      }
      else if(prev_dir == 'B')
      {
        Serial.print("BBBBBBBBBB\n");
        digitalWrite(SignalBrake,LOW);
        digitalWrite(SignalForward,LOW);
        delay(10);
        digitalWrite(SignalBackward,HIGH);
      }
    }
    /*
    else if(IOflag == 1 && i != 0)
    {
      uint8_t tmp = stack[0];
      for(int j=0;j<i;i++)
        stack[j] = stack[j+1];
      stack[i] = 0;
      i=i-1;
      if(i<0)
        i = 0;
    }
    */

/*
  digitalWrite(SignalRight,HIGH);     // 6채널 릴레이 ON 
  delay(1000);                
  digitalWrite(SignalRight,LOW);      // 6채널 릴레이 OFF
  delay(1000);
  digitalWrite(SignalLeft,HIGH);     // 7채널 릴레이 ON                 
  delay(1000);
  digitalWrite(SignalLeft,LOW);      // 7채널 릴레이 OFF
  delay(1000);

*/


  /*
  digitalWrite(SignalBrake,HIGH);     // 4채널 릴레이 ON                
  digitalWrite(SignalBrake,LOW);      // 4채널 릴레이 OFF
  digitalWrite(SignalSpeed,HIGH);     // 5채널 릴레이 ON                 
  digitalWrite(SignalSpeed,LOW);      // 5채널 릴레이 OFF
  digitalWrite(SignalRight,HIGH);     // 6채널 릴레이 ON                 
  digitalWrite(SignalRight,LOW);      // 6채널 릴레이 OFF
  digitalWrite(SignalLeft,HIGH);     // 7채널 릴레이 ON                 
  digitalWrite(SignalLeft,LOW);      // 7채널 릴레이 OFF
  */
}
