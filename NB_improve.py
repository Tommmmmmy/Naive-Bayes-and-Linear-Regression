import os
import re
from math import log
path1 = './hw2_train/train/ham'
path2 = './hw2_train/train/spam'
path3 = './hw2_test/test/ham'
path4 = './hw2_test/test/spam'
dict = {}
dict["ham"] = {}
dict["spam"] = {}
stop_list = set()

content = open("./stopwords.txt", "r")
for line in content:
    stop_list.add(re.compile("[^a-zA-Z']+").sub(' ', line).strip())

count_element = []
num = 0
for filename in os.listdir(path1):
    content = open(os.path.join(path1, filename), "r")
    for line in content:
        line = line.strip()
        # pattern = re.compile("[^a-zA-Z']+")
        for element in line.replace(" ' ", "'").strip().split(" "):
            if (not element == "") and (element.lower() not in stop_list):
                num += 1
                if dict["ham"].__contains__(element):
                    dict["ham"][element] += 1
                else:
                    dict["ham"][element] = 1
                    dict["spam"][element] = 0
            # if element not in word1 and (not element == ""):
            #     word1.add(element)
count_element.append(num)
            # for element in list:
            #     print element

num = 0
for filename in os.listdir(path2):
    content = open(os.path.join(path2, filename), "r")
    for line in content:
        line = line.strip()
        pattern = re.compile("[^a-zA-Z']+")
        for element in line.replace(" ' ", "'").strip().split(" "):
            if (not element == "") and (element.lower() not in stop_list):
                num += 1
                if dict["spam"].__contains__(element):
                    dict["spam"][element] += 1
                else:
                    dict["spam"][element] = 1
                    dict["ham"][element] = 0
count_element.append(num)
# print len(dict["ham"])
# print count_element[0]
# print count_element[1]
count_ham = len(os.listdir(path1))
count_spam = len(os.listdir(path2))
count = count_ham + count_spam
# print prior_spam
# print prior_ham



# dict = {}
# for word in words:
#     list = []
#     num = 0
#     for filename in os.listdir(path1):
#         content = open(os.path.join(path1, filename), "r")
#         for line in content:
#             line = line.strip()
#             pattern = re.compile("[^a-zA-Z]+")
#             for element in pattern.sub(' ', line).strip().split(" "):
#                 if word == element:
#                     num += 1
#     list.append(num)
#     num = 0
#     for filename in os.listdir(path2):
#         content = open(os.path.join(path2, filename), "r")
#         for line in content:
#             line = line.strip()
#             pattern = re.compile("[^a-zA-Z]+")
#             for element in pattern.sub(' ', line).strip().split(" "):
#                 if word == element:
#                     num += 1
#     list.append(num)
#     dict[word] = list
# print dict
score = {}
result = {}
result["ham"] = {}
result["spam"] = {}
result["ham"]["F"] = 0
result["ham"]["T"] = 0
result["spam"]["F"] = 0
result["spam"]["T"] = 0

for filename in os.listdir(path3):
    content = open(os.path.join(path3, filename), "r")
    score["ham"] = log(1.0 * count_ham / count, 2)
    score["spam"] = log(1.0 * count_spam / count, 2)
    for line in content:
        line = line.strip()
        pattern = re.compile("[^a-zA-Z]+")
        for element in line.replace(" ' ", "'").strip().split(" "):
            if dict["ham"].__contains__(element):
                score["ham"] += log(1.0*(dict["ham"][element]+1)/(count_element[0]+len(dict["ham"])),2)
                score["spam"] += log(1.0*(dict["spam"][element] + 1) / (count_element[1] + len(dict["spam"])),2)
    if score["ham"] < score["spam"]:
        result["ham"]["F"] += 1
    else:
        result["ham"]["T"] += 1

for filename in os.listdir(path4):
    content = open(os.path.join(path4, filename), "r")
    score["ham"] = log(1.0 * count_ham / count, 2)
    score["spam"] = log(1.0 * count_spam / count, 2)
    for line in content:
        line = line.strip()
        pattern = re.compile("[^a-zA-Z]+")
        for element in pattern.sub(' ', line).strip().split(" "):
            if dict["spam"].__contains__(element):
                score["ham"] += log(1.0*(dict["ham"][element] + 1) / (count_element[0] + len(dict["ham"])),2)
                score["spam"] += log(1.0*(dict["spam"][element] + 1) / (count_element[1] + len(dict["spam"])),2)
    if score["ham"] < score["spam"]:
        result["spam"]["T"] += 1
    else:
        result["spam"]["F"] += 1

print 'ham: ' + str(
            1.0 * result["ham"]["T"] / (result["ham"]["T"] + result["ham"]["F"])) + "\n" + 'spam: ' + str(
            1.0 * result["spam"]["T"] / (result["spam"]["T"] + result["spam"]["F"]))


