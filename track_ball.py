import cv2
import numpy as np

def track_ball_trajectory(video_path):
    cap = cv2.VideoCapture(video_path)
    trajectories = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Preprocessing
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # Define color range for the ball (assuming the ball is red)
        lower_color = np.array([0, 120, 70])
        upper_color = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv, lower_color, upper_color)

        lower_color = np.array([170, 120, 70])
        upper_color = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_color, upper_color)

        mask = mask1 | mask2
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Find contours
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        center = None

        if contours:
            # Find the largest contour assuming it's the ball
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            if radius > 5:
                center = (int(x), int(y))
                trajectories.append(center)

        # Optional: visualize tracking
            cv2.circle(frame, center, int(radius), (0, 255, 255), 2)
            cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    # cv2.destroyAllWindows()

    return trajectories
