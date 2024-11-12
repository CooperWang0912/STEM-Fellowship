import csv

training = []

csvFile = open("", "r")  # Open the data file
reader = csv.reader(csvFile)
data = list(reader)  # Convert the data file into a list

datapoints = []
labels = []

for i in range(len(data) - 61):  # Separate the data into groups of 60 datapoints
    datapoints.append(data[i:i+60])
    labels.append(data[i:i+60])
