import numpy as np
from tqdm import tqdm
import os, glob
import yaml
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from sklearn.feature_extraction import image
import time

size = 1
shape_var = 3*((2 * size + 1)**2)


# def get_all_patches(im):

#     h, w = im.shape[0:2]
#     temp = np.zeros(((h-2*size)*(w-2*size), shape_var), dtype=float)

#     for x in tqdm(range(size, im.shape[0]-size)):
#         for y in range(size, im.shape[1]-size):
#             temp[(x-size) * (w-2*size) + y - size, :] = im[x - size:x + size+1, y-size:y+size+1, :].reshape(-1, shape_var)
#     return temp

def get_all_patches(im):
    patches = image.extract_patches_2d(im, ((2 * size) + 1, (2 * size) + 1))
    return patches.reshape(-1, shape_var)


def image_segmentator(im, m_list, s_list):
    threshold = 0

    h, w = im.shape[0:2]
    # s=time.time()
    x = np.expand_dims(get_all_patches(im), 1)
    # e=time.time()
    # print("expand: ", e-s)

    n_class = len(m_list)
    x_list = []

    for i in range(n_class):
        x_list.append(x - m_list[i])

    val_list = []

    # s=time.time()
    for i in range(n_class):
        temp = -0.5 * np.matmul(np.matmul(x_list[i], np.linalg.inv(s_list[i])), np.transpose(x_list[i], (0, 2, 1)))
        val_list.append(temp - np.log(np.sqrt(2 * np.pi)) - np.linalg.slogdet(s_list[i])[1])
        # val_list[i] = val_list[i] - np.log(np.sqrt(2 * np.pi)) - np.linalg.slogdet(s_list[i])[1]
    # e=time.time()
    # print("computation: ", e-s)

    for i in range (n_class):
        if i == 0:
            all_vals = val_list[i]
        else:
            all_vals = np.hstack([all_vals, val_list[i]])

    prediction = np.argmax(all_vals, axis=1)

    # val[val > threshold] = 1
    # val[val < threshold] = 0

    return prediction.reshape(h - (2 * size), w - (2 * size))


# def get_patch_based_regions(src_img, roi):
#     # size = 2
#     print(roi[0][1])
#     # quit()
#     temp = src_img[roi[0][1] - size:roi[0][1] + size+1, roi[0][0]-size:roi[0][0]+size+1, :].reshape(-1, shape_var)

#     for x in range(roi[0][1], roi[1][1]):
#         for y in range(roi[0][0], roi[1][0]):
#             pt = src_img[x - size:x + size+1, y-size:y+size+1, :].reshape(-1, shape_var)
#             temp = np.vstack([temp, pt])
#     return temp

def get_patch_based_regions(src_img, roi):
    patches = image.extract_patches_2d(src_img[roi[0][1]:roi[1][1], roi[0][0]:roi[1][0], :], ((2 * size) + 1, (2 * size) + 1))

    return patches.reshape(-1, shape_var)


def get_patch_from_seg(im, seg):
    h, w = seg.shape
    count = 0
    total_size = seg.sum()
    temp = np.zeros((total_size, shape_var))
    for i in tqdm(range(h)):
        if i < size or i >= h - size:
            continue
        for j in range(w):
            if j < size or j >= w - size:
                continue
            if seg[i, j]:
                temp[count, :] = im[i - size:i + size+1, j-size:j+size+1, :].reshape(-1, shape_var)
                count = count + 1
                # if flag == 0:
                #     temp = im[i - size:i + size+1, j-size:j+size+1, :].reshape(-1, shape_var)
                #     flag = 1
                # else:
                #     pt = im[i - size:i + size+1, j-size:j+size+1, :].reshape(-1, shape_var)
                #     temp = np.vstack([temp, pt])
    return temp


def segmenation_LDA(src_img, rois, save_path, num):
    # print("Iniside Function")
    func_start = time.time()

    print(num)

    # print(rois)
    # print(src_img.shape)

    # fig = plt.figure(constrained_layout=True)
    # ax = fig.subplots(1) 

    # ax.imshow(src_img)


    # for i in range(int(len(rois))):
    #     print(i)
    #     print(rois[i])
    #     rect = patches.Rectangle((rois[i][0][0], rois[i][0][1]), rois[i][1][0] - rois[i][0][0], rois[i][1][1] - rois[i][0][1] )

    #     ax.add_patch(rect)

    # plt.show()


    # size = 2

    out_path = f'{save_path}/IM_0{num}/'

    os.makedirs(out_path, exist_ok=True)


    if len(rois) == 0:

        # if int(num) == 1:
        #     load_path = '/home/tester/Desktop/recordingGui-master/saved_params/'
        #     n_class = len(sorted(glob.glob(f'{load_path}/covs_*.npy')))
        # else:
        
        # start = time.time()
        load_path = f'{save_path}/IM_0{str(int(num)-1).zfill(4)}/'
        n_class = len(sorted(glob.glob(f'{load_path}/covs_*.npy')))
        if(n_class == 0):
            load_path = '/home2/tester/Desktop/recordingGui-master/saved_params/'
            n_class = len(sorted(glob.glob(f'{load_path}/covs_*.npy')))

        # end = time.time()
        # print("Time taken to load Cov npy : ", end - start, 's')

        # print(out_path)
        # print(n_class)

        mu_list = []
        sigma_list = []

        # start = time.time()
        for i in range(n_class):
            mu_list.append(np.load(f'{load_path}/means_{i}.npy', allow_pickle=True).item())
            sigma_list.append(np.load(f'{load_path}/covs_{i}.npy', allow_pickle=True).item())

        iteration = str(len(mu_list[0].keys()) - 1)

        mu_list = []
        sigma_list = []

        for i in range(n_class):
            mu_list.append(np.load(f'{load_path}/means_{i}.npy', allow_pickle=True).item()[iteration])
            sigma_list.append(np.load(f'{load_path}/covs_{i}.npy', allow_pickle=True).item()[iteration])

        # end = time.time()

        # print("Time taken to load sigma list : ", end - start, 's')


    # save the rois

    else:
        with open(f'{out_path}/rois.yml', 'w') as yaml_file:
            yaml.dump(rois, yaml_file, default_flow_style=True)

        n_class = int(len(rois))

        c_list = []
        mu_list = []
        sigma_list = []

        for i in range(n_class):

            c_list.append(get_patch_based_regions(src_img, rois[i]))
            mu_list.append(np.mean(c_list[i].reshape(-1, shape_var), axis=0))
            sigma_list.append(np.cov(np.transpose(c_list[i].reshape(-1, shape_var))))

    iterate = True
    count = 0

    s_dict_list = []
    m_dict_list = []
    
    for i in range(n_class):
        s_dict_list.append({})
        m_dict_list.append({})

        m_dict_list[i][str(count)] = mu_list[i]
        s_dict_list[i][str(count)] = sigma_list[i]
    
    prediction = image_segmentator(src_img, mu_list, sigma_list)
    
    # old_m0 = np.copy(mu_list[0])
    
    # while iterate:
    #     count += 1

    #     c_list = []
    #     mu_list = []
    #     sigma_list = []

    #     print("Iterating : ", count)

    #     for i in range(n_class):
    #         c_list.append(get_patch_from_seg(src_img[size:-size, size:-size], prediction == i))
    #         mu_list.append(np.mean(c_list[i].reshape(-1, shape_var), axis=0))
    #         sigma_list.append(np.cov(np.transpose(c_list[i].reshape(-1, shape_var))))

    #         m_dict_list[i][str(count)] = mu_list[i]
    #         s_dict_list[i][str(count)] = sigma_list[i]

    #     if (mu_list[0] - old_m0).sum() == 0:
    #         iterate = False
    #     else:
    #         print((mu_list[0] - old_m0).sum())
    #         old_m0 = np.copy(mu_list[0])

    #     print("Improving Segmentation")

    #     prediction = image_segmentator(src_img, mu_list, sigma_list)

    #     # plt.figure()
    #     # plt.imshow(prediction)
    #     # plt.show()

    #     print("Debug")

    for i in range(n_class):
        np.save(f'{out_path}/means_{i}.npy', m_dict_list[i])
        np.save(f'{out_path}/covs_{i}.npy', s_dict_list[i])


    func_end = time.time()

    print("Time taken to complete func : ", func_end - func_start, 's')
    return prediction
