from flask import Flask, request
from utils.reshape import reshape

import cv2
import tensorflow as tf
import tensorflow.contrib.eager as tfe
app = Flask(__name__)


@app.route("/resize", methods=['POST'])
def resize():
    """
    resize method.
    Read "image_name" key and resize it.

    :return: success or failed, cv2.imwrite
    """

    import numpy as np
    print(request)
    print(request.headers)
    print(request.data)
    image_name = request.data
    print(image_name)
    image = cv2.imread(filename='/home/hashimoto/LineBot'+image_name)
    print("this is an image value:", image)
    if image is not None:
	print("image!!",type(image), image.shape)
        image = tf.constant(image)
        cropped_image = reshape(image=image, new_size=None)
        DIRECTORY='/home/hashimoto/LineBot/tmp/cropped/'
        print(cv2.imwrite(filename=DIRECTORY+image_name, img=cropped_image.numpy()))
        return "Success"
    else:
        write_result = False
        return "Failed"


if __name__ == '__main__':
    tfe.enable_eager_execution()
    app.debut=True
    app.run(port=9999)
