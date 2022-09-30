import os, cv2
import numpy as np
import pandas as pd
#import random, tqdm
import seaborn as sns
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import albumentations as album
import segmentation_models_pytorch as smp
img=cv2.imread('4_5764945309327167165.jpg')
image=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
plt.imshow(image)
