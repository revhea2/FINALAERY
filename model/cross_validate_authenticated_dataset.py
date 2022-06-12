import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import numpy as np

dataset = pd.read_csv("auth_data.csv")
X = dataset.iloc[:, 0:18]
Y = dataset.iloc[:, 18]
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, random_state=0)

parameters = {
    "random_state": 82,
    "max_depth": 10,
    "n_estimators": 72,
}

random_forest_classifier = RandomForestClassifier(random_state=parameters["random_state"],
                                                  max_depth=parameters["max_depth"],
                                                  n_estimators=parameters["n_estimators"],
                                                  oob_score=True,
                                                  class_weight="balanced"
                                                  )

random_forest_classifier.fit(X_train, y_train)


y_pred = random_forest_classifier.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("OOB Score:", random_forest_classifier.oob_score_)


for i in range(2, 19):
    print(f"{i}-folds")
    cross_validation_mean_score = np.mean(cross_val_score(random_forest_classifier, X_train, y_train, cv=i))
    print("Cross Validation Score:", cross_validation_mean_score)


