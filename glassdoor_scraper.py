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
metadata_df=pd.read_csv('metadata_csv')
class_dic= pd.read_csv('class_dict.csv')
metadata_df =metadata_df[metadata_df['split'] == 'train']
metadata_df =metadata_df[['image_id','sat_image_path','mask_path']]
metadata_df=metadata_df.sample(frac=1).reset_index(drop=True)
valid_df =metadata_df.sample(frac=0.1,random_state=42)
train_df= metadata_df.drop(valid_df.index)
