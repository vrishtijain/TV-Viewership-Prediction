import pickle
import pandas as pd
from sklearn.svm import SVC
from sklearn import neighbors
from sklearn import preprocessing
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
# from __future__ import absolute_import
# from __future__ import division
# from __future__ import print_function

import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
import matplotlib



def train_classifier(features_train, features_test, label_train, label_test, c,i):
    if c == "Linear":
        model = LinearRegression()
    elif c == "Random_Forest":
        model= RandomForestRegressor(n_estimators=50)
    elif c == "Polynomial":
        poly_features = PolynomialFeatures(degree=1)
        features_train_poly = poly_features.fit_transform(features_train)
        model = LinearRegression()
        model.fit(features_train_poly, label_train)
        # predicting on training data-set
        y_train_predicted = model.predict(features_train_poly)

        # predicting on test data-set
        y_test_predict = model.predict(poly_features.fit_transform(features_test))

        # evaluating the model on training dataset
        rmse_train = np.sqrt(mean_squared_error(label_train, y_train_predicted))
        r2_train = r2_score(label_train, y_train_predicted)

        # evaluating the model on test dataset
        rmse_test = np.sqrt(mean_squared_error(label_test, y_test_predict))
        r2_test = r2_score(label_test, y_test_predict)

        # print("The model performance for the training set")
        # print("RMSE of training set is {}".format(rmse_train))
        # print("R2 score of training set is {}".format(r2_train))
        # print("The model performance for the test set")
        # print("RMSE of test set is {}".format(rmse_test))
        # print("R2 score of test set is {}".format(r2_test))
    elif c == "Kmeans":
        knn = neighbors.KNeighborsRegressor()
        params = {'n_neighbors': [2, 3, 4, 5, 6, 7, 8, 9]}
        model = GridSearchCV(knn, params, cv=5)
    else:
        print("Incorrect Selection Of Classifier")

    model.fit(features_train, label_train)

    # fileName = './Prediction_models/' + classifier + '.pickle'
    # with open(fileName, 'wb') as file:
    #     pickle.dump(model, file)
    # print("Pickle File Created %s" % fileName)
    if i ==1:
        accuracy = model.score(features_test, label_test)
        # print("Accuracy Is:", accuracy)

    return model

def main(simpsons_file):

    print('Viewership Prediction Started')
    viewer_data = pd.read_csv(simpsons_file, dtype={'Unique_Users': float, 'US_Viewers_In_Millions': float}, usecols = range(19), index_col = False, low_memory = False)
    viewer_data.dropna( inplace = True )
    print('Episode Data File Read Successful')

    x = viewer_data.loc[:, ['Views', 'IMDB_Rating', 'IMDB_Votes', 'Retweets', 'Favorites', 'Vader_Score', 'Sentiment_Score', 'Tweets_Per_Day', 'Unique_Users']]
    y = viewer_data.loc[:, ['US_Viewers_In_Millions']]
    x_temp =x
    y_temp =y
    scaler = MinMaxScaler( feature_range = (0, 1) )
    x = scaler.fit_transform(x)
    y = scaler.fit_transform(y)
    print('Data Rescaling Complete')

    x = preprocessing.scale(x)
    y = preprocessing.scale(y)
    print('Data Standardization Complete')

    # x = preprocessing.normalize(x)
    # y = preprocessing.normalize(y)
    # # print('Data Normalization Complete')

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)
    print("Shape of x_train: ", x_train.shape)
    print("Shape of y_train: ", y_train.shape)
    print("Shape of x_test: ", x_test.shape)
    print("Shape of y_test", y_test.shape)
    print('Data Sliced In Training And Testing Sets')

    print("Model Training Started")
    algorithm = "Random_Forest"
    model = train_classifier(x_train, x_test, y_train, y_test, algorithm,1)
    print("Model Training Complete")

    flat_list = []
    for sublist in y:
        for item in sublist:
            flat_list.append(item)


    scaler = MinMaxScaler( feature_range = (0, 1))
    x = scaler.fit_transform(x_temp)
    x = preprocessing.scale(x)
    x = preprocessing.normalize(x)
    x_train, x_test, y_train, y_test = train_test_split(x, y_temp, test_size = 0.2, random_state = 0)
    model = train_classifier(x_train, x_test, y_train, y_test, "Random_Forest",1)
    viewer_data['Predicted_Viewership'] = model.predict(x)
    viewer_data.to_csv('./Prediction_data/predicted_file.csv')
    plt.scatter(viewer_data['Predicted_Viewership'], y_temp, label='skitscat')
    plt.xlabel('Predicted Viewership')
    plt.ylabel('Actual Viewership')
    plt.title('Prediction vs Reality')
    plt.legend()
    plt.show()
    print("Done")

if __name__ == '__main__':
    main('./Prediction_data/simpsons_episodes.csv')
