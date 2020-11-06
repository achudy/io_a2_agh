import cvlib as cv
import cv2
from cvlib.object_detection import draw_bbox
img = cv2.imread('test.png')
bbox, label, conf = cv.detect_common_objects(img)
vehicleNumber = label.count('car') + label.count('bus') + label.count('motorcycle')
output_image = draw_bbox(img, bbox, label, conf)
cv2.imwrite("/home/achudy/studia/io_a2_agh/code/test_result.png", output_image)
cv2.imshow("imag", output_image)
cv2.waitKey()
cv2.destroyAllWindows()