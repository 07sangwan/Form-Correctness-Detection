import cv2
import numpy as np


#On-video background text...
def draw_text_with_bg(img, text, pos, font=cv2.FONT_HERSHEY_SIMPLEX,
                      scale=0.7, color=(255,255,255), thickness=2,
                      bg_color=(0,0,0), alpha=0.6, padding=6):

    x, y = map(int, pos)
    (w, h), baseline = cv2.getTextSize(text, font, scale, thickness)

    x1 = x - padding
    y1 = y - h - padding
    x2 = x + w + padding
    y2 = y + baseline + padding

    overlay = img.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), bg_color, -1)
    img[:] = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

    cv2.putText(img, text, (x, y), font, scale, color, thickness, cv2.LINE_AA)

#Angle Function...
def angle(a, b, c):
    a = np.array(a[:2]); b = np.array(b[:2]); c = np.array(c[:2])
    ba = a - b; bc = c - b
    denom = (np.linalg.norm(ba) * np.linalg.norm(bc)) + 1e-8
    if denom == 0:
        return 0
    cos = np.dot(ba, bc) / denom
    cos = float(np.clip(cos, -1, 1))
    return float(np.degrees(np.arccos(cos)))
