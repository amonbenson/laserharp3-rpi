from picamera import PiCamera
import numpy as np
import cv2


class Sensor:
    def __init__(self, resolution=(320, 240), framerate=60):
        # set parameters
        self.resolution = np.array(resolution).reshape(2)
        self.framerate = int(framerate)

        # setup camera
        self.camera = PiCamera()
        self.camera.resolution = self.resolution
        self.camera.framerate = self.framerate

        # disable automatic controls
        self.camera.exposure_mode = 'off'
        self.camera.awb_mode = 'off'

        # set manual parameters
        self.camera.brightness = 50
        self.camera.contrast = 0
        self.camera.sharpness = 0
        self.camera.saturation = 0
        self.camera.iso = 800
        self.camera.shutter_speed = 30000
        self.camera.exposure_compensation = 0
        self.camera.awb_gains = (1, 1)

        # initialize buffers
        self.yuv = np.empty((int(self.resolution[1] * 1.5), self.resolution[0]), dtype=np.uint8)
        self.luminance = None
        self.thresh = None
        self.centers = []

    def capture(self):
        # capture image and extract luminance channel
        self.camera.capture(self.yuv, format='yuv', use_video_port=True)
        self.luminance = self.yuv[:self.resolution[1], :]

        # preprocess and extract contours
        self.thresh = cv2.threshold(self.luminance, 200, 255, cv2.THRESH_BINARY)[1]
        contours = cv2.findContours(self.thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        # get the blob centers
        self.centers = []
        if contours is not None:
            for contour in contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                self.centers.append((x + w / 2, y + h / 2))
        return self.centers
