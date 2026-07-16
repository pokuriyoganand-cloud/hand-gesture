import cv2

# -----------------------------
# Keyboard Layout
# -----------------------------

LAYOUT = [
    [("Esc",1),("1",1),("2",1),("3",1),("4",1),("5",1),("6",1),("7",1),("8",1),("9",1),("0",1),("-",1),("=",1),("Backspace",3.5)],

    [("Tab",1.8),("Q",1),("W",1),("E",1),("R",1),("T",1),("Y",1),("U",1),("I",1),("O",1),("P",1),("[",1),("]",1),("\\",1.8)],

    [("Caps",2),("A",1),("S",1),("D",1),("F",1),("G",1),("H",1),("J",1),("K",1),("L",1),(";",1),("'",1),("Enter",3.2)],

    [("Shift",2.5),("Z",1),("X",1),("C",1),("V",1),("B",1),("N",1),("M",1),(",",1),(".",1),("/",1),("Shift",2.5)],

    [("Ctrl",1.5),("Win",1.5),("Alt",1.5),("Space",6),("Alt",1.5),("Ctrl",1.5)]
]

BASE_WIDTH = 36
KEY_HEIGHT = 40
GAP = 4

# Camera resolution
# Camera resolution
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

# Keyboard position (middle-right)
START_X = 650
START_Y = 180


class Button:

    def __init__(self, pos, text, size):
        self.pos = pos
        self.text = text
        self.size = size


def create_keyboard():

    buttons = []

    y = START_Y

    for row in LAYOUT:

        x = START_X

        for key, scale in row:

            width = int(BASE_WIDTH * scale + GAP * (scale - 1))

            buttons.append(
                Button(
                    [x, y],
                    key,
                    [width, KEY_HEIGHT]
                )
            )

            x += width + GAP

        y += KEY_HEIGHT + GAP

    return buttons


def draw_glass(img, x, y, w, h):

    if x < 0 or y < 0:
        return

    if x+w > img.shape[1]:
        return

    if y+h > img.shape[0]:
        return

    roi = img[y:y+h, x:x+w]

    blur = cv2.GaussianBlur(roi, (41,41), 0)

    overlay = blur.copy()

    cv2.addWeighted(
        blur,
        0.90,
        overlay,
        0.10,
        0,
        roi
    )

    cv2.rectangle(
        img,
        (x,y),
        (x+w,y+h),
        (255,255,255),
        2
    )

def draw_keyboard(img, buttons, hover=None):

    min_x = min(b.pos[0] for b in buttons)
    min_y = min(b.pos[1] for b in buttons)

    max_x = max(b.pos[0] + b.size[0] for b in buttons)
    max_y = max(b.pos[1] + b.size[1] for b in buttons)

    draw_glass(
        img,
        min_x - 10,
        min_y - 10,
        (max_x - min_x) + 20,
        (max_y - min_y) + 20
    )

    for button in buttons:

        x, y = button.pos
        w, h = button.size

        color = (255,255,255)

        if hover == button:

            overlay = img[y:y+h, x:x+w].copy()

            fill = overlay.copy()
            fill[:] = (120,220,255)

            img[y:y+h,x:x+w] = cv2.addWeighted(
                overlay,
                0.7,
                fill,
                0.3,
                0
            )

            color = (0,255,255)

        cv2.rectangle(img,(x,y),(x+w,y+h),color,2)

        text_size = cv2.getTextSize(
            button.text,
            cv2.FONT_HERSHEY_DUPLEX,
            0.55,
            2
        )[0]

        tx = x + (w-text_size[0])//2
        ty = y + (h+text_size[1])//2

        cv2.putText(
            img,
            button.text,
            (tx,ty),
            cv2.FONT_HERSHEY_DUPLEX,
            0.55,
            (255,255,255),
            2
        )


        tx = x + (w-text_size[0])//2
        ty = y + (h+text_size[1])//2

        cv2.putText(
            img,
            button.text,
            (tx,ty),
            cv2.FONT_HERSHEY_PLAIN,
            0.55,
            (255,255,255),
            1
        )