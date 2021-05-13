import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score

from sklearn.model_selection import GridSearchCV

import sklearn.tree as tree

ten_k_fillings_data = pd.read_csv('10_k_fillings.csv')
ten_k_fillings_data.rename(columns={'Unnamed: 0':'Company'}, inplace=True)
#ten_k_fillings_data.head()

variation_data = pd.read_csv('price_variation.csv')
variation_data.rename(columns={'Unnamed: 0':'Company'}, inplace=True)
#variation_data.head()

full_data = pd.merge(ten_k_fillings_data, variation_data, on='Company', how='inner')


#sb.pairplot(full_data, hue='class')


# for col in full_data.columns[2:]:
#     plt.suptitle(col)
#     plt.scatter(full_data[col], full_data[full_data.columns[-1]])
#     plt.show()
    

#full_data.head()



#DATA HANDLING
full_data.describe()


#DECISION TREES
all_inputs = full_data.drop(columns=["class","Company","2019 PRICE VAR [%]"])
all_labels = full_data["class"].values

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

decision_tree_classifier = DecisionTreeClassifier()

parameter_grid = {'criterion': ['gini', 'entropy'],
                  'splitter': ['best', 'random'],
                  'max_depth': [1, 2, 3, 4, 5],
                  'max_features': [1, 2, 3, 4]}

cross_validation = StratifiedKFold(n_splits=10)

grid_search = GridSearchCV(decision_tree_classifier,
                           param_grid=parameter_grid,
                           cv=cross_validation)

grid_search.fit(all_inputs, all_labels)
print('Best score: {}'.format(grid_search.best_score_))
print('Best parameters: {}'.format(grid_search.best_params_))

decision_tree_classifier = grid_search.best_estimator_

with open('iris_dtc.dot', 'w') as out_file:
    out_file = tree.export_graphviz(decision_tree_classifier, out_file=out_file)








