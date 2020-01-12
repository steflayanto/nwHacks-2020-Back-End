import cv2, time

cap = cv2.VideoCapture(0)
assert cap.isOpened()
time.sleep(2)
ret, frame = cap.read(0)
if ret:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', gray)
    print(cv2.mean(gray)[0])
    cv2.waitKey(0)

cap.release()