import cv2
import mediapipe as mp
import math


class HandTracker:

    def __init__(
            self,
            mode=False,
            maxHands=2,
            detectionCon=0.8,
            trackCon=0.8):

        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )

        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        self.results = self.hands.process(imgRGB)

        hands = []

        if self.results.multi_hand_landmarks:

            for handLms, handedness in zip(
                    self.results.multi_hand_landmarks,
                    self.results.multi_handedness):

                self.mpDraw.draw_landmarks(
                    img,
                    handLms,
                    self.mpHands.HAND_CONNECTIONS
                )

                lmList = []

                h, w, c = img.shape

                for lm in handLms.landmark:

                    cx = int(lm.x * w)
                    cy = int(lm.y * h)

                    lmList.append((cx, cy))

                hands.append({

                    "label": handedness.classification[0].label,

                    "lmList": lmList

                })

        return hands

    def pinchDistance(self, hand):

        thumb = hand["lmList"][4]

        index = hand["lmList"][8]

        x1, y1 = thumb
        x2, y2 = index

        return math.hypot(x2 - x1, y2 - y1)

    def isPinching(self, hand, threshold=40):

        return self.pinchDistance(hand) < threshold

    def getIndexFinger(self, hand):

        return hand["lmList"][8]