import cv2
import mediapipe as mp

# Initialize Mediapipe pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils


def detect_batsman_orientation(video_path, frames_to_analyze=10):
    cap = cv2.VideoCapture(video_path)

    # Variables to store orientation counts
    left_hand_count = 0
    right_hand_count = 0
    total_frames_analyzed = 0

    while total_frames_analyzed < frames_to_analyze:
        ret, frame = cap.read()

        if not ret:
            break  # End of video or problem reading the frame

        # Convert the frame to RGB because MediaPipe expects RGB input
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with the MediaPipe Pose model
        result = pose.process(frame_rgb)

        if not result.pose_landmarks:
            continue  # Skip this frame if no landmarks are detected

        # Extract relevant landmarks
        landmarks = result.pose_landmarks.landmark

        # Get the x-coordinates of the wrists and shoulders
        left_wrist_x = landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x
        right_wrist_x = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x
        left_shoulder_x = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x
        right_shoulder_x = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x
        nose_x = landmarks[mp_pose.PoseLandmark.NOSE].x

        # Logic to determine if the left or right hand is closer to the nose (body center)
        # Check wrist position relative to nose
        if left_wrist_x < nose_x < right_wrist_x:
            left_hand_count += 1
        elif right_wrist_x < nose_x < left_wrist_x:
            right_hand_count += 1
        else:
            # Additional check: analyze shoulders relative to the nose
            if left_shoulder_x < nose_x < right_shoulder_x:
                left_hand_count += 1
            elif right_shoulder_x < nose_x < left_shoulder_x:
                right_hand_count += 1

        total_frames_analyzed += 1
        # Draw pose landmarks on the frame
        mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Display the frame with landmarks
        cv2.imshow('Batsman Orientation Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

    # Final decision based on the counts of detected left/right-hand orientations
    if left_hand_count > right_hand_count:
        return "Left-Handed"
    elif right_hand_count > left_hand_count:
        return "Right-Handed"
    else:
        return "Unknown"


if __name__ == "__main__":
    # Test with a sample video file
    orientation = detect_batsman_orientation("sample_batting_video.mp4", frames_to_analyze=10)
    print(f"Batsman Orientation: {orientation}")
