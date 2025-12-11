import cv2
import mediapipe as mp
import pandas as pd
from evaluator import FormEvaluator
from utils import draw_text_with_bg

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils


# Video Processing...
def process_video(input_path, output_path="processed.mp4"):
    pose = mp_pose.Pose(min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    w = int(cap.get(3)) or 640
    h = int(cap.get(4)) or 480

    out = cv2.VideoWriter(output_path,
                          cv2.VideoWriter_fourcc(*"mp4v"),
                          fps, (w, h))

    evaluator = FormEvaluator()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = pose.process(rgb)

        lm = None
        if res.pose_landmarks:
            lm = [[p.x*w, p.y*h, p.z, p.visibility] for p in res.pose_landmarks.landmark]

        fb, L_ang, R_ang = evaluator.evaluate(lm)

        if res.pose_landmarks:
            mp_drawing.draw_landmarks(frame, res.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        y = 30
        for line in fb:
            draw_text_with_bg(frame, line, (10, y))
            y += 35

        left_elbow_text = f"Left Elbow: {L_ang:.1f}°" if L_ang is not None else "Left Elbow: N/A"
        right_elbow_text = f"Right Elbow: {R_ang:.1f}°" if R_ang is not None else "Right Elbow: N/A"

        draw_text_with_bg(frame, left_elbow_text, (10, h-60))
        draw_text_with_bg(frame, right_elbow_text, (10, h-25))

        out.write(frame)

    cap.release()
    out.release()

    return output_path
