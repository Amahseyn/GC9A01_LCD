import cv2
import os

def save_frames(video_path, output_folder, frames_per_second=10):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate the interval between frames to achieve the desired frames per second
    interval = int(round(fps / frames_per_second))

    # Loop through frames with the specified interval
    for i in range(0, frame_count, interval):
        # Set the video capture object to the current frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)

        # Read the frame
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame to 256x256
        resized_frame = cv2.resize(frame, (256, 256))

        # Save the resized frame to the output folder
        frame_filename = f"{output_folder}/frame_{i+1:04d}.jpg"
        cv2.imwrite(frame_filename, resized_frame)

    # Release the video capture object
    cap.release()

if __name__ == "__main__":
    # Specify the path to your video file
    video_path = "1.mp4"

    # Specify the output folder for resized frames
    output_folder = "frames"

    # Call the function to save frames (10 frames per second)
    save_frames(video_path, output_folder, frames_per_second=10)
