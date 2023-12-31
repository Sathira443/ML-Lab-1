# -*- coding: utf-8 -*-
"""Lab1_label3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dL_CruJNM00vZT9qN1241UIkmE9j9pqq

Load the datasets and import libraries
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA

df_train = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/train.csv")
df_test = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/valid.csv")

"""Seperate features and labels"""

df_train_X = df_train.drop(['label_1', 'label_2', 'label_3', 'label_4'], axis=1)
df_train_y = df_train['label_3']
df_test_X = df_test.drop(['label_1', 'label_2', 'label_3', 'label_4'], axis=1)
df_test_y = df_test['label_3']

"""Standardize the data"""

scaler = StandardScaler()
df_train_X_scaled = scaler.fit_transform(df_train_X)
df_test_X_scaled = scaler.transform(df_test_X)

"""Initialize and fit the k-NN model before PCA"""

model_before = RandomForestClassifier()
model_before.fit(df_train_X_scaled, df_train_y)
y_pred_before = model_before.predict(df_test_X_scaled)

"""Perform PCA and transform data using PCA"""

pca = PCA(n_components=0.95)
pca.fit(df_train_X_scaled)

pca_df_train_X = pca.transform(df_train_X_scaled)
pca_df_test_X = pca.transform(df_test_X_scaled)

"""Initialize and fit the k-NN model after PCA"""

model_after = RandomForestClassifier()
model_after.fit(pca_df_train_X, df_train_y)
y_pred_after = model_after.predict(pca_df_test_X)

"""Create a DataFrame for the transformed data"""

feature_names = [f"new_feature_{i}" for i in range(1, pca_df_test_X.shape[1] + 1)]
pca_df_test_X_df = pd.DataFrame(pca_df_test_X, columns=feature_names)

summary_df = pd.DataFrame({
    'Predicted labels before feature engineering': y_pred_before,
    'Predicted labels after feature engineering': y_pred_after,
    'No of new features': [pca_df_test_X.shape[1]] * len(df_test_X)
})

final_df = pd.concat([summary_df, pca_df_test_X_df], axis=1)

"""Save the final DataFrame to a CSV"""

csv_file_path = '../../Downloads/190359P_label_3.csv'
final_df.to_csv(csv_file_path, index=False)