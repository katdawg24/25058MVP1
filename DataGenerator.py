import serial
import time
import random
from datetime import datetime

def generate_data():
    """Generate a line of data with time, temperature, and depth."""
    current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # Format time with milliseconds
    temperature = round(random.uniform(20.0, 25.0), 1)  # Random temperature in Celsius
    depth = round(random.uniform(50, 60), 1)  # Random depth in mm
    return f"{current_time} {temperature} {depth}"

def main():
    port = 'COM3'  # Replace with your COM port
    baudrate = 9600

    try:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            print(f"Sending data to {port} at {baudrate} baud...")
            while True:
                data = generate_data()
                ser.write((data + '\n').encode('utf-8'))  # Send data as bytes
                print(f"Sent: {data}")
                time.sleep(0.1)  # Wait 100 milliseconds
    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Program stopped by user.")

if __name__ == "__main__":
    main()
