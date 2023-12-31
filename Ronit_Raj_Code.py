# -*- coding: utf-8 -*-
"""Final2-Copy3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1outux7_ZrKqpm5fzTm56dtyGjoy_HKZU
"""

import numpy as np
import pandas as pd

file_path = "training_data.csv"
data = pd.read_csv(file_path)

print(data)

k = data.copy()
targets = pd.read_csv("training_data_targets.csv", names = ["Targets"])
k['Targets'] = targets
print(k)
k = pd.get_dummies(k, columns= ['Primary_Diagnosis'], dtype= int)
k.replace('GBM', 1, inplace= True)
k.replace('LGG', 0, inplace= True)
correlation = k['Primary_Diagnosis_Glioblastoma'].corr(k['Targets'])

print(correlation)
#Since the correlation is Almost 1, this ooverfits the data .I will be dropping this column to train my models more accurately.

column_name_to_drop = 'Primary_Diagnosis'
data = data.drop(column_name_to_drop, axis=1)

df_cleaned = pd.DataFrame(data)
df_cleaned.replace('--', None, inplace=True)
targets = pd.read_csv('training_data_targets.csv', names = ['Target'])
df_cleaned['Target'] = targets

# column_to_fill_with_mean = 'your_column_name'
# df[column_to_fill_with_mean] = df[column_to_fill_with_mean].fillna(df[column_to_fill_with_mean].mean())
# df_filled_with_mode = df.apply(lambda x: x.fillna(x.mode().iloc[0]))
# print(df_filled_with_mode)

print(df_cleaned.isna().sum())

# df_cleaned = df_cleaned.dropna()

print(df_cleaned)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# data = {'Target': ['LGG', 'GBM' ]}
# df_cleaned = pd.DataFrame(data)
class_counts = df_cleaned['Target'].value_counts()
plt.figure(figsize=(8, 6))
sns.barplot(x=class_counts.index, y=class_counts.values, palette='pastel')
plt.title('Number of Instances in Each Class')
plt.xlabel('Target Class')
plt.ylabel('Number of Instances')
plt.show()

k = []
for i in df_cleaned['Age_at_diagnosis']:
    if i == None:
        k.append(None)
    else:
        l = i.split(" ")
        k.append(l[0])

len(df_cleaned['Age_at_diagnosis'])
print(len(k))

j = []
for i in k:
    if i == None:
        j.append(None)
    else:

        j.append(int(i))
df_cleaned['Age_at_diagnosis'] = j

print(df_cleaned)

column_mean = 'Age_at_diagnosis'
df_cleaned[column_mean] = df_cleaned[column_mean].fillna(df_cleaned[column_mean].mean())
df_cleaned_mode = df_cleaned.apply(lambda x: x.fillna(x.mode().iloc[0]))
print(df_cleaned_mode)

c = df_cleaned_mode.columns

c = list(c)
c.remove('Target')
c.remove('Age_at_diagnosis')
print(c)

# columns_to_encode = list(range(3, 26))
df_encoded = pd.get_dummies(df_cleaned_mode, columns = c)
print(df_encoded)

print(df_encoded)



correlation_matrix = df_encoded.drop('Target', axis = 1).corr()
correlation_threshold = 0.5
highly_correlated_features = set()

for i in range(len(correlation_matrix.columns)):
    for j in range(i):
        if abs(correlation_matrix.iloc[i, j]) > correlation_threshold:
            colname = correlation_matrix.columns[i]
            highly_correlated_features.add(colname)

print(highly_correlated_features)

feature_data = df_encoded.drop(highly_correlated_features, axis=1)

feature_data.columns

X = feature_data.drop('Target', axis = 1)
y = feature_data['Target']

from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score ,classification_report ,confusion_matrix, make_scorer
from sklearn.model_selection import StratifiedKFold

#Decision Tree

dt_classifier = DecisionTreeClassifier()
f1_scorer = make_scorer(f1_score, average='weighted')

param_grid = {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best', 'random'],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

stratified_kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
grid_search = GridSearchCV(
    estimator=dt_classifier,
    param_grid=param_grid,
    cv=stratified_kfold,
    scoring=f1_scorer
)

grid_search.fit(X, y)
print("Best Hyperparameters:", grid_search.best_params_)
best_dt_model = grid_search.best_estimator_

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

y_pred = best_dt_model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

print("Metrics:")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

print("Classification Report:")
print(classification_report(y_test, y_pred))

print("Confusion Matrix:")
conf_matrix_dt = confusion_matrix(y_test, y_pred)
print(conf_matrix_dt)

from sklearn.model_selection import StratifiedKFold, GridSearchCV, train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

svm_classifier = SVC()

svm_param_grid = {
    'C': [0.1, 1, 10],
    'kernel': ['linear', 'rbf'],
    'gamma': ['scale', 'auto', 0.001, 0.01, 0.1, 1],
    'degree': [2, 3, 4],
    'coef0': [0.0, 1.0, 2.0],
    'shrinking': [True, False]
}


stratified_kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

svm_grid_search = GridSearchCV(
    estimator=svm_classifier,
    param_grid=svm_param_grid,
    cv=stratified_kfold,
    scoring='f1_macro',
)

svm_grid_search.fit(X, y)

print("Best SVM Hyperparameters:", svm_grid_search.best_params_)

svm_best_model = svm_grid_search.best_estimator_

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

svm_y_pred = svm_best_model.predict(X_test)

f1_macro = f1_score(y_test, svm_y_pred, average='macro')

print("\nSVM Metrics:")
print("F1 Score (Macro):", f1_macro)
print("\nSVM Classification Report:")
classification_report_svm = classification_report(y_test, svm_y_pred)
print(classification_report_svm)
print("\nSVM Confusion Matrix:")
conf_matrix_svm = confusion_matrix(y_test, svm_y_pred)
print(conf_matrix_svm)

#Adaboost

adaboost_classifier = AdaBoostClassifier()

adaboost_param_grid = {
    'n_estimators': [50, 100, 200],
    'learning_rate': [0.01, 0.1, 1],
    'base_estimator': [None, DecisionTreeClassifier(max_depth=1), DecisionTreeClassifier(max_depth=2)],
    'algorithm': ['SAMME', 'SAMME.R']
}

stratified_kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

adaboost_grid_search = GridSearchCV(
    estimator=adaboost_classifier,
    param_grid=adaboost_param_grid,
    cv=stratified_kfold,
    scoring='f1_macro'
)

adaboost_grid_search.fit(X_train, y_train)

print("\nBest AdaBoost Hyperparameters:", adaboost_grid_search.best_params_)

adaboost_best_model = adaboost_grid_search.best_estimator_

adaboost_y_pred = adaboost_best_model.predict(X_test)

f1_macro_adaboost = f1_score(y_test, adaboost_y_pred, average='macro')

print("\nAdaBoost Metrics:")
print("F1 Score (Macro):", f1_macro_adaboost)

print("\nAdaBoost Classification Report:")
classification_report_adaboost = classification_report(y_test, adaboost_y_pred)
print(classification_report_adaboost)

print("\nAdaBoost Confusion Matrix:")
conf_matrix_adaboost = confusion_matrix(y_test, adaboost_y_pred)
print(conf_matrix_adaboost)

#Logistic Regression

logreg_classifier = LogisticRegression()

logreg_param_grid = {
    'penalty': ['l1', 'l2', 'elasticnet', 'none'],
    'C': [0.001, 0.01, 0.1, 1, 10, 100],
    'fit_intercept': [True, False],
    'solver': ['newton-cg', 'lbfgs', 'liblinear', 'sag', 'saga'],
    'max_iter': [50, 100, 200],
    'multi_class': ['auto', 'ovr', 'multinomial'],
}

stratified_kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

logreg_grid_search = GridSearchCV(
    estimator=logreg_classifier,
    param_grid=logreg_param_grid,
    cv=stratified_kfold,
    scoring='f1_macro',
)

logreg_grid_search.fit(X_train, y_train)

print("\nBest Logistic Regression Hyperparameters:", logreg_grid_search.best_params_)

logreg_best_model = logreg_grid_search.best_estimator_
logreg_y_pred = logreg_best_model.predict(X_test)
f1_macro_logreg = f1_score(y_test, logreg_y_pred, average='macro')

print("\nLogistic Regression Metrics:")
print("F1 Score (Macro):", f1_macro_logreg)
print("\nLogistic Regression Classification Report:")
classification_report_logreg = classification_report(y_test, logreg_y_pred)
print(classification_report_logreg)
print("\nLogistic Regression Confusion Matrix:")
conf_matrix_logreg = confusion_matrix(y_test, logreg_y_pred)
print(conf_matrix_logreg)

#Random Forest

rf_classifier = RandomForestClassifier()

rf_param_grid = {
    'n_estimators': [50, 100, 200],
    'criterion': ['gini', 'entropy'],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': ['auto', 'sqrt', 'log2'],
    'bootstrap': [True, False],
}

stratified_kfold = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

rf_grid_search = GridSearchCV(
    estimator=rf_classifier,
    param_grid=rf_param_grid,
    cv=stratified_kfold,
    scoring='f1_macro',
)

rf_grid_search.fit(X_train, y_train)

print("\nBest Random Forest Hyperparameters:", rf_grid_search.best_params_)

rf_best_model = rf_grid_search.best_estimator_
rf_y_pred = rf_best_model.predict(X_test)
f1_macro_rf = f1_score(y_test, rf_y_pred, average='macro')

print("\nRandom Forest Metrics:")
print("F1 Score (Macro):", f1_macro_rf)
print("\nRandom Forest Classification Report:")
classification_report_rf = classification_report(y_test, rf_y_pred)
print(classification_report_rf)
print("\nRandom Forest Confusion Matrix:")
conf_matrix_rf = confusion_matrix(y_test, rf_y_pred)
print(conf_matrix_rf)

#K-Nearest Neighbour

knn_classifier = KNeighborsClassifier()

knn_param_grid = {
    'n_neighbors': [3, 4, 6, 5, 7 ,11],
    'weights': ['uniform', 'distance'],
    'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
    'leaf_size': [10, 20, 30, 40, 50],
    'p': [1, 2],
    'metric': ['euclidean', 'manhattan', 'minkowski'],
}

knn_grid_search = GridSearchCV(
    estimator=knn_classifier,
    param_grid=knn_param_grid,
    cv=5,
    scoring='f1_macro',
)

knn_grid_search.fit(X_train, y_train)

print("\nBest k-Nearest Neighbors Hyperparameters:", knn_grid_search.best_params_)

knn_best_model = knn_grid_search.best_estimator_
knn_y_pred = knn_best_model.predict(X_test)
f1_macro_knn = f1_score(y_test, knn_y_pred, average='macro')

print("\nk-Nearest Neighbors Metrics:")
print("F1 Score (Macro):", f1_macro_knn)
print("Accuracy:", accuracy_score(y_test, knn_y_pred))
print("Precision:", precision_score(y_test, knn_y_pred, average='weighted'))
print("Recall:", recall_score(y_test, knn_y_pred, average='weighted'))
print("\nk-Nearest Neighbors Classification Report:")
classification_report_knn = classification_report(y_test, knn_y_pred)
print(classification_report_knn)

conf_matrix_knn = confusion_matrix(y_test, knn_y_pred)
print(conf_matrix_knn)

#Labels
test_data = pd.read_csv('test_data.csv')
k = test_data["Age_at_diagnosis"]
new_age = []
a = 0
for i in k:
    if i == None:
        new_age.append(None)
    else:
        l = i.split()
        if len(l) > 2:
            if float(l[2]) > (366/2):
                new_age.append(int(l[0]) + 1)
            else:
                new_age.append(int(l[0]))
        else:
            new_age.append(int(l[0]))

test_data["Age_at_diagnosis"] = new_age
print("The data set now becomes")

import numpy as np
test_data.drop('Primary_Diagnosis', axis = 1, inplace = True)
final_data = pd.get_dummies(test_data, dtype = int)
l = np.zeros(87)
feature_data = final_data.drop(highly_correlated_features, axis=1)
feature_data.insert(2, 'Race_american indian or alaska native', l)
feature_data.insert(3, 'Race_asian', l)
feature_data.insert(17, 'BCOR_MUTATED', l)
feature_data.insert(18, 'CSMD3_MUTATED', l)

feature_data.columns

y_pred = adaboost_best_model.predict(feature_data)
feature_data['Labels'] = y_pred
for i in y_pred:
    print(i)

