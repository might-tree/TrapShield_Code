"""  
Copyright (c) 2019-present NAVER Corp.
MIT License
"""

# -*- coding: utf-8 -*-
import sys
import os
import time
import argparse
import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.autograd import Variable
from refinenet import RefineNet
from multiprocessing import Pool, Process
from craft import CRAFT
from PIL import Image
import cv2
from skimage import io
import numpy as np
import craft_utils
import imgproc
import file_utils
import json
import zipfile
from collections import OrderedDict
#import requests
# from torch.utils import mkldnn as mkldnn_utils
from config_v3_main import PATH_TO_CRAFT, \
    IMAGES_EXTENSIONS_TO_ACCEPT, \
    MULTI_LANGUAGE_MODEL_PATH, ENGLISH_LANGUAGE_MODEL, \
    REFINER_MODEL, DETECTOR_TEMP_FOLDER, RESULT_FOLDER, USE_CUDA
from arg_parser import *


torch.set_num_interop_threads(8)


##### Celery module #####
def loader_(net, model_args, cuda=False, refine=False, normal=True):
    if normal:
        if cuda:
            net.load_state_dict(copyStateDict(torch.load(model_args)))
        else:
            net.load_state_dict(
                copyStateDict(torch.load(model_args, map_location='cpu')))

        if cuda:
            net = net.cuda()
            net = torch.nn.DataParallel(net)
            cudnn.benchmark = False

        return net.eval(), False
    else:
        # LinkRefiner
        refine_net = None
        if refine:
            refine_net = RefineNet()
            if args.cuda:
                refine_net.load_state_dict(
                    copyStateDict(torch.load(args.refiner_model)))
                refine_net = refine_net.cuda()
                refine_net = torch.nn.DataParallel(refine_net)
            else:
                refine_net.load_state_dict(copyStateDict(
                    torch.load(args.refiner_model, map_location='cpu')))
            return refine_net.eval(), True
        return refine_net, False


def test_net(net, image, text_threshold, link_threshold, low_text, cuda, poly,
             refine_net=None):
    t0 = time.time()
    # resize
    img_resized, target_ratio, size_heatmap = imgproc.resize_aspect_ratio(image,
                                                                          args.canvas_size,
                                                                          interpolation=cv2.INTER_LINEAR,
                                                                          mag_ratio=args.mag_ratio)
    ratio_h = ratio_w = 1 / target_ratio

    # preprocessing
    x = imgproc.normalizeMeanVariance(img_resized)
    x = torch.from_numpy(x).permute(2, 0, 1)  # [h, w, c] to [c, h, w]
    x = Variable(x.unsqueeze(0))  # [c, h, w] to [b, c, h, w]
    if cuda:
        x = x.cuda()
    # net = mkldnn_utils.to_mkldnn(net)

    # forward pass
    with torch.no_grad():
        y, feature = net(x)

    # make score and link map
    score_text = y[0, :, :, 0].cpu().data.numpy()
    score_link = y[0, :, :, 1].cpu().data.numpy()

    # refine link

    if refine_net is not None:
        with torch.no_grad():
            y_refiner = refine_net(y, feature)
        score_link = y_refiner[0, :, :, 0].cpu().data.numpy()

    t0 = time.time() - t0
    t1 = time.time()

    # Post-processing
    boxes, polys = craft_utils.getDetBoxes(score_text, score_link,
                                           text_threshold, link_threshold,
                                           low_text, poly)

    # coordinate adjustment
    boxes = craft_utils.adjustResultCoordinates(boxes, ratio_w, ratio_h)
    polys = craft_utils.adjustResultCoordinates(polys, ratio_w, ratio_h)
    for k in range(len(polys)):
        if polys[k] is None: polys[k] = boxes[k]

    t1 = time.time() - t1

    # render results (optional)
    render_img = score_text.copy()
    render_img = np.hstack((render_img, score_link))
    ret_score_text = imgproc.cvt2HeatmapImg(render_img)

    if args.show_time: print(
        "\ninfer/postproc time : {:.3f}/{:.3f}".format(t0, t1))

    return boxes, polys, ret_score_text


def processing(image_list, result_folder, refine=True):

    global refine_net
    if not refine:
        refine_net = None
    # try:
    for k, image_path in enumerate(image_list):
        image = imgproc.loadImage(image_path)
        bboxes, polys, score_text = test_net(net, image, args.text_threshold,
                                             args.link_threshold,
                                             args.low_text, args.cuda,
                                             args.poly, refine_net)

        # save score text
        filename, file_ext = os.path.splitext(os.path.basename(image_path))
        mask_file = os.path.join(result_folder, filename + '_mask.jpg')
        cv2.imwrite(mask_file, score_text)

        file_utils.saveResult(image_path, image[:, :, ::-1], polys,
                              dirname=result_folder)




net = CRAFT()  # initialize

net, args.poly = loader_(net, args.trained_model, args.cuda, args.refine, True)
refine_net, args.poly = loader_(net, args.refiner_model, args.cuda, args.refine,
                                False)


def inference(req_json):

    """ For test images in a folder """
    image_list, _, _ = file_utils.get_files(req_json['test_folder'])
    result_folder = req_json['result_folder']
    if not os.path.isdir(result_folder):
        os.mkdir(result_folder)
    processing(image_list, result_folder, False)
    return


