import MainWindow
import SerialWorker
import pandas as pd

class Main(object):
    
    def __init__(self):
        self.temp_cutoff = 30
        self.distance_cutoff = 100000

    def setUp(self):
        self.df = pd.DataFrame(columns= ["Time", "Temp", "Distance"])

        self.receive_serial_thread = SerialWorker.SerialWorker('COM5', 9600)
        self.receive_serial_thread.start()
        self.receive_serial_thread.data_received.connect(self.processData)

        self.send_serial_thread = SerialWorker.SerialWorker('COM3', 9600)

        self.main_window = MainWindow.Ui_MainWindow(self.receive_serial_thread, self.send_serial_thread)

    def processData(self, data):
        self.df.loc[len(self.df)] = [float(data[0]), float(data[1]), float(data[2])]
        
    


        

if __name__ == "__main__":
    main = Main()
    main.setUp()