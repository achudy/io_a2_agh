import cvlib as cv
import cv2
from cvlib.object_detection import draw_bbox
import time
# img = cv2.imread('test.png')
# bbox, label, conf = cv.detect_common_objects(img)
# vehicleNumber = label.count('car') + label.count('bus') + label.count('motorcycle')
# output_image = draw_bbox(img, bbox, label, conf)
# cv2.imwrite("/home/achudy/studia/io_a2_agh/code/test_result.png", output_image)
# cv2.imshow("imag", output_image)
# cv2.waitKey()
# cv2.destroyAllWindows()


video_in = cv2.VideoCapture('C:/Users/karol/Downloads/GrupaC1.avi')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_out = cv2.VideoWriter('C:/Users/karol/Downloads/GrupaC1out.avi', fourcc, 20.0, (1920, 1080))
input_frames = []
output_frames = []
number_of_frames = 0


while video_in.isOpened():
    ret, frame = video_in.read()
    # input_frames.append(frame)
    bbox, label, conf = cv.detect_common_objects(frame)
    output_image = draw_bbox(frame, bbox, label, conf)
    video_out.write(output_image)
    print(number_of_frames)
    number_of_frames += 1

video_in.release()
video_out.release()
cv2.destroyAllWindows()
