import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from scipy import signal
import os

# Code adapted from
# adeveloperdiary.com/data-science/computer-vision/applying-gaussian-smoothing-to-an-image-using-python-from-scratch/

def convolve(image, kernel, average=False, verbose=False):

    y = image

    image_row, image_col = y.shape
    kernel_row, kernel_col = kernel.shape

    output = np.zeros(y.shape)

    pad_height = int((kernel_row - 1) / 2)
    pad_width = int((kernel_col - 1) / 2)

    padded_image = np.zeros((image_row + (2 * pad_height), image_col + (2 * pad_width)))

    padded_image[pad_height:padded_image.shape[0] - pad_height, pad_width:padded_image.shape[1] - pad_width] = y

    for row in range(image_row):
        for col in range(image_col):
            output[row, col] = np.sum(kernel * padded_image[row:row + kernel_row, col:col + kernel_col])
            if average:
                output[row, col] /= kernel.shape[0] * kernel.shape[1]

    if verbose:
        plt.imshow(output, cmap='gray')
        plt.title("Output Image using {}X{} Kernel".format(kernel_row, kernel_col))
        plt.show()

    return output


def dnorm(x, mu, sd):
    return 1 / (np.sqrt(2 * np.pi) * sd) * np.e ** (-np.power((x - mu) / sd, 2) / 2)

def gaussian_kernel(size, sigma=1, verbose=False):
    kernel_1D = np.linspace(-(size // 2), size // 2, size)
    for i in range(size):
        kernel_1D[i] = dnorm(kernel_1D[i], 0, sigma)
    kernel_2D = np.outer(kernel_1D.T, kernel_1D.T)

    kernel_2D *= 1.0 / kernel_2D.max()

    return kernel_2D

def gaussian_blur(image, kernel_size, sigma=2, verbose=False, optimize=True):
    kernel = gaussian_kernel(kernel_size, sigma=sigma, verbose=verbose)
    if optimize:
        return signal.convolve2d(image, kernel)
    return convolve(image, kernel, average=True, verbose=verbose)

def gradient_magnitude_direction(image, verbose=False):
    # Using a scharr kernel
    scharr = np.array([
        [47, 162, 47],
        [0, 0, 0],
        [-47, -162, -47]
    ])

    x = convolve(image, scharr)
    y = convolve(image, scharr.T)

    magnitude = np.sqrt(np.square(x) + np.square(y))
    magnitude *= 255.0 / magnitude.max()

    direction = np.arctan2(x, y)
    direction = np.rad2deg(direction)
    direction += 180

    if verbose:
        plt.imshow(direction, cmap="gray")
        plt.show()

    return magnitude, direction

def non_max_suppression(gradient_magnitude, gradient_direction, verbose=False):
    image_row, image_col = gradient_magnitude.shape
    output = np.zeros(gradient_magnitude.shape)

    PI = 180

    for row in range(1, image_row - 1):
        for col in range(1, image_col - 1):
            direction = gradient_direction[row, col]

            if (0 <= direction < PI / 8) or (15 * PI / 8 <= direction <= 2 * PI):
                before_pixel = gradient_magnitude[row, col - 1]
                after_pixel = gradient_magnitude[row, col + 1]

            elif (PI / 8 <= direction < 3 * PI / 8) or (9 * PI / 8 <= direction < 11 * PI / 8):
                before_pixel = gradient_magnitude[row + 1, col - 1]
                after_pixel = gradient_magnitude[row - 1, col + 1]

            elif (3 * PI / 8 <= direction < 5 * PI / 8) or (11 * PI / 8 <= direction < 13 * PI / 8):
                before_pixel = gradient_magnitude[row - 1, col]
                after_pixel = gradient_magnitude[row + 1, col]

            else:
                before_pixel = gradient_magnitude[row - 1, col - 1]
                after_pixel = gradient_magnitude[row + 1, col + 1]

            if gradient_magnitude[row, col] >= before_pixel and gradient_magnitude[row, col] >= after_pixel:
                output[row, col] = gradient_magnitude[row, col]

    if verbose:
        plt.imshow(output, cmap='gray')
        plt.title("Non Max Suppression")
        plt.show()

    return output


def threshold(image, low, high, weak=100, verbose=False):
    output = np.zeros(image.shape)
    strong = 255

    strong_row, strong_col = np.where(image >= high)
    weak_row, weak_col = np.where((image <= high) & (image >= low))

    output[strong_row, strong_col] = strong
    output[weak_row, weak_col] = weak

    if verbose:
        plt.imshow(output, cmap='gray')
        plt.title("threshold")
        plt.show()

    return output


def hysteresis(image, weak=100, verbose=False):
    image_row, image_col = image.shape
    top_to_bottom = image.copy()

    for row in range(1, image_row):
        for col in range(1, image_col):
            if top_to_bottom[row, col] == weak:
                if top_to_bottom[row, col + 1] == 255 or top_to_bottom[row, col - 1] == 255 or top_to_bottom[
                    row - 1, col] == 255 or top_to_bottom[
                    row + 1, col] == 255 or top_to_bottom[
                    row - 1, col - 1] == 255 or top_to_bottom[row + 1, col - 1] == 255 or top_to_bottom[
                    row - 1, col + 1] == 255 or top_to_bottom[
                    row + 1, col + 1] == 255:
                    top_to_bottom[row, col] = 255
                else:
                    top_to_bottom[row, col] = 0

    bottom_to_top = image.copy()

    for row in range(image_row - 1, 0, -1):
        for col in range(image_col - 1, 0, -1):
            if bottom_to_top[row, col] == weak:
                if bottom_to_top[row, col + 1] == 255 or bottom_to_top[row, col - 1] == 255 or bottom_to_top[
                    row - 1, col] == 255 or bottom_to_top[
                    row + 1, col] == 255 or bottom_to_top[
                    row - 1, col - 1] == 255 or bottom_to_top[row + 1, col - 1] == 255 or bottom_to_top[
                    row - 1, col + 1] == 255 or bottom_to_top[
                    row + 1, col + 1] == 255:
                    bottom_to_top[row, col] = 255
                else:
                    bottom_to_top[row, col] = 0

    right_to_left = image.copy()

    for row in range(1, image_row):
        for col in range(image_col - 1, 0, -1):
            if right_to_left[row, col] == weak:
                if right_to_left[row, col + 1] == 255 or right_to_left[row, col - 1] == 255 or right_to_left[
                    row - 1, col] == 255 or right_to_left[
                    row + 1, col] == 255 or right_to_left[
                    row - 1, col - 1] == 255 or right_to_left[row + 1, col - 1] == 255 or right_to_left[
                    row - 1, col + 1] == 255 or right_to_left[
                    row + 1, col + 1] == 255:
                    right_to_left[row, col] = 255
                else:
                    right_to_left[row, col] = 0

    left_to_right = image.copy()

    for row in range(image_row - 1, 0, -1):
        for col in range(1, image_col):
            if left_to_right[row, col] == weak:
                if left_to_right[row, col + 1] == 255 or left_to_right[row, col - 1] == 255 or left_to_right[
                    row - 1, col] == 255 or left_to_right[
                    row + 1, col] == 255 or left_to_right[
                    row - 1, col - 1] == 255 or left_to_right[row + 1, col - 1] == 255 or left_to_right[
                    row - 1, col + 1] == 255 or left_to_right[
                    row + 1, col + 1] == 255:
                    left_to_right[row, col] = 255
                else:
                    left_to_right[row, col] = 0

    final_image = top_to_bottom + bottom_to_top + right_to_left + left_to_right

    final_image[final_image > 255] = 255

    if verbose:
        plt.imshow(final_image, cmap='gray')
        plt.title("Hysteresis")
        plt.show()

    return final_image

def canny(imagestr, verbose=False, megaVerbose=False,
          kernel_size=15, sigma=5,
          low=2, high=5,
          size=None, optimize=True): # size = (x, y)

    image = Image.open(imagestr)
    if size:
        image = image.resize(size)
    image = image.convert("L")

    y = np.asarray(image.getdata(), dtype=np.float64).reshape(image.size[1], image.size[0])

    blur = gaussian_blur(y, kernel_size=kernel_size, sigma=sigma, verbose=megaVerbose)
    mag, d = gradient_magnitude_direction(blur, verbose=megaVerbose)
    nms = non_max_suppression(mag, d, verbose=megaVerbose)
    thr = threshold(nms, low, high, verbose=megaVerbose)
    hys = hysteresis(thr, verbose=megaVerbose)

    im = Image.fromarray(np.asarray(hys, dtype=np.uint8), mode="L")

    # Crop away the padded edge
    amt = kernel_size // 2
    im = im.crop( (0 + amt, 0 + amt, im.size[0] - amt, im.size[1] - amt) )
    hys = hys[amt:-amt, amt:-amt]

    im.save("EdgeDetector.png", "PNG")
    image.close()
    im.close()

    if verbose:
        fig, axs = plt.subplots(2, 3)
        axs[0, 0].imshow(y, cmap="gray")
        axs[0, 0].set_title("0 Original")
        axs[0, 1].imshow(blur, cmap="gray")
        axs[0, 1].set_title("1 Blur")
        axs[0, 2].imshow(mag, cmap="gray")
        axs[0, 2].set_title("2 Mag")
        axs[1, 0].imshow(nms, cmap="gray")
        axs[1, 0].set_title("3 Non Max Sup")
        axs[1, 1].imshow(thr, cmap="gray")
        axs[1, 1].set_title("4 Threshold")
        axs[1, 2].imshow(hys, cmap="gray")
        axs[1, 2].set_title("5 Hysteresis")
        plt.show()

    return hys


if __name__ == '__main__':

    impath = os.path.join(os.path.dirname(__file__), "Images/Valve.png")

    a = canny(impath, False, kernel_size=11, sigma=4, low = 20, high = 40)

    # plt.imshow(a, cmap="gray")
    # plt.show()



