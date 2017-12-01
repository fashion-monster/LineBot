from flask import Flask, request
from utils.reshape import reshape

import tensorflow as tf
import tensorflow.contrib.eager as tfe
import cv2
import numpy as np
app = Flask(__name__)


@app.route("/resize", methods=['POST'])
def resize():
    """
    resize method.
    Read "image_name" key and resize it.

    :return: success or failed, cv2.imwrite
    """

    image_name = request.args.get("image_path")
    image = tf.constant(np.asarray(cv2.imread(filename=image_name)))
    cropped_image = reshape(image=image, new_size=None)
    DIRECTORY='cropped/'
    return cv2.imwrite(filename=DIRECTORY+image_name, img=cropped_image)


if __name__ == '__main__':
    tfe.enable_eager_execution()
    app.run(port=9999)
