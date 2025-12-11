# Form Correctness Detection Pipeline

This project implements a lightweight posture-analysis system using MediaPipe Pose, designed to evaluate exercise form across multiple movements such as bicep curls, lateral raises, squats, and push-ups.
It extracts keypoints, computes joint angles, applies rule-based logic, and generates frame-wise feedback directly on the processed video.

# Project Overview

The goal of this project is to build a form-correctness detection pipeline capable of identifying common mistakes in basic exercises.
The system uses MediaPipe for real-time keypoint extraction and combines it with a set of rule-based checks to determine whether the user's form is correct.

The pipeline is designed to be simple, extendable, and suitable for beginner/intermediate ML or CV projects.

# Objectives

* Detect human pose keypoints using MediaPipe (or any open-source alternative).

* Extract angles from joints to evaluate posture.

* Apply at least three rule-based checks, including:

* * Elbow angle during bicep curls

* * Wrist-shoulder alignment during lateral raises

* * Torso stability

* Provide continuous frame-wise feedback on the video.

* Support additional exercises such as squats and push-ups.

* Generate time-series angle data in CSV format.
