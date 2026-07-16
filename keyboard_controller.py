from pynput.keyboard import Controller, Key

keyboard = Controller()


class KeyboardController:

    def __init__(self):
        self.clicked = False
        self.caps = False

    def release(self):
        self.clicked = False

    def press(self, key):

        # Prevent repeated presses while pinching
        if self.clicked:
            return

        self.clicked = True

        print("Pressed:", key)

        # ---------- Special Keys ----------

        if key == "Space":
            keyboard.tap(Key.space)

        elif key == "Backspace":
            keyboard.tap(Key.backspace)

        elif key == "Enter":
            keyboard.tap(Key.enter)

        elif key == "Tab":
            keyboard.tap(Key.tab)

        elif key == "Esc":
            keyboard.tap(Key.esc)

        elif key == "Caps":
            self.caps = not self.caps
            keyboard.tap(Key.caps_lock)

        elif key == "Shift":
            keyboard.tap(Key.shift)

        elif key == "Ctrl":
            keyboard.tap(Key.ctrl)

        elif key == "Alt":
            keyboard.tap(Key.alt)

        elif key == "Win":
            keyboard.tap(Key.cmd)

        # ---------- Normal Characters ----------

        else:

            text = key

            if len(text) == 1:

                if text.isalpha():

                    if self.caps:
                        keyboard.type(text.upper())
                    else:
                        keyboard.type(text.lower())

                else:
                    keyboard.type(text)