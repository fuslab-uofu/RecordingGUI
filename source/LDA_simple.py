import numpy as np


def image_segmentator(im, m0, m1, s0, s1):
    threshold = 0

    h, w = im.shape[0:2]
    x = np.expand_dims(im.reshape(-1, 3), 1)

    x0 = (x - m0)
    x1 = (x - m1)

    val = np.matmul(np.matmul(x0, np.linalg.inv(s0)), np.transpose(x0, (0, 2, 1))) - \
                    np.matmul(np.matmul(x1, np.linalg.inv(s1)), np.transpose(x1, (0, 2, 1)))

    val = val + np.linalg.det(s0) - np.linalg.det(s1)

    val[val > threshold] = 1
    val[val < threshold] = 0

    return val.reshape(h, w)


def segmenation_LDA(src_img, bk_1, bk_2, fg_1, size):
    patch_background = src_img[bk_1[1]:bk_1[1] + size, bk_1[0]:bk_1[0] + size]
    patch_background2 = src_img[bk_2[1]:bk_2[1] + size, bk_2[0]:bk_2[0] + size]
    patch_brain = src_img[fg_1[1]:fg_1[1] + size, fg_1[0]:fg_1[0] + size]

    background_samples = np.vstack([patch_background.reshape(-1, 3), patch_background2.reshape(-1, 3)])

    mu_0 = np.mean(background_samples, axis=0)
    mu_1 = np.mean(patch_brain.reshape(-1, 3), axis=0)

    sigma_0 = np.cov(np.transpose(background_samples.reshape(-1, 3)))
    sigma_1 = np.cov(np.transpose(patch_brain.reshape(-1, 3)))

    # prediction = image_segmentator(im1, mu_0, mu_1, sigma_0, sigma_1)
    prediction = image_segmentator(src_img, mu_0, mu_1, sigma_0, sigma_1)          # ?

    return prediction
