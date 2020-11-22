"""
This module checks the file's length and if it is longer than 2160 frames, it splits original video into pieces.
"""

import sys
import os
import cv2


def check_and_cut(video_path: str) -> [str] or str:
    """
    This function checks if len(video) > 2160 frames. If yes then split into 3 min videos
    :param video_path: input video file to process
    :return: list of videos that are at most 2160 minutes long
    """

    video_in = cv2.VideoCapture(video_path)

    total_frames = video_in.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video_in.get(cv2.CAP_PROP_FPS)
    height = int(video_in.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(video_in.get(cv2.CAP_PROP_FRAME_WIDTH))

    if total_frames <= 2160:
        video_in.release()
        return video_path
    else:
        threshold = 2160.0
        current_frame = 0.0
        video_chunk = 0
        list_of_paths = []

        out_path = video_path[:video_path.rfind("/")] + "/vehicle_finder"
        if not os.path.exists(out_path):
            os.makedirs(out_path)

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        video_out = out_path + "/chunk{:04d}.avi".format(video_chunk)
        out = cv2.VideoWriter(video_out, fourcc, fps, (width, height))

        list_of_paths.append(video_out)

        while current_frame != total_frames:
            ret, frame = video_in.read()
            current_frame = video_in.get(cv2.CAP_PROP_POS_FRAMES)

            # skip frame if error
            if not ret:
                video_in.set(1, current_frame + 1.0)
            else:
                out.write(frame)

            if current_frame == threshold:
                threshold *= 2
                video_chunk += 1

                out.release()

                video_out = out_path + "/chunk{:04d}.avi".format(video_chunk)
                out = cv2.VideoWriter(video_out, fourcc, fps, (width, height))

                list_of_paths.append(video_out)

        out.release()
        video_in.release()
        return list_of_paths


if __name__ == '__main__':
    video = sys.argv[1]
    result = check_and_cut(video)
    for chunk in result:
        print(chunk)
    # check_and_cut("path to file") for debugging
