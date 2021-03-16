## Contour Detection - Solution Template

**NOTE:** All values and figures in this template are examples that you will need to replace with your own results

1. **Method Description.: Describe the different mehtods and their key implementation detials.
   **Warm up**:
   I use the signal.convolve2d(I,np.array([[-1,0, 1],[-4,0,4],[-1,0,1]]),mode='same', boundary = 'symm'). 
   I changed the boundary function into "symm", which means symmetrical boundary conditions.
   **Smoothing**:
   We  smooth the image so that we can reduce the amount of edges detected from the noise and apply a low-pass filter.
   In my applications, I firstly use GaussianBlur function to get the blur image. 
   ```
   I = cv2.GaussianBlur(I, (7,7),2)
   ```
   Also, I use derivative of Gaussian filters to obtain more robust estimates of the gradient:
   ```
   dx = signal.convolve2d(I,np.array([[-1,0, 1],[-4,0,4],[-1,0,1]]),mode='same', boundary = 'symm')
   dy = signal.convolve2d(I,np.array([[-1,0, 1],[-4,0,4],[-1,0,1]]).T,mode='same', boundary = 'symm')
   ```
   Then, for the filter, I change the [−1, 0, 1] to np.array([[-1,0, 1],[-4,0,4],[-1,0,1]]) for better results.
   **Non-maximum Suppression**:





2. **Precision Recall Plot.** *TODO*: Use [contour_plot.py](contours/../contour_plot.py) to add curves for the different methods that you implemented into a single plot.
   
   <div align="center">
      <img src="plot.png" width="60%">
   </div>

3. **Results Table.** *TODO*: Present the performance metrics for each implementation part in a table format

   | Method | overall max F-score | average max F-score | AP | Runtime (seconds) |
   | ----------- | --- | --- | ---  | --- |
   | Initial implementation | 0.52 | 0.56 | 0.43 | 0.008 |
   | Warm-up [remove boundary artifacts | | | | |
   | Smoothing | | | | |
   | Non-max suppression | | | | 
   | Test set numbers of best model [From gradescope] | | | |

4. **Visualizations.** *TODO:* Include visualization on 3 images (before and after the contour detection). Comment on
   your observations, where does your contour detector work well, where it doesn't and why? you can are also add visualizations of your own images.
   <div align="center">
      <img src="227092.jpg" width="35%" style="margin:10px;">
      <img src="227092-nms.png" width="35%" style="margin:10px;">
   </div>

5. **Bells and Whistles.** *TODO*: Include details of the bells and whistles that you
   tried here.

   *TODO*: Present the performance metrics for the bells and whistles in a table format
   
   | Method | overall max F-score | average max F-score | AP | Runtime (seconds) |
   | ----------- | --- | --- | ---  | --- |
   | Best base Implementation (from above) | | | | 
   | Bells and whistle (1) [extra credit]) | | | | 
   | Bells and whistle (2) [extra credit]) | | | |
   | Bells and whistle (n) [extra credit]) | | | |