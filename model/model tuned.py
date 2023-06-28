import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier 
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import warnings
warnings.filterwarnings("ignore")

class ModelEvaluator:
    def __init__(self, files):
        self.files = files
        self.models = [
            LogisticRegression(multi_class='ovr', random_state=1),
            SVC(probability=True),
            KNeighborsClassifier(),
            RandomForestClassifier(random_state=1),
            DecisionTreeClassifier(random_state=1),
            MLPClassifier()
        ]
        self.model_names = [
            'Logistic Regression',
            'SVM',
            'K Nearest Neighbors',
            'Random Forest',
            'Decision Tree',
            'Neural Network'
        ]
        self.metrics = ['accuracy score', 'f1 score', 'precision score', 'recall score']

    def evaluate_models(self):
        for dset in self.files:
            file = dset + '.csv'
            df = self.load_data(file)
            df = self.preprocess_data(df)
            X_train, X_test, y_train, y_test = self.split_data(df)
            scaled_X_train, scaled_X_test = self.scale_data(X_train, X_test)
            evaluation_results = self.evaluate_models_performance(scaled_X_train, y_train, scaled_X_test, y_test)
            self.display_results(dset, evaluation_results)

    def load_data(self, file):
        df = pd.read_csv(file)
        df.columns = ['Structure', 't_half']
        df = df.dropna(subset=['t_half'])
        return df

    def preprocess_data(self, df):
        X = df.drop(columns=['Structure'])
        y = df['Structure']
        return X, y

    def split_data(self, df):
        X, y = df
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)
        return X_train, X_test, y_train, y_test

    def scale_data(self, X_train, X_test):
        scaler = StandardScaler().fit(X_train)
        scaled_X_train = scaler.transform(X_train)
        scaled_X_test = scaler.transform(X_test)
        return scaled_X_train, scaled_X_test

    def evaluate_models_performance(self, X_train, y_train, X_test, y_test):
        evaluation_results = []
        for i, model in enumerate(self.models):
            params = self.get_hyperparameters(i)
            tuned_model = self.tune_model(model, params, X_train, y_train)
            y_pred = tuned_model.predict(X_test)
            scores = [
                accuracy_score(y_test, y_pred),
                f1_score(y_test, y_pred, average='weighted'),
                precision_score(y_test, y_pred, average='weighted', zero_division=0),
                recall_score(y_test, y_pred, average='weighted'),
            ]
            evaluation_results.append(scores)
        return evaluation_results

    def get_hyperparameters(self, model_index):
        if model_index == 0:  # Logistic Regression
            return {'C': [0.1, 1, 10], 'solver': ['lbfgs', 'liblinear']}
        elif model_index == 1:  # SVM
            return {'C': [0.1, 1, 10], 'kernel': ['linear', 'rbf'], 'gamma': ['scale', 'auto']}
        elif model_index == 2:  # KNN
            return {'n_neighbors': [3, 5, 7], 'weights': ['uniform', 'distance']}
        elif model_index == 3:  # Random Forest
            return {'n_estimators': [50, 100, 150], 'max_depth': [None, 5, 10]}
        elif model_index == 4:  # Decision Tree
            return {'max_depth': [None, 5, 10], 'min_samples_split': [2, 5, 10]}
        elif model_index == 5:  # MLP
            return {'hidden_layer_sizes': [(100,), (50, 50), (20, 20, 20)], 'alpha': [0.0001, 0.001, 0.01]}

    def tune_model(self, model, params, X_train, y_train):
        grid_search = GridSearchCV(model, params, cv=3)
        grid_search.fit(X_train, y_train)
        return grid_search.best_estimator_

    def display_results(self, dset, evaluation_results):
        df = pd.DataFrame(evaluation_results, index=self.model_names, columns=self.metrics)
        print(dset, df)

files = ['clusterdata_1000rea_20200318_reduced',
'clusterdata_1000rea_20200109_reduced',
'clusterdata_1000rea_20210406_reduced',
'clusterdata_1000rea_20210409_reduced',
'clusterdata_1000rea_20210416_reduced'
]
model_evaluator = ModelEvaluator(files)
model_evaluator.evaluate_models()
