#_*_ coding:utf8 _*_

import cv2 as cv

img = cv.imread("C:\Users\liguo\Documents\python\guandong_Surface_defect_dentification_of_aluminum_profile\Data\guangdong_round1_train1_20180903\凸粉20180901101040对照样本.jpg")
cv.nameWindow("image")
cv.imshow("image", img)
cv.waitKey(0)
cv.destroyAllWindows()


