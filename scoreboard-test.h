#include <ArduinoJson.h>


int returnEndVal(float voltage_new, float resistor_base, float voltage_base) {
  float resistor = -resistor_base + (voltage_base * resistor_base / voltage_new);
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

void outputJson(int array1[], int array2[], int sheetnum) {

char out[512];
StaticJsonDocument<1024> score;

score["sheet"] = sheetnum;
  for (int j = 0; j < 16; j++) {
    score["Blue"][j] = array1[j];
    score["Yellow"][j] = array2[j];
  }
  Serial.print("Blue - ");
//  for (int j = 0; j < 16; j++) {
//    Serial.print(blueScore[j]);
//  }
//  Serial.println();
//  Serial.print("Yellow - ");
//  for (int j = 0; j < 16; j++) {
//    Serial.print(yellowScore[j]);
//  }
//  Serial.println();

  serializeJson(score, out);
//  mqtt_client->publish("curling/palmettocurling/score", 0, true, out);
}