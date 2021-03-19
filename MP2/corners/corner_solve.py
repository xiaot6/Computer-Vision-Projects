import numpy as np
import scipy
import cv2
from scipy.signal import convolve2d
from scipy import signal

import cv2
import numpy as np



def compute_corners1(I): #1 original
  # Currently this code proudces a dummy corners and a dummy corner response
  # map, just to illustrate how the code works. Your task will be to fill this
  # in with code that actually implements the Harris corner detector. You
  # should return th ecorner response map, and the non-max suppressed corners.
  # Input:
  #   I: input image, H x W x 3 BGR image
  # Output:
  #   response: H x W response map in uint8 format
  #   corners: H x W map in uint8 format _after_ non-max suppression. Each
  #   pixel stores the score for being a corner. Non-max suppressed pixels
  #   should have a low / zero-score.
  
  rng = np.random.RandomState(int(np.sum(I.astype(np.float32))))
  sz = I.shape[:2]
  # print(I.shape) #(120, 160, 3)
  # print(sz) # (120, 160)
  corners = rng.rand(*sz)
  # print(corners.shape) # (120, 160)
  corners = np.clip((corners - 0.95)/0.05, 0, 1)
  
  response = scipy.ndimage.gaussian_filter(corners, 4, order=0, output=None,
                                           mode='reflect')
  corners = corners * 255.
  corners = np.clip(corners, 0, 255)
  corners = corners.astype(np.uint8)
  
  response = response * 255.
  response = np.clip(response, 0, 255)
  response = response.astype(np.uint8)
  # print(response.shape)
  # print(corners.shape)
  return response, corners


def compute_corners2(image): # No NMS



  #the variables we might change 
  alpha = 0.05
  # kernal_size = (3,3)
  # sigma = 0


  #reading the image as a grayscale image
  image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
  dx = signal.convolve2d(image_gray, np.array([[-1, 0, 1]]), mode='same', boundary='symm')
  dy = signal.convolve2d(image_gray, np.array([[-1, 0, 1]]).T, mode='same', boundary='symm')

  dxx = scipy.ndimage.gaussian_filter(dx ** 2, sigma = 1)
  dxy = scipy.ndimage.gaussian_filter(dx * dy, sigma = 1)
  dyy = scipy.ndimage.gaussian_filter(dy ** 2, sigma = 1)
  detM = dxx * dyy - dxy**2
  traceM = (dxx+dyy)**2
  response = detM - alpha * traceM 
  response = response * 255. / np.max(response) 

  # threshold = 5
  # response[response< threshold] = 0

  response = np.clip(response, 0, 255)
  response = response.astype(np.uint8)

  # corners = response
  # # Non maximum suppression
  # window = 1
  # for r in range(0,image_gray.shape[0]):
  #         for c in range(0, image_gray.shape[1]):
  #                 flag = 0
  #                 for i in range(r-window,r+window+1):
  #                   for j in range(c-window,c+window+1):
  #                     if i >= 0 and j >= 0 and i < image_gray.shape[0] and j < image_gray.shape[1]:
  #                         if(corners[r,c] < response[i,j]):
  #                                 corners[r,c] = 0
  #                                 flag = 1
  #                                 break
  #                     if(flag == 1):
  #                             break

  # corners = corners * 255. / np.max(corners) 
  # corners = np.clip(corners, 0, 255)
  # corners = corners.astype(np.uint8)

  return response, response

# With NMS
def compute_corners4(image): # 4 best 



  #the variables we might change 
  alpha = 0.05
  # kernal_size = (3,3)
  # sigma = 3


  #reading the image as a grayscale image
  image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
  # #Calculating image gradients in x and y direction
  # dx = cv2.Sobel(image_gray, cv2.CV_64F,1, 0)
  # dy = cv2.Sobel(image_gray, cv2.CV_64F,0, 1)
  # #calculate dxx, dyy, dxy
  # dxx = cv2.GaussianBlur(dx**2, kernal_size, sigma)
  # dxy = cv2.GaussianBlur(dx*dy, kernal_size, sigma)
  # dyy = cv2.GaussianBlur(dy**2, kernal_size, sigma)
  dx = signal.convolve2d(image_gray, np.array([[-1, 0, 1]]), mode='same', boundary='symm')
  dy = signal.convolve2d(image_gray, np.array([[-1, 0, 1]]).T, mode='same', boundary='symm')

  dxx = scipy.ndimage.gaussian_filter(dx ** 2, sigma = 1)
  dxy = scipy.ndimage.gaussian_filter(dx * dy, sigma = 1)
  dyy = scipy.ndimage.gaussian_filter(dy ** 2, sigma = 1)
  detM = dxx * dyy - dxy**2
  traceM = (dxx+dyy)**2
  response = detM - alpha * traceM 
  response = response * 255. / np.max(response) 

  # threshold = 5
  # response[response< threshold] = 0

  response = np.clip(response, 0, 255)
  response = response.astype(np.uint8)


  corners = response
  # Non maximum suppression
  window = 2
  for r in range(0,image_gray.shape[0]):
          for c in range(0, image_gray.shape[1]):
                  flag = 0
                  for i in range(r-window,r+window+1):
                    for j in range(c-window,c+window+1):
                      if i >= 0 and j >= 0 and i < image_gray.shape[0] and j < image_gray.shape[1]:
                          if(corners[r,c] < response[i,j]):
                                  corners[r,c] = 0
                                  flag = 1
                                  break
                      if(flag == 1):
                              break

  corners = corners * 255. / np.max(corners) 
  corners = np.clip(corners, 0, 255)
  corners = corners.astype(np.uint8)

  return response, corners



#Bells and Whistles
def compute_corners(image): # 4 

  #the variables we might change 
  alpha = 0.05
  kernal_size = (3,3)
  sigma = 3


  #reading the image as a grayscale image
  image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  
  # #Calculating image gradients in x and y direction
  # dx = cv2.Sobel(image_gray, cv2.CV_64F,1, 0)
  # dy = cv2.Sobel(image_gray, cv2.CV_64F,0, 1)
  # #calculate dxx, dyy, dxy
  # dxx = cv2.GaussianBlur(dx**2, kernal_size, sigma)
  # dxy = cv2.GaussianBlur(dx*dy, kernal_size, sigma)
  # dyy = cv2.GaussianBlur(dy**2, kernal_size, sigma)
  dx = signal.convolve2d(image_gray, np.array([[-1, 0, 1]]), mode='same', boundary='symm')
  dy = signal.convolve2d(image_gray, np.array([[-1, 0, 1]]).T, mode='same', boundary='symm')

  dxx = scipy.ndimage.gaussian_filter(dx ** 2, sigma = 1)
  dxy = scipy.ndimage.gaussian_filter(dx * dy, sigma = 1)
  dyy = scipy.ndimage.gaussian_filter(dy ** 2, sigma = 1)
  detM = dxx * dyy - dxy**2
  traceM = (dxx+dyy)**2
  response = detM - alpha * traceM 
  response = response * 255. / np.max(response) 

  # threshold = 5
  # response[response< threshold] = 0

  response = np.clip(response, 0, 255)
  response = response.astype(np.uint8)


  corners = response
  # Non maximum suppression
  window = 2
  for r in range(0,image_gray.shape[0]):
          for c in range(0, image_gray.shape[1]):
                  flag = 0
                  for i in range(r-window,r+window+1):
                    for j in range(c-window,c+window+1):
                      if i >= 0 and j >= 0 and i < image_gray.shape[0] and j < image_gray.shape[1]:
                          if(corners[r,c] < response[i,j]):
                                  corners[r,c] = 0
                                  flag = 1
                                  break
                      if(flag == 1):
                              break

  corners = corners * 255. / np.max(corners) 
  corners = np.clip(corners, 0, 255)
  corners = corners.astype(np.uint8)

  return response, corners


