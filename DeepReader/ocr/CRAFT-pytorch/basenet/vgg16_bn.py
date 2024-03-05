from collections import namedtuple
import torch
import os
import torch.nn as nn
import torch.nn.init as init
from torchvision import models
from torchvision.models.vgg import model_urls
# torch.set_num_threads(os.cpu_count())
def init_weights(modules):
    for m in modules:
        if isinstance(m, nn.Conv2d):
            init.xavier_uniform_(m.weight.data)
            if m.bias is not None:
                m.bias.data.zero_()
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
        elif isinstance(m, nn.Linear):
            m.weight.data.normal_(0, 0.01)
            m.bias.data.zero_()

class vgg16_bn(torch.nn.Module):
    def __init__(self, pretrained=False, freeze=True):
        super(vgg16_bn, self).__init__()
        model_urls['vgg16_bn'] = model_urls['vgg16_bn'].replace('https://', 'http://')
        vgg_pretrained_features = models.vgg16_bn(pretrained=pretrained).features

        self.slice1 = torch.nn.Sequential()
        self.slice2 = torch.nn.Sequential()
        self.slice3 = torch.nn.Sequential()
        self.slice4 = torch.nn.Sequential()
        self.slice5 = torch.nn.Sequential()

        # for x in range(12):  # conv2_2
        #     self.slice1.add_module(str(x), vgg_pretrained_features[x])

        self.slice1.add_module(str(0), nn.Conv2d(3, 4, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)))
        self.slice1.add_module(str(1), nn.BatchNorm2d(4, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True))
        self.slice1.add_module(str(2), nn.ReLU(inplace=True))
        self.slice1.add_module(str(3), nn.Conv2d(4, 4, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)))
        self.slice1.add_module(str(4), nn.BatchNorm2d(4, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True))
        self.slice1.add_module(str(5), nn.ReLU(inplace=True))
        self.slice1.add_module(str(6), nn.MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False))
        self.slice1.add_module(str(7), nn.Conv2d(4, 8, kernel_size=3, padding=1, stride=1))
        self.slice1.add_module(str(8), nn.BatchNorm2d(8, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True))
        self.slice1.add_module(str(9), nn.ReLU(inplace=True))
        self.slice1.add_module(str(10), nn.Conv2d(8, 8, kernel_size=3, padding=1, stride=1))
        self.slice1.add_module(str(11), nn.BatchNorm2d(8, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True))

        # for x in range(12, 19):         # conv3_3
        #     self.slice2.add_module(str(x), vgg_pretrained_features[x])

        self.slice2.add_module(str(12), nn.ReLU(inplace=True))
        self.slice2.add_module(str(13), nn.MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False))
        self.slice2.add_module(str(14), nn.Conv2d(8, 16, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)))
        self.slice2.add_module(str(15), nn.BatchNorm2d(16, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True))
        self.slice2.add_module(str(16), nn.ReLU(inplace=True))
        self.slice2.add_module(str(17), nn.Conv2d(16, 16, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)))
        self.slice2.add_module(str(18), nn.BatchNorm2d(16, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True))

        # for x in range(19, 29):         # conv4_3
        #     self.slice3.add_module(str(x), vgg_pretrained_features[x])

        self.slice3.add_module(str(19), nn.ReLU(inplace=True))
        self.slice3.add_module(str(20), nn.Conv2d(16, 16, kernel_size=3, padding=1, stride=1))
        self.slice3.add_module(str(21), nn.BatchNorm2d(16, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True))
        self.slice3.add_module(str(22), nn.ReLU(inplace=True))
        self.slice3.add_module(str(23), nn.MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False))
        self.slice3.add_module(str(24), nn.Conv2d(16, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)))
        self.slice3.add_module(str(25), nn.BatchNorm2d(32, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True))
        self.slice3.add_module(str(26), nn.ReLU(inplace=True))
        self.slice3.add_module(str(27), nn.Conv2d(32, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)))
        self.slice3.add_module(str(28), nn.BatchNorm2d(32, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True))

        # for x in range(29, 39):         # conv5_3
        #     self.slice4.add_module(str(x), vgg_pretrained_features[x])

        self.slice4.add_module(str(29), nn.ReLU(inplace=True))
        self.slice4.add_module(str(30), nn.Conv2d(32, 32, kernel_size=3, padding=1, stride=1))
        self.slice4.add_module(str(31), nn.BatchNorm2d(32, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True))
        self.slice4.add_module(str(32), nn.ReLU(inplace=True))
        self.slice4.add_module(str(33), nn.MaxPool2d(kernel_size=2, stride=2, padding=0, dilation=1, ceil_mode=False))
        self.slice4.add_module(str(34), nn.Conv2d(32, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)))
        self.slice4.add_module(str(35), nn.BatchNorm2d(32, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True))
        self.slice4.add_module(str(36), nn.ReLU(inplace=True))
        self.slice4.add_module(str(37), nn.Conv2d(32, 32, kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)))
        self.slice4.add_module(str(38), nn.BatchNorm2d(32, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True))

        # fc6, fc7 without atrous conv
        self.slice5 = torch.nn.Sequential(
                nn.MaxPool2d(kernel_size=3, stride=1, padding=1),
                nn.Conv2d(32, 64, kernel_size=3, padding=6, dilation=6),
                nn.Conv2d(64, 64, kernel_size=1)
        )

        if not pretrained:
            init_weights(self.slice1.modules())
            init_weights(self.slice2.modules())
            init_weights(self.slice3.modules())
            init_weights(self.slice4.modules())

        init_weights(self.slice5.modules())        # no pretrained model for fc6 and fc7

        if freeze:
            for param in self.slice1.parameters():      # only first conv
                param.requires_grad= False


    def forward(self, X):
        h = self.slice1(X)
        h_relu2_2 = h

        # h = self.q_2(h)
        h = self.slice2(h)
        # h = self.dq_2(h)
        h_relu3_2 = h

        # h = self.q_3(h)
        h = self.slice3(h)
        # h = self.dq_3(h)
        h_relu4_3 = h

        # h = self.q_4(h)
        h = self.slice4(h)
        # h = self.dq_4(h)
        h_relu5_3 = h

        # h = self.q_5(h)
        h = self.slice5(h)
        # h = self.dq_5(h)
        h_fc7 = h

        vgg_outputs = namedtuple("VggOutputs", ['fc7', 'relu5_3', 'relu4_3', 'relu3_2', 'relu2_2'])
        out = vgg_outputs(h_fc7, h_relu5_3, h_relu4_3, h_relu3_2, h_relu2_2)
        return out

'''
class vgg16_bn(torch.nn.Module):
    def __init__(self, pretrained=True, freeze=True):
        super(vgg16_bn, self).__init__()
        model_urls['vgg16_bn'] = model_urls['vgg16_bn'].replace('https://', 'http://')
        vgg_pretrained_features = models.vgg16_bn(pretrained=pretrained).features
        self.slice1 = torch.nn.Sequential()
        self.slice2 = torch.nn.Sequential()
        self.slice3 = torch.nn.Sequential()
        self.slice4 = torch.nn.Sequential()
        self.slice5 = torch.nn.Sequential()
        for x in range(12):         # conv2_2
            self.slice1.add_module(str(x), vgg_pretrained_features[x])
        for x in range(12, 19):         # conv3_3
            self.slice2.add_module(str(x), vgg_pretrained_features[x])
        for x in range(19, 29):         # conv4_3
            self.slice3.add_module(str(x), vgg_pretrained_features[x])
        for x in range(29, 39):         # conv5_3
            self.slice4.add_module(str(x), vgg_pretrained_features[x])

        # fc6, fc7 without atrous conv
        self.slice5 = torch.nn.Sequential(
                nn.MaxPool2d(kernel_size=3, stride=1, padding=1),
                nn.Conv2d(512, 1024, kernel_size=3, padding=6, dilation=6),
                nn.Conv2d(1024, 1024, kernel_size=1)
        )

        if not pretrained:
            init_weights(self.slice1.modules())
            init_weights(self.slice2.modules())
            init_weights(self.slice3.modules())
            init_weights(self.slice4.modules())

        init_weights(self.slice5.modules())        # no pretrained model for fc6 and fc7

        if freeze:
            for param in self.slice1.parameters():      # only first conv
                param.requires_grad= False

    def forward(self, X):
        # torch.set_num_interop_threads(8)
        # torch.set_num_threads(8)
        print (torch.get_num_threads(),torch.get_num_interop_threads())
        h = self.slice1(X)
        h_relu2_2 = h
        print ("Completed first")
        h = self.slice2(h)
        h_relu3_2 = h
        h = self.slice3(h)
        h_relu4_3 = h
        h = self.slice4(h)
        h_relu5_3 = h
        h = self.slice5(h)
        h_fc7 = h
        vgg_outputs = namedtuple("VggOutputs", ['fc7', 'relu5_3', 'relu4_3', 'relu3_2', 'relu2_2'])
        out = vgg_outputs(h_fc7, h_relu5_3, h_relu4_3, h_relu3_2, h_relu2_2)
        return out'''
