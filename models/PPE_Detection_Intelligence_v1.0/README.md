# Construction PPE Detection Intelligence v1.0

## Purpose

YOLO11n-based object detection model for construction-site
Personal Protective Equipment (PPE) monitoring.

## Supported Classes

0. helmet
1. gloves
2. vest
3. boots
4. goggles
5. none
6. Person
7. no_helmet
8. no_goggle
9. no_gloves
10. no_boots

## Model

Architecture: YOLO11n
Task: Object Detection
Image Size: 640
Training Epochs: 50

## Test Performance

Precision: 58.01%
Recall: 53.71%
mAP50: 54.33%
mAP50-95: 27.16%

## Validation Performance

Precision: 71.8%
Recall: 54.6%
mAP50: 59.3%
mAP50-95: 29.3%

## Important

The model performs better on PPE-present classes such as
helmet, vest, gloves and boots.

Missing-PPE classes require further improvement, especially
no_boots, no_gloves and no_goggle.

Therefore this version should be considered a research/prototype
model rather than a production-certified safety system.

## Backend Integration

The main model file is:

models/ppe_detection_best.pt

The backend can load the model using Ultralytics YOLO.
