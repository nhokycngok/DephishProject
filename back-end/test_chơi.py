a = [-1, 1, -1, -1, -1, -1, 1, -1, 0, -1, -1, -1, -1, 0, 1, -1, 0, -1, -1, -1]
print(len(a))
b = {}
for i in range(0, len(a)):
    temp = 'cot' + str(i + 1)
    b[temp] = a[i]

print(b)
#
def convert_dict_to_arry(dict_input):
    converted_array = []
    # dict_input = {'cot1': -1, 'cot2': 1, 'cot3': -1, 'cot4': -1, 'cot5': -1, 'cot6': -1, 'cot7': 1, 'cot8': -1, 'cot9': 0,
    #  'cot10': -1, 'cot11': -1, 'cot12': -1, 'cot13': -1, 'cot14': 0, 'cot15': 1, 'cot16': -1, 'cot17': 0, 'cot18': -1,
    #  'cot19': -1, 'cot20': -1}
    for key in dict_input.keys():
        converted_array.append(dict_input[key])
    return converted_array

print(convert_dict_to_arry(1))

# a = {"url":{"0":"https://bambooairway.vn/"},"having ip address":{"0":"-1"},"shortening service":{"0":"-1"},"missing title":{"0":"-1"},"domain contain -":{"0":"-1"},"redirect using //":{"0":"-1"},"HTTPS":{"0":"-1"},"favicon":{"0":"-1"},"link of tags link":{"0":"-1"},"server form handler":{"0":"-1"},"on mouse over":{"0":"-1"},"right click":{"0":"-1"},"popup window":{"0":"-1"},"url of anchor":{"0":"0"},"Links in script and link":{"0":"0"},"submitting to mail":{"0":"0"},"using iframe":{"0":"1"},"url of image":{"0":"-1"},"Fake Link In Status Bar":{"0":"-1"},"Percentage of URL external resource":{"0":"-1"},"frequent Domain Name Mismatch":{"0":"-1"}}
# print(len(a))
# b =[]
# for i in a.keys():
#     # b.a[i]['0']
#     if i != 'url':
#         b.append(int(a[i]['0']))
#
# print(b)


# import pickle
#
# from pandas import read_csv
#
# from sklearn.model_selection import train_test_split
#
# from sklearn.ensemble import RandomForestClassifier
#
#
#
# print("create model")
# # Load dataset
# test = [[-1, -1, -1, -1, -1, -1, 1, 0, -1, -1, -1, -1, 1, 0, 1, 1, 0, -1, 1, -1]]
#
# data_name = "csv/newdata.csv"
# name_model = "trained_model_5_7_ver_5_svc.pickle"
# name_of_model = "trained_model_5_7_ver_5_svc.pickle"
# name_of_data = "csv/newdata.csv"
# dataset = read_csv(data_name)
# array = dataset.values
#
#
#
# best_accuracy = 0
# for _ in range(20):
#     X = array[:, 0:20]
#     y = array[:, 20]
#     # data set to train and test 20 80
#     X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.20, random_state=0)
#     # algorithm
#     from sklearn.preprocessing import StandardScaler
#     sc = StandardScaler()
#     X_train = sc.fit_transform(X_train)
#     X_validation = sc.fit_transform((X_validation))
#     model = RandomForestClassifier()
#     # fit model
#     model.fit(X_train, Y_train)
#     accuracy = model.score(X_validation, Y_validation)
#     print(accuracy)
#     if accuracy > best_accuracy:
#         best_accuracy = accuracy
#         print("accuracy : ", best_accuracy)
#         # save model
#         with open(name_model, "wb") as file:
#             pickle.dump(model, file)
#     # print(best_accuracy)
# print("model trainning complated succesfully")
#
# predictions = model.predict(test)
# predictions_percent = model.predict_proba(test)
#
# print(predictions)
# print(predictions_percent)
