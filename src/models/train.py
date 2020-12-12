import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix

def train_model(source_dir, classifier, model_params):
    """
    Trains model with data preparation and desired classifier.
    """

    df = pd.read_csv(source_dir)
    X = df.drop(columns=['streaming']).values
    y = df['streaming'].values
    #Train test split of 70/30
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    #Normalizing data with respect to the entire training data
    scaler = StandardScaler()
    scaler.fit(X)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    #Choosing the desired model type
    classifier_type = {
        "RandomForest": RandomForestClassifier,
        "KNN": KNeighborsClassifier
    }

    model_params = model_params[classifier]
    clf = classifier_type[classifier](**model_params)

    #Outputting prediction and accuracy score
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print('%s model accuracy: %s' % (classifier, accuracy))

    return clf