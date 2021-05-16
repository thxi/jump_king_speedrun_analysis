from random import choices

import numpy as np
import cv2
import imutils
from scipy.spatial import cKDTree


# the idea of an efficient implementation
# is taken from https://stackoverflow.com/a/59920744
def data_coord2view_coord(p, resolution, pmin, pmax):
    dp = pmax - pmin
    dv = (p - pmin) / dp * resolution
    return dv


def kNN2DDens(xv, yv, resolution, neighbours, dim=2):
    # Create the tree
    tree = cKDTree(np.array([xv, yv]).T)
    # Find the closest nnmax-1 neighbors (first entry is the point itself)
    grid = np.mgrid[0:resolution, 0:resolution].T.reshape(resolution**2, dim)
    dists = tree.query(grid, neighbours)
    # Inverse of the sum of distances to each grid point.
    inv_sum_dists = 1. / dists[0].sum(1)

    # Reshape
    im = inv_sum_dists.reshape(resolution, resolution)
    return im


# produce heatmap for a screen
def make_heatmap(positions, screen):
    np.random.seed(0)
    # remapping x with inverted y to w, h
    xmax = 60
    ymax = 44

    x = np.array([])
    y = np.array([])
    for i in range(1, len(positions)):
        prev = positions[i - 1]
        cur = positions[i]
        x = np.append(x, np.linspace(prev[0], cur[0], num=20))
        y = np.append(y, np.linspace(prev[1], cur[1], num=20))

    resolution = 250

    extent = [0, xmax, 0, ymax]
    xv = data_coord2view_coord(x, resolution, extent[0], extent[1])
    yv = data_coord2view_coord(y, resolution, extent[2], extent[3])

    neighbours = 2
    im = kNN2DDens(xv, yv, resolution, neighbours)
    im = im * 2000
    im = np.clip(im, 0, 255).astype(np.uint8)
    im = cv2.resize(im, (60, 44))
    im = cv2.applyColorMap(im, cv2.COLORMAP_OCEAN)
    im = imutils.resize(im, width=600)
    im = cv2.GaussianBlur(im, (3, 3), cv2.BORDER_DEFAULT)

    # im is bgr
    im = cv2.resize(im, (600, 448))
    transp_mask = np.zeros_like(im).astype(np.float32)

    # make background transparent
    for i in range(im.shape[0]):
        for j in range(im.shape[1]):
            if im[i][j][0] > 100:
                transp_mask[i][j] = 0.4

    heatmap = (transp_mask * im).astype(np.uint8) + (
        (1 - transp_mask) * screen).astype(np.uint8)
    return heatmap
