import numpy as np
import math
from collections import deque
from utils import angle

#Form Evaluator...
class FormEvaluator:
    def __init__(self, smooth_window=5):
        self.left_hist = deque(maxlen=smooth_window)
        self.right_hist = deque(maxlen=smooth_window)

    def evaluate(self, lm):
        if lm is None:
            return ["No person detected"], None, None

        # MediaPipe landmark indices
        L_SH, R_SH = 11, 12
        L_EL, R_EL = 13, 14
        L_WR, R_WR = 15, 16
        L_HP, R_HP = 23, 24

        get = lambda i: lm[i][:2]

        L_ang = angle(get(L_SH), get(L_EL), get(L_WR))
        R_ang = angle(get(R_SH), get(R_EL), get(R_WR))

        self.left_hist.append(L_ang)
        self.right_hist.append(R_ang)

        L_sm = float(np.mean(self.left_hist))
        R_sm = float(np.mean(self.right_hist))

        fb = []

        #Bicep Curls Rules
        if L_sm < 80: fb.append("Left Curl: GOOD")
        elif L_sm < 110: fb.append("Left Curl: PARTIAL")
        else: fb.append("Left Curl: INCOMPLETE")

        if R_sm < 80: fb.append("Right Curl: GOOD")
        elif R_sm < 110: fb.append("Right Curl: PARTIAL")
        else: fb.append("Right Curl: INCOMPLETE")

        #Squat Check...
        L_KN, R_KN = 25, 26  # knee points
        L_AN, R_AN = 27, 28  # ankle points

        left_squat_angle = angle(get(L_HP), get(L_KN), get(L_AN))
        right_squat_angle = angle(get(R_HP), get(R_KN), get(R_AN))

        if left_squat_angle < 95 and right_squat_angle < 95:
            fb.append("Squat Depth: Good")
        else:
            fb.append("Squat Depth: Shallow")


        #Pushup Body Line Check...
        body_line_angle = angle(get(L_SH), get(L_HP), get(L_AN))
        if body_line_angle < 15:
            fb.append("Push-Up Form: Straight Body")
        else:
            fb.append("Push-Up Form: Not A Good Form")


        #Torso Symmetry...
        def slope(p1, p2):
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            return dy / (dx + 1e-8)

        ls, rs = get(L_SH), get(R_SH)
        lh, rh = get(L_HP), get(R_HP)

        sh_slope = slope(ls, rs)
        hp_slope = slope(lh, rh)

        sh_angle = abs(math.degrees(math.atan(sh_slope)))
        hp_angle = abs(math.degrees(math.atan(hp_slope)))
        torso_diff = abs(sh_angle - hp_angle)

        if torso_diff > 12:
            fb.append(f"Torso Tilt Detected ({torso_diff:.1f}°)")
        else:
            fb.append("Torso Stable")

        #Lateral Raise Rule...
        torso_h = abs(ls[1] - lh[1]) + 1e-6

        if abs(get(L_WR)[1] - ls[1]) < 0.25 * torso_h:
            fb.append("Left Raise: Level")
        else:
            fb.append("Left Raise: Not Level")

        if abs(get(R_WR)[1] - rs[1]) < 0.25 * torso_h:
            fb.append("Right Raise: Level")
        else:
            fb.append("Right Raise: Not Level")

        return fb, L_sm, R_sm

