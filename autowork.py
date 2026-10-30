"""Capture one photo from the default camera, then close the camera."""

import time
from pathlib import Path

import cv2


def main() -> None:
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        camera.release()
        raise RuntimeError("Could not open the default camera.")

    try:
        # Give the camera a moment to initialize before capturing.
        time.sleep(2)
        success, frame = camera.read()
        if not success:
            raise RuntimeError("Could not capture an image from the camera.")

        photo_path = Path.cwd() / "photo.jpg"
        if not cv2.imwrite(str(photo_path), frame):
            raise RuntimeError(f"Could not save the photo to {photo_path}.")

        print(f"Photo saved to: {photo_path}")
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()