#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>


const char* ssid = "Public";
const char* password = "password";
const char* mqtt_server = "broker.hivemq.com";
const char* HostName = "Sheet2";
const char* topic = "curling/palmettocurling/score/2";
const char* mqttUser = "MQTT USER2";
const char* mqttPassword = "MQTT PASSWORD";
WiFiClient espClient;
PubSubClient client(espClient);

//const int bluePins[] = {3,2,0,4};
const int bluePins[] = {4,0,2,3};

//const int yellowPins[] = {14,12,13,15};
const int yellowPins[] = {15,13,12,14};
char out[512];
StaticJsonDocument<1024> score;
//JsonObject& score = jsonBuffer.createObject();
int blueEnablePin = 5;
int yellowEnablePin = 16;

int blueScore[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
int yellowScore[16] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

float Vin = 3.0;
float Vout = 0.0;
float R1 = 974.0;
float R2 = 0;
float buffer = 0.0;

void setup_wifi() {
  delay(10);
  
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect(HostName, mqttUser, mqttPassword)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

int returnEndVal(float resistor) {
  int End = 0;
  if (resistor < 50) {
    End = 0;
  }
  else if (50 < resistor && resistor < 150) {
    End =  1;
  }
  else if (150 < resistor && resistor < 250) {
    End =  2;
  }
  else if (250 < resistor && resistor < 350) {
    End = 3;
  }
  else if (350 < resistor && resistor < 450) {
    End =  4;
  }
  else if (450 < resistor && resistor < 550) {
    End = 5;
  }
  else if (550 < resistor && resistor < 650) {
    End =  6;
  }
  else if (650 < resistor && resistor < 750) {
    End =  7;
  }
  else if (750 < resistor && resistor < 850) {
    End =  8;
  }
  else if (850 < resistor && resistor < 950) {
    End =  9;
  }
  else if (950 < resistor && resistor < 1050) {
    End =  10;
  }
  else if (1050 < resistor && resistor < 1150) {
    End = 11;
  }
  else if (1150 < resistor && resistor < 1250) {
    End =  12;
  }
  else {
    End =  0;
  }
  return End;
}

int setpins(const int pins[], bool A, bool B, bool C, bool D) {
    digitalWrite(pins[0],A);
    digitalWrite(pins[1],B);
    digitalWrite(pins[2],C);
    digitalWrite(pins[3],D);
}

void readBlue() {
  digitalWrite(yellowEnablePin,1);
  digitalWrite(blueEnablePin,0);
  int x = 0;
  while (x < 16) {
    if(x == 0) {
      setpins(bluePins,0,0,0,0);
    }
    else if(x == 1) {
      setpins(bluePins,0,0,0,1);
    }
    else if(x == 2) {
      setpins(bluePins,0,0,1,0);
    }
    else if(x == 3) {
      setpins(bluePins,0,0,1,1);
    }
    else if(x == 4) {
      setpins(bluePins,0,1,0,0);
    }
    else if(x == 5) {
      setpins(bluePins,0,1,0,1);
    }
    else if(x == 6) {
      setpins(bluePins,0,1,1,0);
    } 
    else if(x == 7) {
      setpins(bluePins,0,1,1,1);
      }
    else if(x == 8) {
      setpins(bluePins,1,0,0,0);
    }
    else if(x == 9) {
      setpins(bluePins,1,0,0,1);
    }
    else if(x == 10) {
      setpins(bluePins,1,0,1,0);
    }
    else if(x == 11) {
      setpins(bluePins,1,0,1,1);
    }
    else if(x == 12) {
      setpins(bluePins,1,1,0,0);
    }
    else if(x == 13) {
      setpins(bluePins,1,1,0,1);
    }
    else if(x == 14) {
      setpins(bluePins,1,1,1,0);
    }
    else {
      setpins(bluePins,1,1,1,1);
    }
    delay(500);
    buffer = analogRead(0);
    Vout = (buffer / 1024.0) * Vin;
    R2=((Vin/Vout)-1)*R1;
    //Serial.println(returnEndVal(R2));
    blueScore[x] = returnEndVal(R2-100);
    x++;
  }
}

void readYellow() {
  digitalWrite(blueEnablePin,1);
  digitalWrite(yellowEnablePin,0);
  int x = 0;
  while (x < 16) {
    if(x == 0) {
      setpins(yellowPins,0,0,0,0);
    }
    else if(x == 1) {
      setpins(yellowPins,0,0,0,1);
    }
    else if(x == 2) {
      setpins(yellowPins,0,0,1,0);
    }
    else if(x == 3) {
      setpins(yellowPins,0,0,1,1);
    }
    else if(x == 4) {
      setpins(yellowPins,0,1,0,0);
    }
    else if(x == 5) {
      setpins(yellowPins,0,1,0,1);
    }
    else if(x == 6) {
      setpins(yellowPins,0,1,1,0);
    } 
    else if(x == 7) {
      setpins(yellowPins,0,1,1,1);
      }
    else if(x == 8) {
      setpins(yellowPins,1,0,0,0);
    }
    else if(x == 9) {
      setpins(yellowPins,1,0,0,1);
    }
    else if(x == 10) {
      setpins(yellowPins,1,0,1,0);
    }
    else if(x == 11) {
      setpins(yellowPins,1,0,1,1);
    }
    else if(x == 12) {
      setpins(yellowPins,1,1,0,0);
    }
    else if(x == 13) {
      setpins(yellowPins,1,1,0,1);
    }
    else if(x == 14) {
      setpins(yellowPins,1,1,1,0);
    }
    else {
      setpins(yellowPins,1,1,1,1);
    }
    delay(500);
    buffer = analogRead(0);
    Vout = (buffer / 1024.0) * Vin;
    R2=((Vin/Vout)-1)*R1;
    //Serial.println(returnEndVal(R2));
    yellowScore[x] = returnEndVal(R2-100);
    x++;
  }
}   



void setup() {
  Serial.begin(9600);
  

  for (int x = 0; x < 4; x++) {
    pinMode(bluePins[x],OUTPUT);
    pinMode(yellowPins[x],OUTPUT);
    pinMode(blueEnablePin,OUTPUT);
    pinMode(yellowEnablePin,OUTPUT);
  }
 setup_wifi();
  client.setServer(mqtt_server, 1883);
  // put your setup code here, to run once:

}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  readBlue();
  readYellow();
  score["sheet"] = "3";
  for (int j = 0; j < 16; j++) {
    score["Blue"][j] = blueScore[j];
    score["Yellow"][j] = yellowScore[j];
  }
  Serial.print("Blue - ");
  for (int j = 0; j < 16; j++) {
    Serial.print(blueScore[j]);
  }
  Serial.println();
  Serial.print("Yellow - ");
  for (int j = 0; j < 16; j++) {
    Serial.print(yellowScore[j]);
  }
  Serial.println();

  serializeJson(score, out);
  Serial.println(out);
  client.publish(topic, out);

  client.loop();
}
