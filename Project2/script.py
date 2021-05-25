import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score

from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

import sklearn.tree as tree

from sklearn.metrics import classification_report, accuracy_score, confusion_matrix



ten_k_fillings_data = pd.read_csv('10_k_fillings.csv')
ten_k_fillings_data.rename(columns={'Unnamed: 0':'Company'}, inplace=True)
clean_data = ten_k_fillings_data.drop(columns=["Company"])
#ten_k_fillings_data.head()

variation_data = pd.read_csv('price_variation.csv')
variation_data.rename(columns={'Unnamed: 0':'Company'}, inplace=True)
clean_data_test = variation_data.drop(columns=["Company"])
#variation_data.head()

#full_data = pd.merge(ten_k_fillings_data, variation_data, on='Company', how='inner')


# Create correlation matrix
corr_matrix = clean_data.corr().abs()

# Select upper triangle of correlation matrix
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))

# Find features with correlation greater than 0.95
to_drop = [column for column in upper.columns if any(upper[column] > 0.95)]

# Drop features 
clean_data.drop(to_drop, axis=1, inplace=True)


down_price_data = clean_data.loc[clean_data['class'] == 0]
up_price_data = clean_data.loc[clean_data['class'] == 1]

os_dataset = pd.concat([down_price_data.sample(n=451, random_state=1, replace=True), up_price_data])
us_dataset = pd.concat([down_price_data, up_price_data.sample(n=187, random_state=1)])



train_split, test_split = train_test_split(clean_data, random_state=1, test_size=0.25, stratify=clean_data['class'])

train_split_os, test_split_os = train_test_split(os_dataset, random_state=1, test_size=0.25, stratify=os_dataset['class'])

train_split_us, test_split_us = train_test_split(us_dataset, random_state=1, test_size=0.25, stratify=us_dataset['class'])

X_train = train_split.iloc[:, :-1].values
y_train = train_split.iloc[:, -1].values
X_test = test_split.iloc[:, :-1].values
y_test = test_split.iloc[:, -1].values

X_train_os = train_split_os.iloc[:, :-1].values
y_train_os = train_split_os.iloc[:, -1].values
X_test_os = test_split_os.iloc[:, :-1].values
y_test_os = test_split_os.iloc[:, -1].values

X_train_us = train_split_us.iloc[:, :-1].values
y_train_us = train_split_us.iloc[:, -1].values
X_test_us = test_split_us.iloc[:, :-1].values
y_test_us = test_split_us.iloc[:, -1].values


scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.fit_transform(X_train)
X_test = scaler.fit_transform(X_test)
X_train_os = scaler.fit_transform(X_train_os)
X_test_os = scaler.fit_transform(X_test_os)
X_train_us = scaler.fit_transform(X_train_us)
X_test_us = scaler.fit_transform(X_test_us)


#sb.pairplot(full_data, hue='class')


# for col in full_data.columns[2:]:
#     plt.suptitle(col)
#     plt.scatter(full_data[col], full_data[full_data.columns[-1]])
#     plt.show()
    

#full_data.head()



#DATA HANDLING
#full_data.describe()


#DECISION TREES
#all_inputs = full_data.drop(columns=["class","Company","2019 PRICE VAR [%]"])
#all_labels = full_data["class"].values

# model_accuracies = []
# for repetition in range(1000):
#     (training_inputs,
#      testing_inputs,
#      training_classes,
#      testing_classes) = train_test_split(all_inputs, all_labels, test_size=0.25)
    
#     # Create the classifier
#     decision_tree_classifier = DecisionTreeClassifier()
    
#     # Train the classifier on the training set
#     decision_tree_classifier.fit(training_inputs, training_classes)
    
#     # Validate the classifier on the testing set using classification accuracy
#     classifier_accuracy = decision_tree_classifier.score(testing_inputs, testing_classes)
    
#     model_accuracies.append(classifier_accuracy)

# plt.hist(model_accuracies)

#CROSS-VALIDATION
# decision_tree_classifier = DecisionTreeClassifier()
# cv_scores = cross_val_score(decision_tree_classifier, all_inputs, all_labels, cv=10)
# plt.hist(cv_scores)
# plt.title('Average score: {}'.format(np.mean(cv_scores)))


#PARAMETER TUNING
# decision_tree_classifier = DecisionTreeClassifier(max_depth=1)

# cv_scores = cross_val_score(decision_tree_classifier, all_inputs, all_labels, cv=10)
# plt.hist(cv_scores)
# plt.title('Average score: {}'.format(np.mean(cv_scores)))

# decision_tree_classifier = DecisionTreeClassifier()

# parameter_grid = {'max_depth': [1, 2, 3, 4, 5],
#                   'max_features': [1, 2, 3, 4]}

# cross_validation = StratifiedKFold(n_splits=10)

# grid_search = GridSearchCV(decision_tree_classifier,
#                            param_grid=parameter_grid,
#                            cv=cross_validation)

# grid_search.fit(all_inputs, all_labels)
# print('Best score: {}'.format(grid_search.best_score_))
# print('Best parameters: {}'.format(grid_search.best_params_))


# grid_visualization = grid_search.cv_results_['mean_test_score']
# grid_visualization.shape = (5, 4)
# sb.heatmap(grid_visualization, cmap='Blues', annot=True)
# plt.xticks(np.arange(4) + 0.5, grid_search.param_grid['max_features'])
# plt.yticks(np.arange(5) + 0.5, grid_search.param_grid['max_depth'])
# plt.xlabel('max_features')
# plt.ylabel('max_depth')
# ;




#DECISION TREES;
decision_tree_classifier = DecisionTreeClassifier(random_state=0)

parameter_grid = {'criterion': ['gini','entropy'],
                  'splitter': ['best', 'random'],
                  'max_depth': [1, 2, 3, 4, 5],
                  'max_features': [1, 2, 3, 4, 'sqrt', 'auto','log2']}

grid_search = GridSearchCV(decision_tree_classifier,
                            param_grid=parameter_grid,
                            scoring='precision_weighted',
                            cv=10)

grid_search.fit(X_train, y_train)
print('Best score: {}'.format(grid_search.best_score_))
print('Best parameters: {}'.format(grid_search.best_params_))


decision_tree_classifier = grid_search.best_estimator_

with open('iris_dtc.dot', 'w') as out_file:
    out_file = tree.export_graphviz(decision_tree_classifier, out_file=out_file)
   
predictions_train = grid_search.predict(X_train)
predictions_test = grid_search.predict(X_test) 

print(accuracy_score(y_train, predictions_train))

print(accuracy_score(y_test, predictions_test))

print(classification_report(y_train, predictions_train, target_names=['IGNORE', 'BUY']))
print(classification_report(y_test, predictions_test, target_names=['IGNORE', 'BUY']))
    
    
#SVM  
# svm_classifier = SVC(random_state=0)


# tuned_parameters = [{'kernel': ['rbf', 'linear','poly','sigmoid'], 
#                       'gamma': ['auto','scale', 1e-3, 1e-4], 
#                       'C': [0.01, 0.1, 1, 10, 100],
#                       'tol':[1e-4, 1e-3]}]


# grid_search = GridSearchCV(svm_classifier,
#                         param_grid=tuned_parameters,
#                             scoring='precision_weighted',
#                             n_jobs=-1,
#                             cv=10)

# grid_search.fit(X_train, y_train)

# print('Best score: {}'.format(grid_search.best_score_))
# print('Best parameters: {}'.format(grid_search.best_params_))

# predictions_train = grid_search.predict(X_train)
# predictions_test = grid_search.predict(X_test)

# print(accuracy_score(y_train, predictions_train))
# print(accuracy_score(y_test, predictions_test))
# print(classification_report(y_train, predictions_train, target_names=['Ignore', 'Buy']))
# print(classification_report(y_test, predictions_test, target_names=['Ignore', 'Buy']))


#MLP
# mlp_classifier = MLPClassifier(random_state=0, early_stopping=False)


# tuned_parameters = {'hidden_layer_sizes': [(32,), (64,), (32, 64, 32)],
#                     'activation': ['logistic','tanh', 'relu'],
#                     'solver': ['adam', 'sgd', 'lbfgs'],
#                     'alpha': [0.0001, 0.001, 0.01],
#                     'learning_rate': ['constant','adaptive'],
#                     'power_t': [0.25, 0.5, 0.75]}

# grid_search = GridSearchCV(mlp_classifier, 
#                     tuned_parameters,
#                     scoring='precision_weighted',
#                     n_jobs=-1,
#                     cv=10)

# grid_search.fit(X_train, y_train)

# print('Best score: {}'.format(grid_search.best_score_))
# print('Best parameters: {}'.format(grid_search.best_params_))

# predictions_train = grid_search.predict(X_train)
# predictions_test = grid_search.predict(X_test)


# print(accuracy_score(y_train, predictions_train))
# print(accuracy_score(y_test, predictions_test))

# print(confusion_matrix(y_train, predictions_train))
# print(confusion_matrix(y_test, predictions_test))

# print(classification_report(y_train, predictions_train, target_names=['IGNORE', 'BUY']))
# print(classification_report(y_test, predictions_test, target_names=['IGNORE', 'BUY']))


#KNN
# knn_classifier = KNeighborsClassifier()

# tuned_parameters = {'n_neighbors': list(range(1,30)),
#                     'weights': ['uniform','distance'],
#                     'p':[1,2]}

# grid_search = GridSearchCV(knn_classifier, 
#                     tuned_parameters,
#                     scoring='precision_weighted',
#                     n_jobs=-1,
#                     cv=10)


# grid_search.fit(X_train, y_train)

# print('Best score: {}'.format(grid_search.best_score_))
# print('Best parameters: {}'.format(grid_search.best_params_))

# predictions_train = grid_search.predict(X_train)
# predictions_test = grid_search.predict(X_test)


# print(accuracy_score(y_train, predictions_train))
# print(accuracy_score(y_test, predictions_test))

# print(confusion_matrix(y_train, predictions_train))
# print(confusion_matrix(y_test, predictions_test))

# print(classification_report(y_train, predictions_train, target_names=['IGNORE', 'BUY']))
# print(classification_report(y_test, predictions_test, target_names=['IGNORE', 'BUY']))


#Random Forest
# tuned_parameters = {'n_estimators': [2048],
#                     'max_features': ['auto', 'sqrt'],
#                     'max_depth': [4, 6, 8],
#                     'criterion': ['gini', 'entropy']}

# grid_search = GridSearchCV(RandomForestClassifier(),
#                     tuned_parameters,
#                     n_jobs=-1,
#                     scoring='precision_weighted',
#                     cv=10)

# grid_search.fit(X_train, y_train)

# print('Best score: {}'.format(grid_search.best_score_))
# print('Best parameters: {}'.format(grid_search.best_params_))

# predictions_train = grid_search.predict(X_train)
# predictions_test = grid_search.predict(X_test)


# print(accuracy_score(y_train, predictions_train))
# print(accuracy_score(y_test, predictions_test))

# print(confusion_matrix(y_train, predictions_train))
# print(confusion_matrix(y_test, predictions_test))

# print(classification_report(y_train, predictions_train, target_names=['IGNORE', 'BUY']))
# print(classification_report(y_test, predictions_test, target_names=['IGNORE', 'BUY']))


#Extreme Gradient Boosting
# tuned_parameters = {'learning_rate': [0.001],
#                     'max_depth': [4],
#                     'n_estimators': [2048]}

# grid_search = GridSearchCV(xgb.XGBClassifier(),
#                     tuned_parameters,
#                     n_jobs=-1,
#                     scoring='precision_weighted',
#                     cv=10)

# grid_search.fit(X_train, y_train)

# print('Best score: {}'.format(grid_search.best_score_))
# print('Best parameters: {}'.format(grid_search.best_params_))

# predictions_train = grid_search.predict(X_train)
# predictions_test = grid_search.predict(X_test)


# print(accuracy_score(y_train, predictions_train))
# print(accuracy_score(y_test, predictions_test))

# print(confusion_matrix(y_train, predictions_train))
# print(confusion_matrix(y_test, predictions_test))

# print(classification_report(y_train, predictions_train, target_names=['IGNORE', 'BUY']))
# print(classification_report(y_test, predictions_test, target_names=['IGNORE', 'BUY']))



