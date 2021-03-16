import numpy as np
import cv2 
from scipy.signal import convolve2d
import skimage.color 
from scipy import signal
import skimage.color as color
import skimage.transform as sktr
import matplotlib.pyplot as plt


# def blend(im1, im2, mask):
#   mask = mask / 255.
#   out = im1 * mask + (1-mask) * im2
#   return out


def get_gaussian_filter(img, sigma):
    w = 100
    h = 100
    x, y = np.mgrid[round(-w/2):round(w/2), round(-h/2):round(h/2)]
    f = np.exp(-x**2/(2*sigma**2)-y**2/(2*sigma**2))
    gaussian = f/f.sum()
    
    gaus = signal.fftconvolve(img, gaussian, mode='same')
    return gaus


def get_Laplacian_Stack(iimg, N):
    w = iimg.shape[0]
    h = iimg.shape[1]

    gstack = np.zeros((w,h,N))
    for x in range(0,N):
        sigma = 2**x
        img = get_gaussian_filter(iimg,sigma)
        gstack[:,:,x] = img

    w,h,n = gstack.shape
    stack = np.zeros((w,h,n))
    for x in range(0,n-1):
        img = gstack[:,:,x]-gstack[:,:,x+1]
        stack[:,:,x] = img
        if x == n-2:
            stack[:,:,x+1] = gstack[:,:,x+1]
    return stack


def get_Gaussian_Stack(iimg, N, alpha):
    w, h= iimg.shape
    stack = np.zeros((w,h,N))
    for x in range(0,N):
        sigma = (2**(x*alpha))
        img = get_gaussian_filter(iimg,sigma)
        stack[:,:,x] = img
    return stack


def blend(left, right, mask):

    N = 5
    alpha = 4

    left = left/255.
    left = color.rgb2gray(left)
    left_lstack = get_Laplacian_Stack(left, N)

    right = right/255.
    right = color.rgb2gray(right)
    right_lstack = get_Laplacian_Stack(right, N)

    mask = mask/255.
    mask = sktr.resize(mask, left.shape)
    maskg = color.rgb2gray(mask)
    mask_gstack = get_Gaussian_Stack(maskg, N, alpha)

    # Blend images
    w, h, N = mask_gstack.shape
    blend = np.zeros((w,h))

    for x in range(0,N):
        left = mask_gstack[:,:,x]*left_lstack[:,:,x]
        right = (1 - mask_gstack[:,:,x])*right_lstack[:,:,x]
        blend += left + right

    return blend  * 255.

    


