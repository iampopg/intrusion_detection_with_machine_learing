import pandas as pd
import numpy as np
import warnings
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import RFE
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

warnings.filterwarnings("ignore")

class IntrusionDetectionClassifier:
    def __init__(self, train_file, test_file):
        self.train = pd.read_csv(train_file)
        self.test = pd.read_csv(test_file)
        
    def explore_data(self):
        pass
        # print(self.train.head())
        # print("Training data has {} rows & {} columns".format(self.train.shape[0], self.train.shape[1]))
        # print(self.test.head())
        # print("Testing data has {} rows & {} columns".format(self.test.shape[0], self.test.shape[1]))
        
    def plot_class_distribution(self):
        ratio = self.train['class'].value_counts()
        labels = ratio.index[0], ratio.index[1]
        sizes = [ratio.values[0], ratio.values[1]]
        figure, axis = plt.subplots()
        axis.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        axis.axis('equal')
        plt.show()
        
    def clean_data(self):
        self.train.drop(['num_outbound_cmds'], axis=1, inplace=True)
        self.test.drop(['num_outbound_cmds'], axis=1, inplace=True)
        
        scaler = StandardScaler()

        cols = self.train.select_dtypes(include=['float64','int64']).columns
        sc_train = scaler.fit_transform(self.train.select_dtypes(include=['float64','int64']))
        sc_test = scaler.fit_transform(self.test.select_dtypes(include=['float64','int64']))

        self.sc_traindf = pd.DataFrame(sc_train, columns=cols)
        self.sc_testdf = pd.DataFrame(sc_test, columns=cols)

        encoder = LabelEncoder()

        cattrain = self.train.select_dtypes(include=['object']).copy()
        cattest = self.test.select_dtypes(include=['object']).copy()

        traincat = cattrain.apply(encoder.fit_transform)
        testcat = cattest.apply(encoder.fit_transform)

        enctrain = traincat.drop(['class'], axis=1)
        cat_Ytrain = traincat[['class']].copy()

        self.train_x = pd.concat([self.sc_traindf, enctrain], axis=1)
        self.train_y = self.train['class']

        self.test_df = pd.concat([self.sc_testdf, testcat], axis=1)
        
    def feature_selection(self):
        rfc = RandomForestClassifier()
        rfe = RFE(rfc, n_features_to_select=10)
        rfe = rfe.fit(self.train_x, self.train_y)

        feature_map = [(i, v) for i, v in itertools.zip_longest(rfe.get_support(), self.train_x.columns)]
        self.selected_features = [v for i, v in feature_map if i==True]

        sns.heatmap(self.train_x[self.selected_features].corr(), annot=True, fmt='.1g')
        plt.show()
        
    def train_and_evaluate_model(self):
        X_train, X_test, Y_train, Y_test = train_test_split(self.train_x, self.train_y, train_size=0.60, random_state=2)

        model = KNeighborsClassifier(n_jobs=-1)
        model.fit(X_train, Y_train)

        scores = cross_val_score(model, X_train, Y_train, cv=10)
        accuracy = metrics.accuracy_score(Y_train, model.predict(X_train))
        confusion_matrix = metrics.confusion_matrix(Y_train, model.predict(X_train))
        classification = metrics.classification_report(Y_train, model.predict(X_train))

        print("Cross Validation Mean Score:\n", scores.mean())
        print("Model Accuracy:\n", accuracy)
        print("Confusion matrix:\n", confusion_matrix)
        print("Classification report:\n", classification)

        accuracy = metrics.accuracy_score(Y_test, model.predict(X_test))
        confusion_matrix = metrics.confusion_matrix(Y_test, model.predict(X_test))
        classification = metrics.classification_report(Y_test, model.predict(X_test))

        print("Model Accuracy:\n", accuracy)
        print("Confusion matrix:\n", confusion_matrix)
        print("Classification report:\n", classification)
        
    def predict_test_data(self):
        model = KNeighborsClassifier(n_jobs=-1)
        model.fit(self.train_x, self.train_y)

        prediction = model.predict(self.test_df)
        self.test['prediction'] = prediction

        ratio = self.test['prediction'].value_counts()
        labels = ratio.index[0], ratio.index[1]
        sizes = [ratio.values[0], ratio.values[1]]

        figure, axis = plt.subplots()
        axis.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        axis.axis('equal')
        plt.show()

# if __name__ == "__main__":
#     train_file = "train.csv"
#     test_file = "test.csv"
    
#     intrusion_detection = IntrusionDetectionClassifier(train_file, test_file)
#     intrusion_detection.explore_data()
#     intrusion_detection.plot_class_distribution()
#     intrusion_detection.clean_data()
#     intrusion_detection.feature_selection()
#     intrusion_detection.train_and_evaluate_model()
#     intrusion_detection.predict_test_data()
