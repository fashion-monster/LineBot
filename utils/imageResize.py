import cv2
import numpy as np


# 画像pathを入力として、300*300にリサイズした画像をリサイズ済みフォルダに保存する
def resizeImage(img_path):
	src_img = cv2.imread(img_path)
	resize_img = cv2.resize(src_img, (300, 300))
	cv2.imwrite('tmp/dst/'+img_path, resize_img)