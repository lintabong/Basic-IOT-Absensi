#include <Arduino.h>
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <Firebase_ESP_Client.h>

#include "addons/TokenHelper.h"
#include "addons/RTDBHelper.h"
#include <SPI.h>
#include <MFRC522.h>

#define WIFI_SSID ""
#define WIFI_PASSWORD ""
#define API_KEY ""
#define DATABASE_URL ""

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

bool signupOK = false;

#define RST_PIN D3
#define SS_PIN  D4

MFRC522 mfrc522(SS_PIN, RST_PIN);

byte readCard[4];
String tagID = "";
String userlist;

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  config.api_key = API_KEY;
  config.database_url = DATABASE_URL;
  
  if (Firebase.signUp(&config, &auth, "", "")) {
    Serial.println("ok");
    signupOK = true;
  }
  else {
    Serial.printf("%s\n", config.signer.signupError.message.c_str());
  }
  
  config.token_status_callback = tokenStatusCallback;

  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
  
  SPI.begin();
  mfrc522.PCD_Init();
  delay(4);
  mfrc522.PCD_DumpVersionToSerial();  
}

void loop() {
  while (getID()){
    Serial.print("**TAG ID: ");
    Serial.println(tagID);
    
    if (Firebase.RTDB.getString(&fbdo, "/user")){
      userlist = fbdo.stringData();
      Serial.println("**firebase get user's data");
    }
  
    StaticJsonDocument<768> doc;
  
    DeserializationError err = deserializeJson(doc, userlist);
    if (err) {
      Serial.print("ERROR: ");
      Serial.println(err.c_str());
      return;
    }
  
    String getid = doc[tagID];
  
    if (getid == "null"){
      Serial.println("  id tidak terdaftar");
      Firebase.RTDB.setString(&fbdo, "/newuser/id" , tagID);
      
    } else {
      Serial.print("  data: ");
      Serial.println(getid);
      
      String stat = "";
      
      if (Firebase.RTDB.getString(&fbdo, "/stat/" + tagID)){
        stat = fbdo.stringData();
      }

      if (stat == "login"){
        Firebase.RTDB.setString(&fbdo, "/stat/" + tagID , "logout");
        Serial.print("  stat: ");Serial.println("logout");
      } else if (stat == "logout"){
        Firebase.RTDB.setString(&fbdo, "/stat/" + tagID , "login");
        Serial.print("  stat: ");Serial.println("login");
      } else {
        Firebase.RTDB.setString(&fbdo, "/stat/" + tagID , "logout");
        Serial.print("  stat: ");Serial.println("else");
      }
    }
    delay(1000);
  }
}

boolean getID() {
  if ( ! mfrc522.PICC_IsNewCardPresent()) {
    return false;
  }
  if ( ! mfrc522.PICC_ReadCardSerial()) {
    return false;
  }
  tagID = "";
  for ( uint8_t i = 0; i < 4; i++) {
    //readCard[i] = mfrc522.uid.uidByte[i];
    tagID.concat(String(mfrc522.uid.uidByte[i], HEX));
  }
  tagID.toUpperCase();
  mfrc522.PICC_HaltA();
  return true;
}
