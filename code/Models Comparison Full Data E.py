import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier 
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import warnings
warnings.filterwarnings("ignore")

df= pd.read_csv('fulldata.csv', header=None)
X = df.iloc[:,3:]
y = df.iloc[:,0]

#create random train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2,random_state = (1))

#scale data
scaler  = StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)
X_test  = scaler.transform(X_test)

lr  = LogisticRegression(C=10, multi_class='ovr', random_state=1, solver='newton-cg')
svc = SVC(C=1000, gamma=1, probability=True)
knn = KNeighborsClassifier(metric='euclidean', n_neighbors=1)
rfc = RandomForestClassifier(random_state=1)
dtc = DecisionTreeClassifier(criterion='entropy', max_depth=20, min_samples_leaf=5,random_state=1)
mlp = MLPClassifier(hidden_layer_sizes=(10, 30, 10))

models_list = [lr, svc, knn, rfc, dtc, mlp]
metrics_ls = ['accuracy score', 'f1 score', 'precision score', 'recall score']

ar = []

for model in models_list:
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)

    scores = [
        accuracy_score(y_test, y_pred),
        f1_score(y_test, y_pred, average= 'weighted'),
        precision_score(y_test, y_pred, average= 'weighted', zero_division=0),
        recall_score(y_test, y_pred, average= 'weighted'),
        ]
    ar.append(scores)
    
df = pd.DataFrame(ar, index =['Logistic Regression', 
                                'SVM',
                                'K Nearest Neighbors', 
                                'Random Forest',
                                'Decision Tree',
                                'Neural Network'
                                  ],
                                columns=metrics_ls)

print(df)
ax = df.plot.bar(rot=0, figsize=[12,10])
