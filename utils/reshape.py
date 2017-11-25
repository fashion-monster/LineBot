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
    new_height = 604
    new_width = 604
    if new_size is not None:
        try:
            new_height = new_size[0]
            new_width = new_size[1]
        except TypeError:
            raise TypeError
        except IndexError:
            raise IndexError

    reshaped = tf.image.resize_images(tf.image.resize_image_with_crop_or_pad(image, max_size, max_size),
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

    image_names = [x for x in os.listdir('original')]

    for x in image_names:
        img = reshape(tf.constant(np.asarray(cv2.imread('original/' + x))), None).numpy()
        print(cv2.imwrite(DIRECTORY + '/' + x, img))  # show T or F
