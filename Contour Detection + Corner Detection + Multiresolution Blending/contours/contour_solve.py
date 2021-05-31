import numpy as np
from scipy import signal
import cv2
from scipy.signal.windows import gaussian
from scipy.signal import convolve2d




# def compute_edges_dxdy(I): #given code 
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

def compute_edges_dxdy1(I): #part1
  """Returns the norm of dx and dy as the edge response function."""
  I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
  I = I.astype(np.float32)/255.
  dx = signal.convolve2d(I, np.array([[-1, 0, 1]]), mode='same', boundary = 'symm')
  dy = signal.convolve2d(I, np.array([[-1, 0, 1]]).T, mode='same', boundary = 'symm')

  mag = np.sqrt(dx**2 + dy**2)
  mag = mag / 1.5
  mag = mag * 255.
  mag = np.clip(mag, 0, 255)
  mag = mag.astype(np.uint8)
  return mag


def compute_edges_dxdy2(I): #part2
  """Returns the norm of dx and dy as the edge response function."""
  I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
  I = I.astype(np.float32)/255.
  I = cv2.GaussianBlur(I, (7,7),2)
  dx = signal.convolve2d(I, np.array([[-1, 0, 1]]), mode='same', boundary = 'symm')
  dy = signal.convolve2d(I, np.array([[-1, 0, 1]]).T, mode='same', boundary = 'symm')
 
 
  #normalize it
  mag = np.sqrt(dx**2 + dy**2)
  mag = ((mag - np.min(mag)) / np.max(mag - np.min(mag))) * 255.0
  mag = np.clip(mag, 0, 255)
  mag = mag.astype(np.uint8)

  return mag


def compute_edges_dxdy3(I): #part3
  """Returns the norm of dx and dy as the edge response function."""
  I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
  I = I.astype(np.float32)/255.
  I = cv2.GaussianBlur(I, (7,7),2)
  dx = signal.convolve2d(I, np.array([[-1, 0, 1]]), mode='same', boundary = 'symm')
  dy = signal.convolve2d(I, np.array([[-1, 0, 1]]).T, mode='same', boundary = 'symm')


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



def compute_edges_dxdy(I): #part4
  """Returns the norm of dx and dy as the edge response function."""
  I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
  I = I.astype(np.float32)/255.
  I = cv2.GaussianBlur(I, (7,7),2)
  dx = signal.convolve2d(I,np.array([[-1,0, 1],[-4,0,4],[-1,0,1]]),mode='same', boundary = 'symm')
  dy = signal.convolve2d(I,np.array([[-1,0, 1],[-4,0,4],[-1,0,1]]).T,mode='same', boundary = 'symm')
 

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







  