import pandas as pd
import numpy as np

#Separate function not included in aniposelib to correct the coordinate frame
def proj(u, v):
    """Project u onto v"""
    return u * np.dot(v,u) / np.dot(u,u)

def ortho(u, v):
    """Orthagonalize u with respect to v"""
    return u - proj(v, u)

def get_median(all_points_3d, ix):
    pts = all_points_3d[:, ix]
    pts = pts[~np.isnan(pts[:, 0])]
    return np.median(pts, axis=0)

def correct_coordinate_frame(config, all_points_3d, bodyparts):
    """Given a config and a set of points and bodypart names, this function will rotate the coordinate frame to match the one in config"""
    bp_index = dict(zip(bodyparts, range(len(bodyparts))))
    axes_mapping = dict(zip('xyz', range(3)))

    ref_point = config['triangulation']['reference_point']
    axes_spec = config['triangulation']['axes']
    a_dirx, a_l, a_r = axes_spec[0]
    b_dirx, b_l, b_r = axes_spec[1]

    a_dir = axes_mapping[a_dirx]
    b_dir = axes_mapping[b_dirx]

    ## find the missing direction
    done = np.zeros(3, dtype='bool')
    done[a_dir] = True
    done[b_dir] = True
    c_dir = np.where(~done)[0][0]

    a_lv = get_median(all_points_3d, bp_index[a_l])
    a_rv = get_median(all_points_3d, bp_index[a_r])
    b_lv = get_median(all_points_3d, bp_index[b_l])
    b_rv = get_median(all_points_3d, bp_index[b_r])

    a_diff = a_rv - a_lv
    b_diff = ortho(b_rv - b_lv, a_diff)

    M = np.zeros((3,3))
    M[a_dir] = a_diff
    M[b_dir] = b_diff
    # form a right handed coordinate system
    if (a_dir,b_dir) in [(0,1), (2,0), (1,2)]:
        M[c_dir] = np.cross(a_diff, b_diff)
    else:
        M[c_dir] = np.cross(b_diff, a_diff)

    M /= np.linalg.norm(M, axis=1)[:,None]

    center = get_median(all_points_3d, bp_index[ref_point])

    all_points_3d_adj = all_points_3d.dot(M.T)
    center_new = get_median(all_points_3d_adj, bp_index[ref_point])
    all_points_3d_adj = all_points_3d_adj - center_new

    return all_points_3d_adj, M, center_new