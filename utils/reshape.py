import tensorflow as tf


def reshape(image, new_size):
    """
    Making gotten images regular size.
    Arg:
        image: 3-D Tensor
        new_size: [new_height, new_width]
    Return:
        reshaped: reshaped images
    """
    max_size = size_decision(image)
    new_height = 300
    new_width = 300
    if new_size is not None:
        try:
            new_height = new_size[0]
            new_width = new_size[1]
        except TypeError:
            raise TypeError
        except IndexError:
            raise IndexError

    reshaped = tf.image.resize_images(image,
                                      [new_height, new_width])
    return reshaped


def size_decision(image):
    """
    Helper function.
    Returning longer edge size.

    Arg:
        image: 3-D Tensor
    Return:
        size: longer edge size
    """
    return tf.reduce_max(tf.shape(image))


if __name__ == '__main__':
    """reshape all images under './original', and put under './copy'"""
    import os
    import cv2
    import numpy as np
    import tensorflow.contrib.eager as tfe  # Version 1.5.0 or higher

    tfe.enable_eager_execution()
    DIRECTORY = './copy'
    dirs = ["0", "1", "2"]

    for dir_name in dirs:
        for image_name in os.listdir(dir_name):
            img_full_path = dir_name + "/" + image_name
            img = reshape(image=tf.constant(np.asarray(cv2.imread(img_full_path))), new_size=None).numpy()
            print(cv2.imwrite(DIRECTORY + '/' + img_full_path, img))
