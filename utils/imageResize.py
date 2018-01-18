# coding=utf-8
import cv2


# 画像pathを入力として、300*300にリサイズした画像をリサイズ済みフォルダに保存する
def resizeImage(img_path):
    src_img = cv2.imread("tmp/origin/" + img_path)
    resize_img = cv2.resize(src_img, (300, 300))
    return cv2.imwrite('tmp/dst/' + img_path, resize_img)
