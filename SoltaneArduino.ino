#include <Servo.h> // motor driver library

// Constants and Variables
Servo motor;               // Servo object for motor control (modify if using a motor driver)
const int motorPin = 9;    // PWM pin for motor control
const int lidarPin = A0;   // Example pin for Lidar sensor input
unsigned long lastSendTime = 0;  // To track when to send data
const int sendInterval = 1000;   // Interval for sending data (milliseconds)

// Setup Function
void setup() {
  Serial.begin(9600);       // Initialize serial communication
  motor.attach(motorPin);   // Attach motor to the PWM pin

  // Initialize Lidar sensor + other peripherals if required
  pinMode(lidarPin, INPUT);
}

// Main Loop
void loop() {
  // Handle incoming commands
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');  // Read the incoming command
    command.trim(); // Remove whitespace or newline
    processCommand(command);
  }

  // Periodically send sensor data
  unsigned long currentTime = millis();
  if (currentTime - lastSendTime >= sendInterval) {
    lastSendTime = currentTime;
    sendSensorData();
  }
}

// Function to Process Incoming Commands
// Speed change command formatted as follows: "SPEED {value}\n"
void processCommand(String command) {
  if (command.startsWith("SPEED")) {
    int speed = command.substring(6).toInt();      // Extract speed value
    speed = constrain(speed, 0, 100);             // Ensure speed is within 0-100%
    setMotorSpeed(speed);                         // Adjust motor speed
    Serial.println("ACK: Speed set to " + String(speed));
  } else {
    Serial.println("ERROR: Unknown Command");
  }
}

// Function to Set Motor Speed
void setMotorSpeed(int speed) {
  int pwmValue = map(speed, 0, 100, 0, 180);       // Convert 0-100% to 0-180 for servo (or 0-255 for PWM motors)
  motor.write(pwmValue);                           // Update motor speed
}

// Function to Send Sensor Data
void sendSensorData() {
  // Replace with actual Lidar sensor data reading
  int lidarValue = analogRead(lidarPin);           // Example Lidar reading
  float distance = (lidarValue / 1023.0) * 500.0;  // Example conversion to distance in cm

  // Send data as <time> <distance>
  unsigned long currentTime = millis();
  Serial.print(currentTime / 1000.0, 2);           // Time in seconds with 2 decimal places
  Serial.print(" ");
  Serial.println(distance, 2);                     // Distance with 2 decimal places
}
