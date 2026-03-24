# AI-Based Knee Rehabilitation Analyzer

## Overview

This project is a real-time AI-based system that analyzes knee
rehabilitation exercises using computer vision. It detects human pose,
calculates knee joint angles, and provides feedback to improve exercise
performance.

## Features

-   Real-time pose detection using MediaPipe
-   Knee angle calculation (hip--knee--ankle)
-   Automatic repetition counter
-   Feedback system (Good / Go Lower / Stand Straight)
-   Left and right leg detection
-   Visual joint tracking (lines and keypoints)
-   Video recording of exercise session

## Tech Stack

-   Python
-   OpenCV
-   MediaPipe (Tasks API)
-   NumPy

## Demo Video

[▶️ Watch Demo](https://drive.google.com/file/d/11JNrMS6Sd4CZnkjQAkci9nqTcT0tbshF/view?usp=sharing)

If the video does not play, download it from the repository and view
locally.

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/its-kanii/AI-Knee-Rehab-Analyzer.git
cd AI-Knee-Rehab-Analyzer
```
### 2. Install dependencies
```bash
pip install opencv-python mediapipe numpy
```
### 3. Download model file

Download from:
[MediaPipe](https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/latest/pose_landmarker_lite.task)

Rename the file to:
```bash
 pose_landmarker.task
```
Place it in the project folder.

### 4. Run the project
```bash
python main.py
```
## How it Works

-   Detects human pose using MediaPipe
-   Extracts hip, knee, and ankle coordinates
-   Calculates knee joint angle in real time
-   Tracks movement to count repetitions
-   Provides feedback based on angle thresholds

## Use Cases

-   Knee rehabilitation monitoring
-   Home physiotherapy assistance
-   Fitness posture correction
-   AI-based healthcare applications

## Future Improvements

-   Detect incorrect knee alignment
-   Support multiple exercises
-   Build web interface using Streamlit
-   Integrate wearable sensor data


