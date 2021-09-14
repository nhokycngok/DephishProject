# Load libraries
import pickle
import os.path
from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

# Load libraries
from pandas import read_csv
from pandas.plotting import scatter_matrix
from matplotlib import pyplot
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import matplotlib.pyplot as plt
import numpy
from sklearn.ensemble import RandomForestClassifier


# def prediction(name_model, test):
#     try:
#         model = pickle.load(open(name_model, 'rb'))
#         predictions = model.predict(test)
#         return True, predictions, "prediction True"
#     except Exception as e:
#         print(e)
#         return False, -3,"exception at func prediction"


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
        return False, -3, "exception at func train_model"


def main():
    print("run")
    name_of_model = "trained_model_6_7_ver_2_randomforest.pickle"
    name_of_data = "csv/data.csv"

    # lst = [[-1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 1, 1, -1, 1, -1, 1, 1]]
    lst = [[-1, 1, -1, -1, -1, -1, 1, -1, 0, -1, -1, -1, -1, 0, 1, -1, 0, -1, -1, -1]]
    # lst = [[-1,-1,-1,-1,-1,-1,-1,0,0,-1,-1,-1,1,0,1,1,0,-1,1,-1]]
    # lst = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 1, -1, -1, -1, -1]]

    # lst = [[-1,-1,-1,-1,-1,-1,-1,1,1,-1,-1,-1,1,1,1,-1,1,-1,1,1],[-1,-1,-1,-1,-1,-1,1,1,-1,-1,-1,0,1,1,1,-1,1,-1,-1,-1],
    # [-1,-1,-1,-1,-1,-1,1,-1,-1,-1,-1,-1,1,0,1,-1,0,-1,1,-1],[-1,-1,-1,1,-1,-1,1,-1,-1,-1,-1,-1,0,0,1,1,1,-1,1,1],
    # [-1,-1,-1,1,-1,-1,1,0,-1,-1,-1,-1,1,1,1,-1,1,-1,1,-1],[-1,-1,-1,1,-1,-1,-1,-1,-1,-1,-1,-1,0,1,1,-1,1,-1,1,1]
    # ,[-1,-1,-1,-1,-1,-1,-1,0,1,-1,-1,-1,0,0,1,1,0,-1,-1,-1],[-1,-1,-1,-1,-1,-1,-1,0,1,-1,-1,-1,1,1,1,1,0,-1,-1,-1],
    # [-1,-1,-1,-1,-1,-1,1,-1,0,-1,-1,-1,-1,1,1,1,0,-1,-1,-1]
    # ]
    arr = numpy.array(lst)
    print(type(arr))
    status_train_model, pr, pr_percent, mess_train_model = train_model(name_of_data, name_of_model, arr)
    print(mess_train_model)
    print("predict : ", pr)
    print("pr_percent type: ", pr_percent)
    # print("pr_percent : ", (pr_percent[0].item(1)))
    if pr[0] == 1:
        print("pr_percent : ", pr_percent[0].item(1))
    elif pr[0] == -1:
        print("pr_percent : ", pr_percent[0].item(0))


if __name__ == "__main__":
    main()

# csv/new.csv

# print(predictions.shape)
# print(type(predictions))

# # Evaluate predictions

# print(confusion_matrix(Y_validation, predictions))
# print(classification_report(Y_validation, predictions))
