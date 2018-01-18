# coding=utf-8
import requests
import os
import sys


# 画像をダウンロードする
def download_image(url, timeout=10):
    response = requests.get(url, allow_redirects=False, timeout=timeout)
    if response.status_code != 200:
        e = Exception("HTTP status: " + str(response.status_code))
        raise e

    content_type = response.headers["content-type"]
    if 'image' not in content_type:
        e = Exception("Content-Type: " + content_type)
        raise e

    return response.content


# 画像のファイル名を決める
def make_filename(base_dir, url):
    parts = url.split("/")
    filename = parts[-1]

    fullpath = base_dir + filename
    return fullpath


# 画像を保存する
def save_image(filename, image):
    with open(filename, "wb") as fout:
        fout.write(image)


# メイン
if __name__ == "__main__":
    urls_txt = "out.txt"
    images_dir = "images/"

    with open(urls_txt, "r") as fin:
        for line in fin:
            url = line.strip()
            filename = make_filename(images_dir, url)

            print("%s" % url)
            try:
                image = download_image(url)
                save_image(filename, image)
            except KeyboardInterrupt:
                break
            except Exception as err:
                print("%s" % (err))
