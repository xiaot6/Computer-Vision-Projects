import numpy as np
from scipy import signal
import cv2
from scipy.signal.windows import gaussian
from scipy.signal import convolve2d




# def compute_edges_dxdy(I):
#   """Returns the norm of dx and dy as the edge response function."""
#   I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
#   I = I.astype(np.float32)/255.
#   dx = signal.convolve2d(I, np.array([[-1, 0, 1]]), mode='same')
#   dy = signal.convolve2d(I, np.array([[-1, 0, 1]]).T, mode='same')
#   mag = np.sqrt(dx**2 + dy**2)
#   mag = mag / 1.5
#   mag = mag * 255.
#   mag = np.clip(mag, 0, 255)
#   mag = mag.astype(np.uint8)
#   return mag

def compute_edges_dxdy(I):
  """Returns the norm of dx and dy as the edge response function."""
  I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
  I = I.astype(np.float32)/255.
  I = cv2.GaussianBlur(I, (7,7),2)
  dx = signal.convolve2d(I,np.array([[-1,0, 1],[-4,0,4],[-1,0,1]]),mode='same', boundary = 'symm')
  dy = signal.convolve2d(I,np.array([[-1,0, 1],[-4,0,4],[-1,0,1]]).T,mode='same', boundary = 'symm')

  # g_l = 15
  # g_s = 1
  # gaussian_kernel = get_gaussian(g_l, g_s)

  # blurred_img = convolve2d(I, gaussian_kernel, mode='same')
  # I = get_derivatives(blurred_img)

  # dog_x = convolve2d(gaussian_kernel, dx, mode='same', boundary = 'symm')
  # dog_y = convolve2d(gaussian_kernel, dy, mode='same', boundary = 'symm')
  # dx = convolve2d(I, dog_x, mode='same')
  # dy = convolve2d(I, dog_y, mode='same')  

  I = np.hypot(dx, dy)    
  I = I / I.max() * 255
  
  angle = np.arctan2(dy, dx)
  
  Z = np.zeros((I.shape))

  angle = angle * 180. / np.pi
  angle[angle < 0] += 180

  angle_mod = angle % 180

  for i in range(I.shape[0] - 1):
      for j in range(I.shape[1] - 1):
        q = 0
        r = 0
          
        if (0 <= angle_mod[i,j] < 45):
            alpha = np.abs(np.tan(angle_mod[i,j]))
            q = (alpha * I[i + 1, j + 1]) + ((1 - alpha) * I[i, j + 1])
            r = (alpha * I[i - 1, j - 1]) + ((1 - alpha) * I[i, j - 1]) 
        
        elif (45 <= angle_mod[i,j] < 90):
            alpha = np.abs(1./np.tan(angle_mod[i,j]))
            q = (alpha * I[i + 1, j + 1]) + ((1 - alpha) * I[i + 1, j])
            r = (alpha * I[i - 1, j - 1]) + ((1 - alpha) * I[i - 1, j])
        
        elif (90 <= angle_mod[i,j] < 135):
            alpha = np.abs(1./np.tan(angle_mod[i,j]))
            q = (alpha * I[i + 1, j - 1]) + ((1 - alpha) * I[i + 1, j])
            r = (alpha * I[i - 1, j + 1]) + ((1 - alpha) * I[i - 1, j])
        
        elif (135 <= angle_mod[i,j] < 180):
            alpha = np.abs(np.tan(angle_mod[i,j]))
            q = (alpha * I[i + 1, j - 1]) + ((1 - alpha) * I[i, j - 1])
            r = (alpha * I[i - 1, j + 1]) + ((1 - alpha) * I[i, j + 1])

        if (I[i,j] >= q) and (I[i,j] >= r):
            Z[i,j] = I[i,j]
        else:
            Z[i,j] = 0
 
  #normalize it
  mag = ((Z - np.min(Z)) / np.max(Z - np.min(Z))) * 255.0
  mag = np.clip(mag, 0, 255)
  mag = mag.astype(np.uint8)

  return mag


def get_gaussian(l=5, sigma=1):
    # Create a gaussian kernel
    kernel_1d = gaussian(l, std=sigma).reshape(l, 1)
    kernel_2d = np.outer(kernel_1d, kernel_1d)
    return kernel_2d

def get_derivatives(im):
    dx = np.array([[-1,0, 1],[-3,0,3],[-1,0,1]])
    dy = np.array([[-1,0, 1],[-3,0,3],[-1,0,1]]).T
    dx_img = convolve2d(im, dx, mode='same')
    dy_img = convolve2d(im, dy, mode='same')
    gradient_img = np.sqrt(np.square(dx_img) + np.square(dy_img))
    return gradient_img



  