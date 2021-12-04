from pyupbit import WebSocketManager
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# Sample From : https://wikidocs.net/117440

class Worker(QThread):
    recv = pyqtSignal(dict)
    """
    what is dict ? ==> buit in python
        dict() -> new empty dictionary
        dict(mapping) -> new dictionary initialized from a mapping object's
            (key, value) pairs
        dict(iterable) -> new dictionary initialized as if via:
            d = {}
            for k, v in iterable:
                d[k] = v
        dict(**kwargs) -> new dictionary initialized with the name=value pairs
            in the keyword argument list.  For example:  dict(one=1, two=2)
        """

    def run(self):
        wm = WebSocketManager("ticker", ["KRW-BTC"])
        while True:
            data = wm.get()
            # print(data)
            self.recv.emit(data)



class MyWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        label = QLabel("BTC", self)
        label.move(20, 20)

        self.price = QLabel("", self)
        self.price.move(80, 20)
        self.price.move(100, 20)

        btn = QPushButton("Start", self)
        btn.move(20, 50)
        btn.clicked.connect(self.click_btn)

        self.th = Worker()
        self.th.recv.connect(self.receive_mgs)

    @pyqtSlot(dict)
    def receive_mgs(self, data):
        print(data)
        trade_price = data.get("trade_price")
        ask_bid = data.get("ask_bid")

        self.price.setText(str(trade_price))


    def click_btn(self):
        self.th.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mywondow = MyWindow()
    mywondow.show()
    app.exec_()
