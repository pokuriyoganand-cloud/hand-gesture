import cv2
import mediapipe as mp
import numpy as np
from pynput.keyboard import Controller

keyboard_controller = Controller()

# MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

while True:import cv2

from config import CAMERA_ID, CAMERA_WIDTH, CAMERA_HEIGHT
from keyboard_ui import create_keyboard, draw_keyboard
from hand_tracker import HandTracker
from keyboard_controller import KeyboardController
from mouse_controller import MouseController


cap = cv2.VideoCapture(CAMERA_ID)
if not cap.isOpened():
    print("Camera could not be opened!")
    exit()

print("Camera opened successfully")
cap.set(3, CAMERA_WIDTH)
cap.set(4, CAMERA_HEIGHT)

tracker = HandTracker()

buttons = create_keyboard()

keyboard = KeyboardController()
mouse = MouseController()

hover_button = None

while True:

    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)

    hands = tracker.findHands(img)

    hover_button = None

    keyboard_pinch = False

    mouse_pinch = False

    h, w, _ = img.shape

    if hands:

        for hand in hands:

            x, y = tracker.getIndexFinger(hand)

            pinching = tracker.isPinching(hand)

            # -----------------------------
            # RIGHT HAND → KEYBOARD
            # -----------------------------

            if hand["label"] == "Right":

                for button in buttons:

                    bx, by = button.pos
                    bw, bh = button.size

                    if bx <= x <= bx + bw and by <= y <= by + bh:

                        hover_button = button

                        if pinching:

                            keyboard.press(button.text)
                            keyboard_pinch = True

                        break

            # -----------------------------
            # LEFT HAND → MOUSE
            # -----------------------------

            else:

                mouse.move(x, y, w, h)

                if pinching:

                    mouse.leftClick()
                    mouse_pinch = True

    if not keyboard_pinch:
        keyboard.release()

    if not mouse_pinch:
        mouse.release()

    draw_keyboard(img, buttons, hover_button)

    cv2.imshow("Virtual Keyboard", img)

    key = cv2.waitKey(1)

    if key == 27:
        break

cap.release()

cv2.destroyAllWindows()
    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame,1)

    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    if result.multi_hand_landmarks:

        for hand in result.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

    cv2.imshow("Gesture Keyboard",frame)

    if cv2.waitKey(1)==27:
        break

cap.release()
cv2.destroyAllWindows()