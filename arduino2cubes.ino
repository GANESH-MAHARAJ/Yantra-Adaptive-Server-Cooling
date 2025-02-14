#include <DHT.h>

// DHT11 Sensor Pins
#define DHTPIN1 2
#define DHTPIN2 4       
#define DHTTYPE DHT11  

DHT dht1(DHTPIN1, DHTTYPE);
DHT dht2(DHTPIN2, DHTTYPE);

// Fan Control Pins
#define FAN_PIN_1 5  // FAN 1 Gate (PWM)
#define FAN_PIN_2 3  // FAN 2 Gate (PWM)

// LED Pin for over-temperature warning
#define LED_PIN 6
 
// Previous temperature & humidity readings
float prev_temp1 = 0.0, prev_temp2 = 0.0;
float prev_hum1 = 0.0, prev_hum2 = 0.0;

void setup() {
    Serial.begin(9600);
    dht1.begin();
    dht2.begin();

    pinMode(FAN_PIN_1, OUTPUT);
    pinMode(FAN_PIN_2, OUTPUT);
}

void loop() {
    
    float prev_temp1 = dht1.readTemperature();
    float prev_temp2 = dht2.readTemperature();
    float prev_hum1 = dht1.readHumidity();
    float prev_hum2 = dht2.readHumidity();
    
    
    delay(1000);
    // Read new sensor values
    float temp1 = dht1.readTemperature();
    float temp2 = dht2.readTemperature();
    float hum1 = dht1.readHumidity();
    float hum2 = dht2.readHumidity();

    // Check for read errors
    if (isnan(temp1) || isnan(hum1) || isnan(temp2) || isnan(hum2)) {
        Serial.println("Error: Failed to read from DHT sensor!");
        delay(2000);
        return;
    }
    
    if (temp1 >= 40.0 || temp2 >= 40.0) {
        digitalWrite(LED_PIN, HIGH);
    } else {
        digitalWrite(LED_PIN, LOW);
    }

    // Read ACS712 current sensor values
    float acsSamples1 = 0.0, acsSamples2 = 0.0;
    for (int i = 0; i < 700; i++) {
        acsSamples1 += analogRead(A0);
        delay(3);
    }
    for (int i = 0; i < 700; i++) {
        acsSamples2 += analogRead(A1);
        delay(3);
    }

    // Compute Average and Convert to Current
    float avgAcs1 = acsSamples1 / 700.0;
    float avgAcs2 = acsSamples2 / 700.0;
    float current1 = (2.5 - (avgAcs1 * (5.0 / 1010.1))) / 0.1;
    float current2 = (2.5 - (avgAcs2 * (5.0 / 1008.1))) / 0.1;

    // Print data
    Serial.print(prev_temp1, 2); Serial.print(" ");
    Serial.print(prev_hum1, 2); Serial.print(" ");
    Serial.print(prev_temp2, 2); Serial.print(" ");
    Serial.print(prev_hum2, 2); Serial.print(" ");
    Serial.print(temp1, 2); Serial.print(" ");
    Serial.print(hum1, 2); Serial.print(" ");
    Serial.print(temp2, 2); Serial.print(" ");
    Serial.print(hum2, 2); Serial.print(" ");
    Serial.print(current1, 2); Serial.print(" ");
    Serial.println(current2, 2);

    // Fan Control from Serial Input
    if (Serial.available()) {
        int fanID = Serial.parseInt();
        int pwmValue = Serial.parseInt();
        
        // Clear Serial buffer
        while (Serial.available()) Serial.read();  

        if ((fanID == 1 || fanID == 2) && pwmValue >= 0 && pwmValue <= 255) { 
            int fanPin = (fanID == 1) ? FAN_PIN_1 : FAN_PIN_2;
            analogWrite(fanPin, pwmValue);  // Set PWM output

            Serial.print("FAN");
            Serial.print(fanID);
            Serial.print(" PWM set to: ");
            Serial.println(pwmValue);
        } 
        else {
            Serial.println("Invalid Command! Send: fanID pwmValue (e.g., '1 150')");
        }
    }

    delay(1000);
}