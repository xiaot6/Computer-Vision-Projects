def warp_images(img0, img1, H):
    """
    write your code to stitch images together according to the homography
    """
    transform = skimage.transform.ProjectiveTransform(H)
    warp = skimage.transform.warp

    r, c, _ = img0.shape

    corners = np.array([[0, 0],[0, r],[c, 0],[c, r]])
    warped_corners = transform(corners)


    combine_corners = np.vstack((warped_corners, corners))

    min_corner = np.int32(combine_corners.min(axis=0))
    max_corner = np.int32(combine_corners.max(axis=0))
    
    output_shape = np.ceil((max_corner - min_corner)[::-1])

    offset = skimage.transform.SimilarityTransform(translation=-min_corner)

    img1_ = warp(img1, offset.inverse, output_shape=output_shape, cval=-1)
    img0_ = warp(img0, (transform + offset).inverse, output_shape=output_shape, cval=-1)
    img1_zeros = warp(img1, offset.inverse, output_shape=output_shape, cval=0)
    img0_zeros = warp(img0, (transform + offset).inverse, output_shape=output_shape, cval=0)

    overlap = (img1_ != -1.0 ).astype(int) + (img0_ != -1.0).astype(int)
    overlap += (overlap < 1).astype(int)
    merged = (img1_zeros+img0_zeros)/overlap

    im = Image.fromarray((255*merged).astype('uint8'), mode='RGB')
    im = np.asarray(im)

    return im



def normalize(pts):
    pts_centered = pts - np.mean(pts,axis= 0)

    scale = 1/ (sqrt(1 / (2 * len(pts)) * np.sum(pts_centered[:, 0]**2 + pts_centered[:, 1]**2)))

    transform = np.array([[scale, 0, -scale*np.mean(pts,axis= 0)[0]], 
                           [0, scale, -scale*np.mean(pts,axis= 0)[1]], 
                           [0, 0, 1]])
    pts = np.concatenate((pts, np.ones((pts.shape[0], 1))), axis=1)
    normalized = np.dot(transform, pts.T).T

    return normalized[:, :2], transform


def normalize(pts):
    mean = np.mean(pts, axis=0)
    pts_x_centered = pts[:, 0] - mean[0]
    pts_y_centered = pts[:, 1] - mean[1]
    pts_centered = pts - np.mean(pts, axis=0)
    print(pts_centered[:, 0] == pts_x_centered)
    print(pts_centered[:, 1] == pts_y_centered)


    scale = 1/ (sqrt(1 / (2 * len(pts)) * np.sum(pts_x_centered**2 + pts_y_centered**2)))

    transform = np.array([[scale, 0, -scale*mean[0]], 
                           [0, scale, -scale*mean[1]], 
                           [0, 0, 1]])
    pts = np.concatenate((pts, np.ones((pts.shape[0], 1))), axis=1)
    normalized = np.dot(transform, pts.T).T

    return normalized[:, :2], transform