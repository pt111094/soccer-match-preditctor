import numpy as np
import pandas as pd
from sklearn import svm
import csv
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn import linear_model
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
def conv(s):
    try:
        s=float(s)
    except ValueError:
        pass    
    return s

with open('data_features.csv', 'rb') as f:
    reader = csv.reader(f)
    data = list(reader)
    #data = map(lambda x: float(x),data)
#print data
#print(data)
data = np.asarray(data)
training_data = data[:int(80.0/100.0*len(data)),:-1]
test_data = data[int(80.0/100.0*len(data)):,:-1]
print test_data
training_labels = data[:int(80.0/100.0*len(data)),-1]
test_labels = data[int(80.0/100.0*len(data)):,-1]
for i in range(0,len(training_data)):
    for j in range(0,len(training_data[i])):
        training_data = training_data.astype(np.float)

for i in range(0,len(test_data)):
    for j in range(0,len(test_data[i])):
        test_data = test_data.astype(np.float)

#training_data = training_data.astype(np.float)
print training_labels
clf = svm.LinearSVC(class_weight='balanced')
clf.fit(training_data,training_labels)
result1 = clf.predict(test_data)
print(classification_report(test_labels,result1))
print(accuracy_score(test_labels,result1))
print(result1)
print(type(training_data[0][1]))

clf = RandomForestClassifier(n_estimators=10)
clf = clf.fit(training_data, training_labels)
result1 = clf.predict(test_data)
print(classification_report(test_labels,result1))
print(accuracy_score(test_labels,result1))

gnb = GaussianNB()
gnb.fit(training_data, training_labels)
result1 = gnb.predict(test_data)
print(classification_report(test_labels,result1))
print(accuracy_score(test_labels,result1))
