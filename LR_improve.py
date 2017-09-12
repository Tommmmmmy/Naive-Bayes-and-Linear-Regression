import os
import re
from math import exp
class Logistic(object):
    learning_rate = 0.01
    lamb = 0.0001
    weights = {}
    stop_list = set()
    path1 = './hw2_train/train/ham'
    path2 = './hw2_train/train/spam'
    path3 = './hw2_test/test/ham'
    path4 = './hw2_test/test/spam'
    def __init__(self):
        content = open("./stopwords.txt", "r")
        for line in content:
            Logistic.stop_list.add(re.compile("[^a-zA-Z']+").sub(' ', line).strip())
        self.train()

    # def read(self):
    #     for filename in os.listdir(Logistic.path1):
    #         content = open(os.path.join(Logistic.path1, filename), "r")
    #         for line in content:
    #             line = line.strip()
    #             pattern = re.compile("[^a-zA-Z']+")
    #             for element in pattern.sub(' ', line).replace(" ' ", "'").strip().split(" "):
    #                 if not element == "":
    #                     if not Logistic.weights.__contains__(element):
    #                         Logistic.weights[element] = 0
    #     for filename in os.listdir(Logistic.path2):
    #         content = open(os.path.join(Logistic.path2, filename), "r")
    #         for line in content:
    #             line = line.strip()
    #             pattern = re.compile("[^a-zA-Z']+")
    #             for element in pattern.sub(' ', line).replace(" ' ", "'").strip().split(" "):
    #                 if not element == "":
    #                     if not Logistic.weights.__contains__(element):
    #                         Logistic.weights[element] = 0
    #         self.predict()

    def train(self):
        Logistic.weights["bias*"] = 0
        for num in range(0, 200):
            for filename in os.listdir(Logistic.path1):
                # print filename
                dict = {}
                content = open(os.path.join(Logistic.path1, filename), "r")
                for line in content:
                    line = line.strip()
                    # pattern = re.compile("[^a-zA-Z']+")
                    for element in line.replace(" ' ", "'").strip().split(" "):
                        if (not element == "") and (element not in Logistic.stop_list):
                            if dict.__contains__(element):
                                dict[element] += 1
                            else:
                                dict[element] = 1
                predict_val = self.predict_ham(dictionary=dict)
                Logistic.weights["bias*"] += Logistic.learning_rate * (
                1 - predict_val) - Logistic.learning_rate * Logistic.lamb * Logistic.weights["bias*"]
                for key in dict:
                    if key in Logistic.weights:
                        Logistic.weights[key] += Logistic.learning_rate * 1.0 * (1 - predict_val) * 1.0 * (dict[key]) - \
                                                 (Logistic.learning_rate * Logistic.lamb * Logistic.weights[key])
                    else:
                        Logistic.weights[key] = 0
            for filename in os.listdir(Logistic.path2):
                dict = {}
                content = open(os.path.join(Logistic.path2, filename), "r")
                for line in content:
                    line = line.strip()
                    # pattern = re.compile("[^a-zA-Z']+")
                    for element in line.replace(" ' ", "'").strip().split(" "):
                        if (not element == "") and (element not in Logistic.stop_list):
                            if dict.__contains__(element):
                                dict[element] += 1
                            else:
                                dict[element] = 1
                predict_val = self.predict_ham(dictionary=dict)
                Logistic.weights["bias*"] += Logistic.learning_rate * (
                    0 - predict_val) - Logistic.learning_rate * Logistic.lamb * Logistic.weights["bias*"]
                for key in dict:
                    if key in Logistic.weights:
                        Logistic.weights[key] += Logistic.learning_rate * 1.0 * (0 - predict_val) * 1.0 * dict[key] - \
                                                 (Logistic.learning_rate * Logistic.lamb * Logistic.weights[key])
                    else:
                        Logistic.weights[key] = 0

    def predict_ham(self, dictionary=None):
        val = 0.0
        for element in dictionary:
            if element in Logistic.weights:
                val += Logistic.weights[element] * dictionary[element]
        return 1.0 / (1.0 + exp(-val))

    # def predict_spam(self, dictionary=None):
    #     val = 0.0
    #     for element in dictionary:
    #         if element in Logistic.weights:
    #             val += Logistic.weights[element] * dictionary[element]
    #     return 1.0 / (1.0 + exp(val))

    def test(self):
        result = {}
        result["ham"] = {}
        result["spam"] = {}
        result["ham"]["F"] = 0
        result["ham"]["T"] = 0
        result["spam"]["F"] = 0
        result["spam"]["T"] = 0
        for filename in os.listdir(Logistic.path3):
            dict = {}
            content = open(os.path.join(Logistic.path3, filename), "r")
            for line in content:
                line = line.strip()
                pattern = re.compile("[^a-zA-Z]+")
                for element in line.replace(" ' ", "'").strip().split(" "):
                    if not element == "":
                        if dict.__contains__(element):
                            dict[element] += 1
                        else:
                            dict[element] = 1
            val = Logistic.weights["bias*"]
            for key in dict:
                if key in Logistic.weights:
                    val += Logistic.weights[key] * dict[key]
            if val > 0:
                result["ham"]["T"] += 1
            else:
                result["ham"]["F"] += 1
        for filename in os.listdir(Logistic.path4):
            dict = {}
            content = open(os.path.join(Logistic.path4, filename), "r")
            for line in content:
                line = line.strip()
                pattern = re.compile("[^a-zA-Z]+")
                for element in line.replace(" ' ", "'").strip().split(" "):
                    if not element == "":
                        if dict.__contains__(element):
                            dict[element] += 1
                        else:
                            dict[element] = 1
            val = Logistic.weights["bias*"]
            for key in dict:
                if key in Logistic.weights:
                    val += Logistic.weights[key] * dict[key]
            if val > 0:
                result["spam"]["F"] += 1
            else:
                result["spam"]["T"] += 1
        print 'lambda: ' + str(Logistic.lamb) + "\n" + 'ham: ' + str(1.0 * result["ham"]["T"] / (result["ham"]["T"] + result["ham"]["F"])) + "\n" + 'spam: ' + str(1.0 * result["spam"]["T"] / (result["spam"]["T"] + result["spam"]["F"]))


def main():
    logistic = Logistic()
    logistic.test()
if __name__ == "__main__":
    main()
