# -*- coding: utf-8 -*-
"""essai01.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lRnOy1VTsrjvu4EtmXnX3kz36G2Hej3m

#Diabetes Prediction

Diabetes is a chronic medical condition characterized by elevated levels of glucose (sugar) in the blood due to either insufficient insulin production or ineffective use of insulin by the body.

##Objective

We will try to build a machine learning model to accurately predict whether or not the patients in the dataset have diabetes or not

#Import Libraries
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from google.colab import files
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

"""#Set the Dataset"""

uploaded = files.upload()

"""#The Dataset

This dataset is originally from the National Institute of Diabetes and Digestive and Kidney Diseases. The objective of the dataset is to diagnostically predict whether or not a patient has diabetes, based on certain diagnostic measurements included in the dataset.

`The features:`
- Pregnancies: Number of times pregnant
- Glucose: Plasma glucose concentration from an oral tolerance test
- Blood Glucose:  Diastolic blood pressure (mm Hg)
- SkinThickness: Triceps skin fold thickness (mm)
- Insulin: 2-Hour serum insulin (mu U/ml)
- BMI: Body mass index (kg/m2)
- DiabetesPedigreeFunction: Diabetes pedigree function
- Age: Age (years)
- Outcome: Class variable (0 or 1)

#Load

load csv file diabetes.csv
"""

df = pd.read_csv('diabetes.csv')

"""#Inspecting Data

Get the first five lines
"""

df.head()

"""There are 768 lines"""

df.shape

"""Inspecting if there is a column with a string dtype"""

df.dtypes

"""There are no null values"""

df.info()

df.describe()

"""# Cleaning

## Duplicates
"""

df.duplicated().sum()

"""No Duplicates

## Missing Values
"""

df.isnull().any()

columns_without_target_col = df.columns[:-1]
columns_with_missing_vals = []
total_ms_vals = 0
for column in columns_without_target_col:
    ms_vals = len(df.loc[df[column] == 0, column])
    total_ms_vals += ms_vals
    print(f"{ms_vals / len(df[column]):>5.1%} Missing values in the {column} column ({ms_vals} values)")
    if ms_vals > 0:
        columns_with_missing_vals.append(column)

print(f"------\nTotal Missing values in the dataset : {total_ms_vals / df[columns_without_target_col].size:.0%} ({total_ms_vals}/{df[columns_without_target_col].size}) ")

"""# Data Visualization

## Histogram of features
"""

df.hist(figsize=(15,8))

"""## Correlation"""

#heatmap
correlation = df.corr()
sns.heatmap(correlation, annot=True)

"""We notice that the highest correlations with the Outcome are:
- Glucose
- BMI
- Age
Whilst Skin Thickness and Blood Pressure are almost unimportant

## Outcome Distribution

There is an imbalance of 15%:
- 34.9% don't have diabetes
- 65.1% have diabetes
"""

a = df['Outcome'].value_counts().plot.pie( autopct='%1.1f%%')
plt.show('Distribution of Diabetes')

"""## Boxplots"""

df.boxplot(figsize=(20, 10))
plt.show()

"""Comparison between Diabetic people and Non-Diabetics:"""

fig = plt.figure(figsize=(12, 15))

for i, col in enumerate(columns_without_target_col):
    ax = fig.add_subplot(len(columns_without_target_col) // 2, 2, i + 1)
    sns.boxplot(data=df, y=col, x='Outcome', ax=ax )
    ax.set_xlabel("")

plt.subplots_adjust(hspace=0.22, wspace=0.15)
plt.show()

"""Diabetics are/have more:
- Glucose
- Pregnancies
- Age
"""

features = df.drop(columns=['Outcome'])

features.head()

"""# Model Building

## Normalizing Features
"""

y = df['Outcome']

scaler = MinMaxScaler()

X = scaler.fit_transform(features)

X

"""## Split Train/Test"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state=42)

"""## Fix Imbalencement"""

sns.countplot(x='Outcome', data=df)  #data=df_diabetes_train)
plt.title("Count of Outcome (diabetes or not)")
plt.show()

#df_copy = pd.DataFrame(X,columns=df.columns[:-1])
#df_copy['Outcome'] = y

def balance_data_with_smote(X, y, target_column):
    #X = df.drop(columns=['Outcome'])
    #y = df['Outcome']
    X,y = SMOTE().fit_resample(X,y)
    res = pd.DataFrame(X,columns=df.columns[:-1])
    res['Outcome'] = y
    return res

balanced_df = balance_data_with_smote(X_train,y_train, 'Outcome')

sns.countplot(x='Outcome', data=balanced_df)  #data=df_diabetes_train)
plt.title("Count of Outcome (diabetes or not)")
plt.show()

"""## KNN Model"""

knn = KNeighborsClassifier(n_neighbors=1)

X_train_balanced = balanced_df.drop(columns=['Outcome'])
y_train_balanced = balanced_df['Outcome']

A = knn.fit(X_train_balanced,y_train_balanced)
B = knn.fit(X_train,y_train)

y_pred_A = A.predict(X_test)
y_pred_B = B.predict(X_test)

y_pred

from sklearn.metrics import confusion_matrix, classification_report

confusion_matrix(y_test,y_pred_A)

confusion_matrix(y_test,y_pred_B)

print(classification_report(y_test,y_pred_A))

print(classification_report(y_test,y_pred_B))

import numpy as np

error_rate = []
for i in range(1,40):
    knn = KNeighborsClassifier(n_neighbors = i)
    knn.fit(X_train,y_train)
    pred_i = knn.predict(X_test)

    error_rate.append(np.mean(pred_i != y_test))

plt.figure(figsize=(10, 6))

plt.plot(range(1, 40), error_rate, color='blue', linestyle='--', markersize=10, markerfacecolor='red', marker='o')

plt.title('K versus Error rate')

plt.xlabel('K')
plt.ylabel('Error rate')

#lowest error rate at 36

knn = KNeighborsClassifier(n_neighbors=13)
knn.fit(X_train, y_train)
predictions = knn.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))