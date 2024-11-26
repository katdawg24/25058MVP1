import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
import serial

class SerialWorker(QThread):
    data_received = pyqtSignal(list)  # Signal to send data to the GUI

    def __init__(self, port, baudrate):
        super().__init__()
        self.port = port
        self.baudrate = baudrate
        self.running = True

    def run(self):
        ser = serial.Serial(self.port, self.baudrate)
        ser.setDTR(False)
        time.sleep(1)
        ser.flushInput()
        ser.setDTR(True)

        try:
            while self.running:
                if ser.in_waiting > 0:
                    data = ser.readline().decode('utf-8').strip()
                    values = [float(x) for x in data.split()]
                    self.data_received.emit(values)  # Emit the signal with new data
            ser.close()
        except serial.SerialException as e:print(f"Error: {e}")
        # finally:
        #     if hasattr(self, 'ser') and self.ser.is_open:
        #         self.ser.close() 


    def send_data(self, data):
        if self.running and hasattr(self, 'ser') and self.ser.is_open:
            try:
                self.ser.write(data.encode('utf-8'))  # Send data as bytes
            except serial.SerialException as e:
                print(f"Error sending data: {e}")
        else:
            if not self.running:
                print("Cannot send data: The thread is not running.")
            elif not hasattr(self, 'ser'):
                print("Cannot send data: Serial connection ('ser') is not initialized.")
            elif not self.ser.is_open:
                print("Cannot send data: Serial port is not open.")

    def stop(self):
        self.running = False
        self.wait()