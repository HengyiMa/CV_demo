
### Supporting code for Computer Vision Assignment 1
### See "Assignment 1.ipynb" for instructions

import math

import numpy as np
from skimage import io

def load(img_path):
    """Loads an image from a file path.

    HINT: Look up `skimage.io.imread()` function.
    HINT: Converting all pixel values to a range between 0.0 and 1.0
    (i.e. divide by 255) will make your life easier later on!

    Inputs:
        image_path: file path to the image.

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """
    

    image = io.imread(img_path)
    out=image
    
    return out

def print_stats(image):
    """ Prints the height, width and number of channels in an image.
        
    Inputs:
        image: numpy array of shape(image_height, image_width, n_channels).
        
    Returns: none
                
    """
    
    # YOUR CODE HERE
    height, width, channels = image.shape
    print("Height:", height)
    print("Width:", width)
    print("Channels:", channels)
    return None

def crop(image, start_row, start_col, num_rows, num_cols):
    """Crop an image based on the specified bounds. Use array slicing.

    Inputs:
        image: numpy array of shape(image_height, image_width, 3).
        start_row (int): The starting row index 
        start_col (int): The starting column index 
        num_rows (int): Number of rows in our cropped image.
        num_cols (int): Number of columns in our cropped image.

    Returns:
        out: numpy array of shape(num_rows, num_cols, 3).
    """


    ### YOUR CODE HERE
    out = image[start_row:start_row + num_rows, start_col:start_col + num_cols,:]

    return out


def change_contrast(image, factor):
    """Change the value of every pixel by following

                        x_n = factor * (x_p - 0.5) + 0.5

    where x_n is the new value and x_p is the original value.
    Assumes pixel values between 0.0 and 1.0 
    If you are using values 0-255, change 0.5 to 128.

    Inputs:
        image: numpy array of shape(image_height, image_width, 3).
        factor (float): contrast adjustment

    Returns:
        out: numpy array of shape(image_height, image_width, 3).
    """



    ### YOUR CODE HERE
    input_rows, input_cols, channels =  image.shape
    out = np.zeros((input_rows, input_cols, channels), dtype=np.uint8)
    for row in range(input_rows):
        for column in range(input_cols):
            out[row,column]=factor*(image[row,column]-0.5)+0.5

    return out


def resize(input_image, output_rows, output_cols):
    """Resize an image using the nearest neighbor method.
    i.e. for each output pixel, use the value of the nearest input pixel after scaling

    Inputs:
        input_image: RGB image stored as an array, with shape
            `(input_rows, input_cols, 3)`.
        output_rows (int): Number of rows in our desired output image.
        output_cols (int): Number of columns in our desired output image.

    Returns:
        np.ndarray: Resized image, with shape `(output_rows, output_cols, 3)`.
    """
    input_rows, input_cols, channels = input_image.shape
    rows=int(input_rows*output_rows)
    columns=int(input_cols*output_cols)
    out = np.zeros((rows, columns, channels), dtype=np.uint8)
    for row in range(rows):
        for col in range(columns):
            input_row = int(row / output_rows)
            input_col = int(col / output_cols)
            out[row, col] = input_image[input_row, input_col]
    return out

def greyscale(input_image):
    """Convert a RGB image to greyscale. 
    A simple method is to take the average of R, G, B at each pixel.
    Or you can look up more sophisticated methods online.
    
    Inputs:
        input_image: RGB image stored as an array, with shape
            `(input_rows, input_cols, 3)`.

    Returns:
        np.ndarray: Greyscale image, with shape `(output_rows, output_cols)`.
    """
    out=np.mean(input_image, axis=2,keepdims=True)
    return out

def binary(grey_img, th):
    """Convert a greyscale image to a binary mask with threshold.

                  x_n = 0, if x_p < th
                  x_n = 1, if x_p > th

    Inputs:
        input_image: Greyscale image stored as an array, with shape
            `(image_height, image_width)`.
        th (float): The threshold used for binarization, and the value range is 0 to 1
    Returns:
        np.ndarray: Binary mask, with shape `(image_height, image_width)`.
    """
    input_rows, input_cols,channels = grey_img.shape
    out = np.zeros((input_rows, input_cols,channels), dtype=np.uint8)
    for row in range(input_rows):
        for column in range(input_cols):
            if grey_img[row,column]/255>th:
                out[row,column]=1
            else:
                out[row,column]=0  
    return out

def conv2D(image, kernel):
    """ Convolution of a 2D image with a 2D kernel. 
    Convolution is applied to each pixel in the image.
    Assume values outside image bounds are 0.
    
    Args:
        image: numpy array of shape (Hi, Wi).
        kernel: numpy array of shape (Hk, Wk). Dimensions will be odd.

    Returns:
        out: numpy array of shape (Hi, Wi).
    """
    out = None
    ### YOUR CODE HERE
    ckernel = np.rot90(kernel, 2)
    input_rows, input_cols = image.shape
    kernel_rows, kernel_cols = ckernel.shape
    out = np.zeros((input_rows, input_cols), dtype=np.uint8)
    paddle=np.pad(image, ((kernel_rows // 2, kernel_rows // 2), (kernel_cols // 2, kernel_cols // 2)),mode='constant')
    for row in range(input_rows):
        for col in range(input_cols):
            area = paddle[ row :row+ kernel_rows ,  col: col + kernel_cols  ]
            out[row, col] = np.sum(area * ckernel)
    return out
def test_conv2D(): #This kernel is uesd to test images with only one channel.
    """ A simple test for your 2D convolution function.
        You can modify it as you like to debug your function.
    
    Returns:
        None
    """

    # Test code written by 
    # Simple convolution kernel.
    kernel = np.array(
    [
        [1,0,1],
        [0,0,0],
        [1,0,0]
    ])

    # Create a test image: a white square in the middle
    test_img = np.zeros((9, 9))
    test_img[3:6, 3:6] = 1

    # Run your conv_nested function on the test image
    test_output = conv2D(test_img, kernel)

    # Build the expected output
    expected_output = np.zeros((9, 9))
    expected_output[2:7, 2:7] = 1
    expected_output[5:, 5:] = 0
    expected_output[4, 2:5] = 2
    expected_output[2:5, 4] = 2
    expected_output[4, 4] = 3

    # Test if the output matches expected output
    assert np.max(test_output - expected_output) < 1e-10, "Your solution is not correct."
def test_conv2D_3ch(): #This kernel is uesd to test images with 3 channels.
    kernel = np.array(
    [
        [1,0,1],
        [0,0,0],
        [1,0,0]
    ])                 #use the same kernel
    test_img = np.array([
        [[1, 0, 3], [2, 5, 2], [10, 30, 25]],
        [[10, 4, 90], [52, 35, 12], [11, 22, 15]],
        [[50, 44, 55], [23, 32,150], [205, 12, 99]]], dtype=np.uint8) #give a test image with 3 channels
    test_output = conv(test_img, kernel)
    return test_output   #since we're using same method like we does in simple conv2d, if we can get a output then it's right.
def conv(image, kernel):
    """Convolution of a RGB or grayscale image with a 2D kernel
    
    Args:
        image: numpy array of shape (Hi, Wi, 3) or (Hi, Wi)
        kernel: numpy array of shape (Hk, Wk). Dimensions will be odd.

    Returns:
        out: numpy array of shape (Hi, Wi, 3) or (Hi, Wi)
    """
    out = None
    ### YOUR CODE HERE
    ckernel = np.rot90(kernel, 2)
    input_rows, input_cols ,channels= image.shape
    kernel_rows, kernel_cols= ckernel.shape
    out = np.zeros((input_rows, input_cols,channels), dtype=np.uint8)
    for channel in range(channels):
        paddle=np.pad(image[:,:,channel],((kernel_rows // 2, kernel_rows // 2), (kernel_cols // 2, kernel_cols // 2)),mode='constant')
        for row in range(input_rows):
            for col in range(input_cols):
                area=paddle[row:row+kernel_rows,col:col+kernel_cols]
                out[row,col,channel] =np.sum(area * ckernel)
    return out
def gauss2D(size, sigma):

    """Function to mimic the 'fspecial' gaussian MATLAB function.
       You should not need to edit it.
       
    Args:
        size: filter height and width
        sigma: std deviation of Gaussian
        
    Returns:
        numpy array of shape (size, size) representing Gaussian filter
    """

    x, y = np.mgrid[-size//2 + 1:size//2 + 1, -size//2 + 1:size//2 + 1]
    g = np.exp(-((x**2 + y**2)/(2.0*sigma**2)))
    return g/g.sum()


def corr(image, kernel):
    """Cross correlation of a RGB image with a 2D kernel
    
    Args:
        image: numpy array of shape (Hi, Wi, 3) or (Hi, Wi)
        kernel: numpy array of shape (Hk, Wk). Dimensions will be odd.

    Returns:
        out: numpy array of shape (Hi, Wi, 3) or (Hi, Wi)
    """
    out = None
    ### YOUR CODE HERE
    input_rows, input_cols ,channels= image.shape
    kernel_rows, kernel_cols,channels2= kernel.shape
    out = np.zeros((input_rows, input_cols,channels), dtype=np.uint8)
    kernel_re = np.zeros_like(kernel)
    for channel in range(channels):
        channel_mean = np.mean(kernel[:, :, channel])
        kernel_re[:, :, channel] = kernel[:, :, channel]-channel_mean
        paddle=np.pad(image[:,:,channel],((kernel_rows // 2, kernel_rows // 2), (kernel_cols // 2, kernel_cols // 2)),mode='constant')
        for row in range(input_rows):
            for col in range(input_cols):
                area=paddle[row:row+kernel_rows,col:col+kernel_cols]
                out[row,col,channel] =np.sum(area *  kernel_re[:, :, channel])/255
    return out


