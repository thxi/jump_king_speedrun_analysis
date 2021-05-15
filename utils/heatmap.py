from random import choices

import numpy as np
import cv2
import imutils
from scipy.spatial import cKDTree


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


def make_heatmap(positions, screen):
    np.random.seed(0)
    # remapping x with inverted y to w, h
    xmax = 60
    ymax = 44
    s2p = choices(positions, k=1000)

    eps = np.random.normal(0, 1, size=1000)
    xs = np.array([i[0] for i in s2p]) + eps
    eps = np.random.normal(0, 1, size=1000)
    ys = np.array([i[1] for i in s2p]) + eps

    resolution = 250

    extent = [0, xmax, 0, ymax]
    xv = data_coord2view_coord(xs, resolution, extent[0], extent[1])
    yv = data_coord2view_coord(ys, resolution, extent[2], extent[3])

    neighbours = 2
    im = kNN2DDens(xv, yv, resolution, neighbours)
    im = im * 3000
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
                transp_mask[i][j] = 0.3

    heatmap = (transp_mask * im).astype(np.uint8) + (
        (1 - transp_mask) * screen).astype(np.uint8)
    return heatmap
