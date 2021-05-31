
### Problems


1.  **Un-shredding Images [30 pts].**
    We accidentally shredded some images! In this problem, we will recover the
    original images from the corresponding shreds. Along the way we will learn how
    to deal with and process images in Python. Example input / output is shown
    below.
    
    <div align="center">
    <img src="shredded.png" width="75%">
    <img src="output.png" width="75%">
    </div>
    
    1.  **Combine .** We will start simple, and work with images where the
        shredder simply divided the image into vertical strips. These are prefixed
        with `simple_` in the [shredded-images](shredded-images) folder. Each folder
        contains the shreds (as individual files) for that particular image.
    
        Our first task is to take these strips and concatenate them (in any order)
        to produce a complete image. Without proper ordering of the strips, this
        image won't quite look correct, but that's ok for now. We will tackle that
        in the next part. For now, save this weird composite image. **Include the
        generated image into your report.**
    
    2.  **Re-order.** As you noticed, without correctly ordering the
        strips, the images didn't quite look correct. Our goal now is to identify the
        correct ordering for these strips. We will adopt a very simple greedy
        algorithm. For each pair of strips, we will compute how well does strip 1 go
        immediately left of strip 2. We will do this my measuring the similarity
        between the last column of pixels in strip 1 and the first column of pixels in
        strip 2. You can measure similarity using (negative of) the *sum of squared
        differences* which is simply the L2 norm of the pixel difference.
        
        Once you have computed the similarity between all pairs of strips, you can
        follow a greedy algorithm to composite the image together. Start with a
        strip and place the strip that is most compatible with it on the left and
        the right side, and so on. Compose the strips together into an image using
        this simple greedy algorithm.
    
        **Save the generated composite images for all the `simple_` shreds from the
        `shredded-images` folder, and include them in your report. Also include a
        brief description of your implemented solution, focusing especially on the
        more non-trivial or interesting parts of the solution.**
        
    3.  **Align and Re-order .** Next, we will tackle the case where our
        shredder also cut out the edges of some of the strips, so that they are no
        longer aligned vertically. These are prefixed with `hard_`. We will now
        modify the strip similarity function from the previous part to compensate for
        this vertical misalignment.
    
        We will vertically slide one strip relative to the other, in the range of 20% 
        of the vertical dimension to find the best alignment, and compute
        similarity between the overlapping parts for different slide amounts. We
        will use the *maximum* similarity over these different slide amounts, as the
        similarity between the two strips. Note that you may need to experiment with
        similarity functions other than the sum of squared distances. One common
        alternative is *zero mean normalized cross correlation*, which is simply the
        dot product between the two pixel vectors after they have been normalized to
        have zero mean and unit norm.
    
        Implement this strategy for measuring the similarity between the strips. Use
        this along with the greedy re-ordering strategy in the previous part, to
        reconstruct this harder set of shreds. You will also have to keep track of
        the slide amounts that led to the best match. You will need those when you
        stitch the shreds together.
    
        **Save the generated composite images for all the `hard_` shreds, and
        include them in your report. As before, include a brief description of your
        implemented solution, focusing especially on the more non-trivial or
        interesting parts of the solution.  What design choices did you make, and
        how did they affect the quality of the result and the speed of computation?
        What are some artifacts and/or limitations of your implementation, and what
        are possible reasons for them?**
