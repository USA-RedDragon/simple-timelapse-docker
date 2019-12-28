import os
import signal
import time

import requests
import cv2


def cleanup():
    print('Concatenating images into a timelapse')
    try:
        concat()
    except Exception as e:
        print(e)
    for f in os.listdir('images/'):
        if f.isdigit():
            os.unlink(f'images/{f}')
    exit(0)


signal.signal(signal.SIGTERM, cleanup)


def main():
    framecount = 0
    try:
        while True:
            start = time.time()
            image_response = requests.get(os.getenv('IMAGE_URL'), verify=False)
            if image_response.status_code == 200:
                with open(f'images/{framecount}', 'wb') as fd:
                    for chunk in image_response.iter_content(chunk_size=512):
                        fd.write(chunk)
                framecount += 1
            time.sleep(60-((time.time())-start))
    except KeyboardInterrupt:
        cleanup()


def concat():
    images = []
    for f in os.listdir('images/'):
        if f.isdigit():
            images.append(f'images/{f}')
    images.sort(key=lambda f: int(f.split('/')[1]))

    frame = cv2.imread(images[0])
    cv2.imshow('video', frame)
    height, width, channels = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    timestamp = time.time()
    out = cv2.VideoWriter(f'video/timelapse-{timestamp}.mp4', fourcc, 20.0, (width, height))

    for image in images:
        frame = cv2.imread(image)
        out.write(frame)
        cv2.imshow('video', frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            break

    out.release()
    cv2.destroyAllWindows()
    print(f'The output video is video/timelapse.mp4')


if __name__ == "__main__":
    main()
