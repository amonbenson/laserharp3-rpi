import cv2


# initialize camera
vid = cv2.VideoCapture(0)

# main loop
while True:
    ret, frame = vid.read()
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# cleanup
vid.release()
cv2.destroyAllWindows()
