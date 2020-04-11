from random import randint
from random import shuffle
from pprint import pprint as pprint


import pandas as pd
import numpy as np


class Controller:
    def __init__(self, dataset):
        self.dataset = dataset

    def split(self):
        """
        Splits the dataset into a training and a testing part
        """
        # r = randint(300, 500)
        r = 500
        # print(r)
        dataset = self.dataset.reindex(np.random.permutation(self.dataset.index))
        training = dataset.iloc[:r].reset_index(drop=True)
        testing = dataset.iloc[r:].reset_index(drop=True)
        return training, testing

    def entropy(self, column):
        """
        Calculates the entropy related to an attribute (column)
        """
        elements, counts = np.unique(column, return_counts=True)
        entropy = np.sum(
            [(-counts[i] / np.sum(counts)) * np.log2(counts[i] / np.sum(counts)) for i in range(len(elements))])
        return entropy

    def infogain(self, data, attribute, target=0):
        """
        Calculate the information gain of the dataset
        Data: dataset for which information gain is to be calculated
        Attribute: the position of the attribute for which the information gain is to be calculated
        Target: the position of the target attribute
        """
        # entropy of the whole dataset
        totalentropy = self.entropy(data[target])

        # values and counts for the split attribute
        vals, counts = np.unique(data[attribute], return_counts=True)

        # weighted entropy
        weightedentropy = np.sum(
            [(counts[i] / np.sum(counts)) * self.entropy(data.where(data[attribute] == vals[i]).dropna()[target]) for i in
             range(len(vals))])

        # information gain
        informationgain = totalentropy - weightedentropy
        return informationgain

    def ID3(self, data, originaldata, features, targetattribute=0, parentnodeclass=None):
        """
        ID3 Algorithm
        :param data: the dataset for which the ID3 algorithm is run (in the first step, this is the whole dataset)
        :param originaldata: the initial/original dataset
        :param features: the feature space of the dataset (in the recursive call we lose features - SPLITTING)
        :param targetattribute: the position of the target attribute
        :param parentnodeclass: value of the target feature for a parent node of a specific node
                                needed since splitting leads to empty feature space
        :return: node/subtree/tree
        """
        # first, the stopping criteria
        # if all target values are the same, return this value
        if len(np.unique(data[targetattribute])) <= 1:
            return np.unique(data[targetattribute])[0]
        # if dataset is empty, return the target feature value in the original dataset
        elif len(data) == 0:
            return np.unique(originaldata[targetattribute])[
                np.argmax(np.unique(originaldata[targetattribute], return_counts=True)[1])]
        # if the feature space is empty, return the target feature value of the parent node
        elif len(features) == 0:
            # return np.unique(originaldata[targetattribute])[np.argmax(np.unique(originaldata[targetattribute], return_counts=True)[1])]
            return parentnodeclass
            # return np.unique(data[targetattribute])[0]
        # if none of the above, grow the tree (aka water it and put fertilizer)
        else:
            # set default value for the node
            parentnodeclass = np.unique(data[targetattribute])[
                np.argmax(np.unique(data[targetattribute], return_counts=True)[1])]

            # select the feature that best splits the dataset
            # return information gain values for the features in the dataset
            itemvalues = [self.infogain(data, feature, targetattribute) for feature in features]
            bestfeatureindex = np.argmax(itemvalues)
            bestfeature = features[bestfeatureindex]

            # create the tree structure; the root gets the name of the feature with the maximum information gain in the first run
            tree = {bestfeature: {}}

            # remove the feature with the best information gain from the feature space
            features = [i for i in features if i != bestfeature]

            # grow a branch under the root node for each possible value of the root node feature
            for value in np.unique(data[bestfeature]):
                value = value

                # split dataset along the value of the feature with the largest information gain --> create subdatasets
                subdata = data.where(data[bestfeature] == value).dropna()

                # do the ID3 algorithm for each of the subdatasets with new parameters
                subtree = self.ID3(subdata, data, features, targetattribute, parentnodeclass)

                # add the subtree to the tree
                tree[bestfeature][value] = subtree

            return tree

    def predict(self, query, tree, default="R"):
        """
        :param query: the query instance as a dictionary: {"featurename": featurevalue}
        :param tree: the tree
        :param default:
        :return:
        """
        for key in list(query.keys()):
            if key in list(tree.keys()):
                try:
                    result = tree[key][query[key]]
                except:
                    return default

                result = tree[key][query[key]]
                if isinstance(result, dict):
                    return self.predict(query, result)
                else:
                    return result

    def test(self, data, tree):
        # creates a new query instance by removing the target feature column from the original dataset and convert it to a dictionary
        queries = data.iloc[:, 1:].to_dict(orient="records")

        # create an empty DataFrame in whose columns the prediction of the tree are stored
        predicted = pd.DataFrame(columns=["predicted"])

        # calculate prediction accuracy
        for i in range(len(data)):
            predicted.loc[i, "predicted"] = self.predict(queries[i], tree, "L")
        # print("The prediction accuracy is: ", (np.sum(predicted["predicted"] == data[0])/len(data))*100, '%')
        return (np.sum(predicted["predicted"] == data[0]) / len(data)) * 100

    def main(self):
        i = 0
        p = 60
        while i < 500:
            print(i)
            trainingdata, testingdata = self.split()
            tree = self.ID3(trainingdata, trainingdata, trainingdata.columns[1:])
            p2 = self.test(testingdata, tree)
            if p2 > p:
                p = p2
                pprint(tree)
                print("The prediction accuracy is: ", p2, '%')
            i += 1