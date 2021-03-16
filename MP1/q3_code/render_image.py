import numpy as np
from generate_scene import get_ball
import matplotlib.pyplot as plt

# specular exponent
k_e = 50

# specular exponent
k_e = 50

def render(Z, N, A, S, 
            point_light_loc, point_light_strength, 
            directional_light_dirn, directional_light_strength,
            ambient_light, k_e):
    # To render the images you will need the camera parameters, you can assume
    # the following parameters. 
    #(cx, cy) denote the center of the image (point
    # where the optical axis intersects with the image, f is the focal length.
    # These parameters along with the depth image will be useful for you to
    # estimate the 3D points on the surface of the sphere for computing the
    # angles between the different directions.
    # N.shape #(256, 384, 3)
    # Z.shape #(256, 384)
    # vi: directional_light_dirn.shape: (1, 3)
    # point_light_loc = [[0, -10, 2]]
    h, w = A.shape
    cx, cy = w / 2, h /2
    f = 128.
#     print(Z.shape)
    # Ambient Term
    I = A * ambient_light
    
    #Diffuse Term
    #point_light_strength * [dot product of v_i (for point light) and n] + directional_light_strength * [dot product of v_i (for directional light) and n]
    
    #take care vi and n as shape (256, 384, 3)
    N = np.array(N)
    n1, n2, n3 = N.shape
    directional_light_dirn = np.array(directional_light_dirn)
    directional_light_dirn = directional_light_dirn - np.zeros(N.shape)
    for i in range(n1):
        for j in range(n2):
            directional_light_dirn[i][j] = directional_light_dirn[i][j]/ np.linalg.norm(directional_light_dirn[i][j])
    
#     directional_light_dirn = directional_light_dirn/ np.linalg.norm(directional_light_dirn)
    #D for directional_light
    Li_vi_dot_n_directional = directional_light_strength[0] * helper(directional_light_dirn, N)
    D_directional_light = np.multiply(A, Li_vi_dot_n_directional)
    
    #calculate vi for point light
    point_light_loc = np.array(point_light_loc)
    point_light_dirn = np.zeros((n1,n2,n3))
    
    x, y = np.meshgrid(np.arange(w), np.arange(h))
    x = x - cx
    y = y - cy
    X = x / f * Z
    Y = y / f * Z
    
    for i in range(n1):
        for j in range(n2):
            point_light_dirn[i][j] = point_light_loc - np.array([X[i][j],Y[i][j],Z[i][j]])
            point_light_dirn[i][j] = point_light_dirn[i][j]/ np.linalg.norm(point_light_dirn[i][j])
    

    Li_vi_dot_n_point = point_light_strength[0] * helper(point_light_dirn, N)
    D_point_light = np.multiply(A, Li_vi_dot_n_point)

    D = D_directional_light + D_point_light
    
    
    # Specular Term
    vr = np.zeros((n1,n2,n3))
    for i in range(n1):
        for j in range(n2):
            vr[i][j] = -np.array([X[i][j],Y[i][j],Z[i][j]])
            vr[i][j] = vr[i][j]/ np.linalg.norm(vr[i][j])
    
    #calculate si
    directional_light_si = np.zeros(directional_light_dirn.shape)
    for i in range(n1):
        for j in range(n2):
            directional_light_si[i][j] = -directional_light_dirn[i][j] - 2 *(np.dot(-directional_light_dirn[i][j], N[i][j]))* N[i][j]
    
    point_light_si = np.zeros(point_light_dirn.shape)
    for i in range(n1):
        for j in range(n2):
            point_light_si[i][j] = -point_light_dirn[i][j] - 2 *(np.dot(-point_light_dirn[i][j], N[i][j]))* N[i][j]
    
    vr_si_directional = helper(vr,directional_light_si)
    vr_si_point = helper(vr,point_light_si)
    
    S_directional = S * directional_light_strength[0] *  vr_si_directional**k_e
    S_point = S * point_light_strength[0] * vr_si_point**k_e
    
    S = S_directional + S_point
    

    I = I + D + S

    I = np.minimum(I, 1)*255
    I = I.astype(np.uint8)
    I = np.repeat(I[:,:,np.newaxis], 3, axis=2)

    return I

def helper(directional_light_dirn, N):
    n1, n2, n3 = N.shape
    ans = np.zeros((n1,n2))
    for i in range(n1):
        for j in range(n2):
            tmp = directional_light_dirn[i][j][0]* N[i][j][0] + directional_light_dirn[i][j][1]* N[i][j][1] + directional_light_dirn[i][j][2]* N[i][j][2]
            if tmp > 0:
                ans[i][j] = tmp
    return ans 

def main():
  for specular in [True, False]:
    # get_ball function returns:
    # - Z (depth image: distance to scene point from camera center, along the
    # Z-axis)
    # - N is the per pixel surface normals (N[:,:,0] component along X-axis
    # (pointing right), N[:,:,1] component along Y-axis (pointing down),
    # N[:,:,2] component along Z-axis (pointing into the scene)),
    # - A is the per pixel ambient and diffuse reflection coefficient per pixel,
    # - S is the per pixel specular reflection coefficient.
    Z, N, A, S = get_ball(specular=specular)

    # Strength of the ambient light.
    ambient_light = 0.5
    
    # For the following code, you can assume that the point sources are located
    # at point_light_loc and have a strength of point_light_strength. For the
    # directional light sources, you can assume that the light is coming _from_
    # the direction indicated by directional_light_dirn, and with strength
    # directional_light_strength. The coordinate frame is centered at the
    # camera, X axis points to the right, Y-axis point down, and Z-axis points
    # into the scene.
    
    # Case I: No directional light, only point light source that moves around
    # the object. 
    point_light_strength = [1.5]
    directional_light_dirn = [[1, 0, 0]]
    directional_light_strength = [0.0]
    
    fig, axes = plt.subplots(4, 4, figsize=(15,10))
    axes = axes.ravel()[::-1].tolist()
    for theta in np.linspace(0, np.pi*2, 16): 
      point_light_loc = [[10*np.cos(theta), 10*np.sin(theta), -3]]
      I = render(Z, N, A, S, point_light_loc, point_light_strength, 
                 directional_light_dirn, directional_light_strength,
                 ambient_light, k_e)
      ax = axes.pop()
      ax.imshow(I)
      ax.set_axis_off()
    plt.savefig(f'specular{specular:d}_move_point.png', bbox_inches='tight')
    plt.close()

    # Case II: No point source, just a directional light source that moves
    # around the object.
    point_light_loc = [[0, -10, 2]]
    point_light_strength = [0.0]
    directional_light_strength = [2.5]
    
    fig, axes = plt.subplots(4, 4, figsize=(15,10))
    axes = axes.ravel()[::-1].tolist()
    for theta in np.linspace(0, np.pi*2, 16): 
      directional_light_dirn = [np.array([np.cos(theta), np.sin(theta), .1])]
      directional_light_dirn[0] = \
        directional_light_dirn[0] / np.linalg.norm(directional_light_dirn[0])
      I = render(Z, N, A, S, point_light_loc, point_light_strength, 
                 directional_light_dirn, directional_light_strength,
                 ambient_light, k_e) 
      ax = axes.pop()
      ax.imshow(I)
      ax.set_axis_off()
    plt.savefig(f'specular{specular:d}_move_direction.png', bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
  main()
