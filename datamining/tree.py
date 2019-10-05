import pandas as pd
import graphviz
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.model_selection import cross_val_score

class DTree:
    def __init__(self):
        self.model = DecisionTreeClassifier(max_depth=100)

    def load_data(self, data_path):
        self.data = pd.read_csv(data_path, sep=',', names=['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target'])
        self.data = self.data[self.data.age != '?']
        self.data = self.data[self.data.sex != '?']
        self.data = self.data[self.data.cp != '?']
        self.data = self.data[self.data.trestbps != '?']
        self.data = self.data[self.data.chol != '?']
        self.data = self.data[self.data.fbs != '?']
        self.data = self.data[self.data.restecg != '?']
        self.data = self.data[self.data.thalach != '?']
        self.data = self.data[self.data.exang != '?']
        self.data = self.data[self.data.oldpeak != '?']
        self.data = self.data[self.data.slope != '?']
        self.data = self.data[self.data.ca != '?']
        self.data = self.data[self.data.thal != '?']

        self.train = self.data.loc[:250, :]
        self.test = self.data.loc[251:, :]

        self.X_train = self.train.loc[:, 'age':'thal']
        self.X_test = self.test.loc[:, 'age':'thal']
        self.Y_train = self.train.loc[:, 'target']
        self.Y_test = self.test.loc[:, 'target']

        print('X_train:', self.X_train.shape)
        print('Y_tain:', self.Y_train.shape)
        print('X_test:', self.X_test.shape)
        print('Y_test:', self.Y_test.shape)

    def training(self):
        self.model.fit(self.X_train, self.Y_train)

    def validate(self):
        rp = cross_val_score(self.model, self.X_test, self.Y_test, scoring='accuracy', cv=2)
        rp2 = cross_val_score(self.model, self.X_train, self.Y_train, scoring='accuracy', cv=2)
        print('Train accuracy:', sum(rp2)/rp2.__len__())
        print('Test accuracy:', sum(rp)/rp.__len__())
        return sum(rp2)/rp2.__len__(), sum(rp)/rp.__len__()

    def predict(self, input):
        return self.model.predict(input)

    def plot(self):
        viz = tree.export_graphviz(self.model, out_file=None,
                                   feature_names=['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach',
                                                  'exang', 'oldpeak', 'slope', 'ca', 'thal'],
                                   class_names='target', filled=True, rounded=True, special_characters=True)
        graph = graphviz.Source(viz)
        graph.render('media/result')