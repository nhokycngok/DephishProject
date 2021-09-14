from pandas import read_csv
import pickle
import os.path
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier


def train_model(data_name, name_model, test):
    # check model exists
    try:
        if os.path.exists(name_model):
            print("loading trained model")
            model = pickle.load(open(name_model, 'rb'))
            predictions = model.predict(test)
            predictions_percent = model.predict_proba(test)
            return True, predictions, predictions_percent, "train_model True"
        else:
            print("create model")
            # Load dataset
            dataset = read_csv(data_name)
            array = dataset.values

            best_accuracy = 0
            for _ in range(5):
                X = array[:, 0:20]
                y = array[:, 20]
                # data set to train and test 20 80
                X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=1)
                # algorithm
                from sklearn.preprocessing import StandardScaler
                sc = StandardScaler()
                X_train = sc.fit_transform(X_train)
                X_validation = sc.fit_transform((X_validation))
                model = RandomForestClassifier()
                # fit model
                model.fit(X_train, Y_train)
                accuracy = model.score(X_validation, Y_validation)
                print(accuracy)
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    print("accuracy : ", best_accuracy)
                    # save model
                    with open(name_model, "wb") as file:
                        pickle.dump(model, file)
                # print(best_accuracy)
            print("model trainning complated succesfully")

            predictions = model.predict(test)
            predictions_percent = model.predict_proba(test)

            return True, predictions, predictions_percent, "train_model True"

    except Exception as e:
        print(e)
        return False, -3, -3, "exception at func train_model"
