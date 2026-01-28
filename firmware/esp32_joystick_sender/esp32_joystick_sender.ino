#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "YOUR_WIFI_SSID";       // Replace with your WiFi SSID
const char* password = "YOUR_WIFI_PASSWORD"; // Replace with your WiFi password
const char* udpAddress = "RASPI_IP_ADDRESS"; // Replace with Pi's IP (e.g., "192.168.1.100")
const int udpPort = 3333;                  // UDP port to send to

#define VRX_PIN 3  // X-axis pin (angular velocity)
#define VRY_PIN 4  // Y-axis pin (linear velocity)

WiFiUDP udp;
int centerX = 2048; // Calibrate: joystick idle value
int centerY = 2048;
float maxLinear = 1.0;  // Max linear speed (m/s, scale to your robot)
float maxAngular = 1.0; // Max angular speed (rad/s)

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to WiFi");
  udp.begin(udpPort);  // Local port (can be same)
}

void loop() {
  int valueX = analogRead(VRX_PIN);
  int valueY = analogRead(VRY_PIN);

  // Normalize to -1.0 to 1.0 (deadzone of 200 to avoid noise)
  float normX = 0.0;
  if (abs(valueX - centerX) > 200) {
    normX = (valueX - centerX) / 2047.0;  // -1 to 1
  }
  float normY = 0.0;
  if (abs(valueY - centerY) > 200) {
    normY = (valueY - centerY) / 2047.0;  // Invert if forward is down
    normY = -normY;  // Assuming pushing forward decreases Y; test and flip if needed
  }

  // Scale to velocities
  float linear = normY * maxLinear;
  float angular = normX * maxAngular;  // Positive X might be right turn; flip sign if needed

  // Format as JSON string
  char message[50];
  snprintf(message, sizeof(message), "{\"lin\":%.2f,\"ang\":%.2f}", linear, angular);

  // Send UDP
  udp.beginPacket(udpAddress, udpPort);
  udp.write((uint8_t*)message, strlen(message));
  udp.endPacket();

  delay(100);  // Send rate; adjust for responsiveness
}
