import time
import cv2
from ..sensor import Sensor


if __name__ == '__main__':
    # choose a lower framerate, because the visualization slows down the process
    sensor = Sensor(framerate=30)

    while True:
        # capture image
        t0 = time.time()
        centers = sensor.capture()
        t1 = time.time()

        # create visualization
        visu = cv2.cvtColor(sensor.luminance, cv2.COLOR_GRAY2BGR)

        # draw centers
        for center in centers:
            cv2.circle(visu, (int(center[0]), int(center[1])), 5, (0, 0, 255), -1)

        # draw fps
        fps = 1 / (t1 - t0)
        cv2.putText(visu, 'FPS: {:.2f}'.format(fps), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # show visualization
        cv2.imshow('frame', visu)
        tlast = t0

        # exit on 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
