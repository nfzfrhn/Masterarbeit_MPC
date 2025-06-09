from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
import sys
import time

class progressBar(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Computing MPC...")
        self.setFixedSize(300, 100)
        self.setWindowIcon(qtg.QIcon('icon/loading.png'))
        self.mainLayout = qtw.QVBoxLayout()
        self.progBar = qtw.QProgressBar()
        self.progBar.setMaximum(100)
        self.progBar.setMinimum(0)
        self.text = qtw.QLabel("Please wait while MPC is running...")
        self.mainLayout.addWidget(self.text)
        self.mainLayout.addWidget(self.progBar)
        self.setLayout(self.mainLayout)
        #self.show()

    def update_progress(self, pValue):
        self.progBar.setValue(pValue)
        qtw.QApplication.processEvents()

        if pValue == self.progBar.maximum():
            self.progBar.hide()
            self.close()

def controller():
    pBar = progressBar()
    pBar.show()
    total_iterations = 100                                              # Total number of iterations in the loop
    for i in range(total_iterations):
        # Perform MPC calculations
        time.sleep(0.1)                                                 # Simulating some computation time
        progress_value = int((i + 1) / total_iterations * 100)          # Calculate progress value
        pBar.update_progress(progress_value)
    pBar.close()
    a = 1
    return a

if __name__ == '__main__':
    app = qtw.QApplication([])
    c = controller()
    print(c)
    app.quit()
    sys.exit(app.exec_())