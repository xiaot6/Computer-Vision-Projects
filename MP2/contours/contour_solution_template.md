## Contour Detection - Solution Template

**NOTE:** All values and figures in this template are examples that you will need to replace with your own results

1. **Method Description.**: Describe the different mehtods and their key implementation detials.

   **Warm up**:

   I use the spicy.
   ```
   spicy.signal.convolve2d(I,np.array([[-1,0, 1],[-4,0,4],[-1,0,1]]),mode='same', boundary = 'symm'). 
   ```
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

   To sharpen the edfes, we will find the local maxima in the gradient image. 
   Here I use this strategy: A gradient is considered locally maximal if it is either greater than or equal to its neighbors in the positive and negative gradient direction.
   For the gradient direction, we calculate the arctangent of the gradient vector:
   ```
   angle = np.arctan2(dy, dx)
   ```
   Then I round it to th nearest 45 degree by the angle mod, so that I can conform to one of 8 discrete directions
   Also, for more accuracy, I use the alpha, which can take the combination of different directions. 
   After than, I compare the the neighbor results with the cernter one. 
   If the neighbor results have a higher "edgeness", we will ignore this center or. Otherwise, we keep it. 

   After that, we normalize our resluts to get the better results. 




2. **Precision Recall Plot.** *TODO*: Use [contour_plot.py](contours/../contour_plot.py) to add curves for the different methods that you implemented into a single plot.
   
   <div align="center">
      <img src="plot.png" width="60%">
   </div>

3. **Results Table.** : Present the performance metrics for each implementation part in a table format

   | Method | overall max F-score | average max F-score | AP | Runtime (seconds) |
   | ----------- | --- | --- | ---  | --- |
   | Initial implementation | 0.52 | 0.56 | 0.43 | 0.008 |
   | Warm-up [remove boundary artifacts | 0.559771| 0.584352| 0.259602| 0.245163|
   | Smoothing | 0.561291  | 0.583706  | 0.401346  | 0.301801|
   | Non-max suppression | 0.611799|0.633582 | 0.605676| 0.9 |
   | Test set numbers of best model [From gradescope] | 0.611799|0.633582 | 0.605676| 0.9 |

4. **Visualizations.** *TODO:* Include visualization on 3 images (before and after the contour detection). Comment on
   your observations, where does your contour detector work well, where it doesn't and why? you can are also add visualizations of your own images.
   <div align="center">
      <img src="./data/val/images/37073.jpg" width="30%" style="margin:10px;">
      <img src="./output/part1/bench/37073.png" width="30%" style="margin:10px;">
      <img src="./output/demo/bench/37073.png" width="30%" style="margin:10px;">

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