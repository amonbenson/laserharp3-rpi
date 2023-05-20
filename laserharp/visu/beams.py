import time
import cv2
import numpy as np
from ..sensor import Sensor


if __name__ == '__main__':
    # choose a lower framerate, because the visualization slows down the process
    sensor = Sensor(framerate=30)

    thresh_max = np.zeros(np.flip(sensor.resolution), dtype=np.uint8)

    while True:
        # capture image
        t0 = time.time()
        centers = sensor.capture()
        t1 = time.time()

        thresh_max = np.logical_or(thresh_max, sensor.thresh).astype(np.uint8) * 255

        # create visualization
        visu = cv2.cvtColor(thresh_max, cv2.COLOR_GRAY2BGR)

        # show visualization
        cv2.imshow('frame', visu)
        tlast = t0

        # clear on 'c'
        if cv2.waitKey(1) & 0xFF == ord('c'):
            thresh_max = np.zeros(np.flip(sensor.resolution), dtype=np.uint8)

        # exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
