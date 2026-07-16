import numpy as np
from pynput.mouse import Controller, Button


class MouseController:

    def __init__(self):

        self.mouse = Controller()

        self.prevX = 0
        self.prevY = 0

        self.smoothing = 5

        self.screenW = 1920
        self.screenH = 1080

        self.frameR = 100

        self.clicked = False

    def move(self, x, y, camW, camH):

        x = np.interp(
            x,
            (self.frameR, camW - self.frameR),
            (0, self.screenW)
        )

        y = np.interp(
            y,
            (self.frameR, camH - self.frameR),
            (0, self.screenH)
        )

        curX = self.prevX + (x - self.prevX) / self.smoothing
        curY = self.prevY + (y - self.prevY) / self.smoothing

        self.mouse.position = (curX, curY)

        self.prevX = curX
        self.prevY = curY

    def leftClick(self):

        if self.clicked:
            return

        self.clicked = True
        self.mouse.click(Button.left)

    def rightClick(self):

        if self.clicked:
            return

        self.clicked = True
        self.mouse.click(Button.right)

    def doubleClick(self):

        if self.clicked:
            return

        self.clicked = True
        self.mouse.click(Button.left, 2)

    def release(self):

        self.clicked = False

    def scrollUp(self):

        self.mouse.scroll(0, 2)

    def scrollDown(self):

        self.mouse.scroll(0, -2)