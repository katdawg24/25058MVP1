import MainWindow
import SerialWorker
import pandas as pd

class Main(object):
    def setUp(self):
        self.df = pd.DataFrame(columns= ["Time", "Temp", "Distance"])

        self.serial_thread = SerialWorker.SerialWorker('COM5', 9600)
        self.serial_thread.start()
        self.serial_thread.data_received.connect(self.processData)

        # self.serial_thread2 = SerialWorker.SerialWorker('COM5', 9600)
        # self.serial_thread2.start()
        # self.serial_thread.data_received.connect(self.processData2)

        self.main_window = MainWindow.Ui_MainWindow(self.serial_thread)

    def processData(self, data):
        
        self.df.loc[len(self.df)] = [float(data[0]), float(data[1]), float(data[2])]
        
    def processData2(self, data):
        data = data

if __name__ == "__main__":
    main = Main()
    main.setUp()