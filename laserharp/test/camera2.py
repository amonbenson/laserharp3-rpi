from picamera import PiCamera
import numpy as np
import cv2


camera = PiCamera()

# setup resolution and framerate
camera.resolution = (320, 240)
camera.framerate = 30

# disable automatic controls
camera.exposure_mode = 'off'
camera.awb_mode = 'off'

# set manual parameters
camera.brightness = 50
camera.contrast = 0
camera.sharpness = 0
camera.saturation = 0
camera.iso = 800
camera.shutter_speed = 30000
camera.exposure_compensation = 0
camera.awb_gains = (1, 1)

# initialize image buffer
yuv = np.empty((int(240 * 1.5), 320), dtype=np.uint8)

# main loop
for _ in camera.capture_continuous(yuv, format='yuv', use_video_port=True):
    # extract luminance channel
    luminance = yuv[:240, :]

    # preprocess and extract contours
    thresh = cv2.threshold(luminance, 200, 255, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

    # compute centers
    centers = []
    if contours is not None:
        for contour in contours:
            (x, y, w, h) = cv2.boundingRect(contour)
            centers.append((x + w / 2, y + h / 2))

    visu = cv2.cvtColor(luminance, cv2.COLOR_GRAY2BGR)
    for center in centers:
        cv2.circle(visu, (int(center[0]), int(center[1])), 5, (0, 0, 255), -1)
    cv2.imshow('frame', visu)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
