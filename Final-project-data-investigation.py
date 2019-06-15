# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 09:51:06 2019

@author: Hamid.t
"""
from sklearn.datasets import load_breast_cancer
import seaborn as sns
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np


os.makedirs('./plots', exist_ok=True)


# loading data
cancer = load_breast_cancer()

y = pd.DataFrame(cancer.target)
X = pd.DataFrame(cancer.data)
X.columns= cancer.feature_names

y.columns=['diagnosis']
y['diagnosis'].replace(1,'M',inplace=True)
y['diagnosis'].replace(0,'B',inplace=True)


X.dropna(inplace=True)
y.dropna(inplace=True)
frames=[X,y]
data_com=pd.concat(frames,axis=1)

# initialize some package settings
sns.set(style="whitegrid",context='talk')

# generate a scatter plot matrix with the "mean" columns
cols = ['diagnosis',
        'mean radius', 
        'mean texture', 
        'mean perimeter', 
        'mean area', 
        'mean smoothness', 
        'mean compactness', 
        'mean concavity',
        'mean concave points', 
        'mean symmetry', 
        'mean fractal dimension']

sns.pairplot(data=data_com[cols], hue='diagnosis')

plt.savefig('plots/pair_mean.jpg',dpi=600)

#generate scatter plot with "worst" columns
cols = ['diagnosis',
        'worst radius', 
        'worst texture', 
        'worst perimeter', 
        'worst area', 
        'worst smoothness', 
        'worst compactness', 
        'worst concavity',
        'worst concave points', 
        'worst symmetry', 
        'worst fractal dimension']

sns.pairplot(data=data_com[cols], hue='diagnosis', palette='RdBu')
plt.savefig('plots/pair_worst.jpg')

#generate heat map
corr = X.corr().round(2)

# Mask for the upper triangle
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True

# Set figure size
f, ax = plt.subplots(figsize=(20, 20))

# Define custom colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Draw the heatmap
sns.heatmap(corr, mask=mask, cmap=cmap, vmin=-1, vmax=1, center=0,
            square=True, linewidths=1, cbar_kws={"shrink": .3}, annot=True)
plt.tight_layout()
plt.savefig('plots/Heat_map.jpg')