# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 10:15:21 2019

@author: Hamid.t
"""
# importing libararies for calculations
import pandas as pd
import numpy as np

# importing libraries for plots 
import matplotlib.pyplot as plt 
import seaborn as sns

#importing libraries for laoding the dataset
from sklearn.datasets import load_breast_cancer


#importing libraries to calculate ROC 
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

import os
# preparing directories for saving plots
os.makedirs('./plots/pairs', exist_ok=True)
os.makedirs('./plots/comparative scatter', exist_ok=True)

# loading data
cancer = load_breast_cancer()

y = cancer.target
X = pd.DataFrame(cancer.data)
# setting colum names
X.columns= cancer.feature_names
y_plot=pd.DataFrame(y)
y_plot.columns=['diagnosis']

X_plot=X
y_plot['diagnosis'].replace(1,'M',inplace=True)
y_plot['diagnosis'].replace(0,'B',inplace=True)

# droppinh empty rows before plotting
X_plot.dropna(inplace=True)
y_plot.dropna(inplace=True)

frames=[X_plot,y_plot]
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
# saving the output plot
plt.savefig('plots/pairs/pair_mean.png',dpi=300)

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
plt.savefig('plots/pairs/pair_worst.png')

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
plt.savefig('plots/pairs/Heat_map.png')



# Splitting features and target datasets into: train and test
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35)

# Training a Linear Regression model with fit()
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression()
lr.fit(X_train, y_train)

# Predicting the results for our test dataset
predicted_values = lr.predict(X_test)

# Printing the residuals: difference between real and predicted
for (real, predicted) in list(zip(y_test, predicted_values)):
    print(f'Value: {real}, pred: {predicted} {"is different" if real != predicted else ""}')

# Printing accuracy score(mean accuracy) from 0 - 1
print(f'Accuracy score is {lr.score(X_test, y_test):.2f}/1 \n')

# Printing the classification report
from sklearn.metrics import classification_report, confusion_matrix, f1_score
print('Classification Report')
print(classification_report(y_test, predicted_values))

# Printing the classification confusion matrix (diagonal is true)
print('Confusion Matrix')
print(confusion_matrix(y_test, predicted_values))

print('Overall f1-score')
print(f1_score(y_test, predicted_values, average="macro"))

# calculating ROC and drawing the ROC figure


logit_roc_auc = roc_auc_score(y_test, lr.predict(X_test))

fpr, tpr, thresholds = roc_curve(y_test, lr.predict_proba(X_test)[:,1])
plt.figure()
plt.plot(fpr, tpr, label='Logistic Regression (area = %0.2f)' % logit_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.savefig('./plots/comparative scatter/Log_ROC')
plt.show()
