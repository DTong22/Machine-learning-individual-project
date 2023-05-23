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

files = ['set_1', 'set_2', 'set_3', 'set_4', 'set_5']

for dset in files:
    file = dset +'.csv'
    df = pd.read_csv(file)
    
    df.columns = ['Structure', 't_half']
    df = df[df['t_half'].notna()]
    
    X = df.drop(columns = ['Structure'])
    #labels
    y = df['Structure']
       
    #create random train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2,random_state = (1))
    
    #scale data
    scaler = StandardScaler().fit(X_train)
    X_train= scaler.transform(X_train)
    X_test = scaler.transform(X_test)
   
    lr  = LogisticRegression(multi_class='ovr', random_state=1)
    svc = SVC(probability=True)
    knn = KNeighborsClassifier()
    rfc = RandomForestClassifier(random_state=1)
    dtc = DecisionTreeClassifier(random_state=1)
    mlp = MLPClassifier()
    
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
    
    print(dset, df)
    ax = df.plot.bar(rot=0, figsize=[12,10])


