from sklearn.feature_extraction import image
from SimpleFNN import FNN
import torch
import numpy as np
import matplotlib.pyplot as plt


patch_size = 1
n_input = 3 * ((2 * patch_size + 1) ** 2)
n_out = 3


def get_all_patches(im):
    patches = image.extract_patches_2d(im, ((2 * patch_size) + 1, (2 * patch_size) + 1))

    return patches.reshape(-1, n_input)


def model_in_batches(inp, model):
    start = 0
    n_batches = 10

    ret_matrix = torch.zeros([inp.shape[0], n_out])

    step = int(inp.shape[0]/n_batches)

    for i in range(n_batches):

        if i != n_batches -1:
            ret_matrix[start: start+step] = model(torch.from_numpy(inp[start: start+step]).cuda().float())

            start = start + step + 1
        else:
            ret_matrix[start:] = model(torch.from_numpy(inp[start:]).cuda().float())

    return ret_matrix


def SegmentationNN(img, model):
    # model_path = '/home/tester/Desktop/recordingGui-master/best_model.pth'
    # n_hidden_layers = 1
    # npl = 32

    img = img / 255.0

    # model = FNN(n_input, n_out, n_hidden_layers, npl)

    # model.load(model_path)

    # model = model.cuda()

    h, w = img.shape[0:2]

    model_inp = get_all_patches(img)
    # out = model(torch.from_numpy(model_inp).cuda().float())
    print("shape of model_inp", model_inp.shape)
    out = model_in_batches(model_inp, model)
  
    prediction = np.argmax(out.detach().cpu().numpy(), axis=1)
    # print(prediction)
    # print(prediction.shape)
    prediction = prediction.reshape(h - (2 * patch_size), w - (2 * patch_size))
    

    return prediction