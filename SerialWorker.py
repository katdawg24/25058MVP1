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
        except serial.SerialException as e:
            print(f"Error: {e}")

    def stop(self):
        self.running = False
        self.wait()