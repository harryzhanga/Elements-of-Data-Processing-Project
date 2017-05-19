import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import math
from knn_helper import *


#this is where you have put the training data
abs_path = 'D:\\University Content and Work\Computer Systems\Second year\Elements of Data Processing\Project\Project Phase 2A\Raw Data Files'


df = pd.read_csv(abs_path+"\Training.csv")
print("Thanks for using me, just need some info on the house: ")

myrow = []
myrow.append(int(input("Number of bathrooms: ")))
myrow.append(int(input("Number of car space: ")))
myrow.append(float(input("Land size in sqm: ")))
myrow.append(None)
myrow.append(int(input("Number of bedrooms: ")))
myrow.append(input("Suburb name: ").upper())
sub = myrow[-1]
df["Landsize"] = df["Landsize"].replace([0], 150)
rows = df.loc[df["Suburb"] == sub]
housemed = (rows["HouseMedian($)"].mean())
if math.isnan(housemed):
    housemed = df["HouseMedian($)"].mean()
percentage = rows["40+ Percentage"].mean()
if math.isnan(percentage):
    percentage = df["40+ Percentage"].mean()

print(df["Type"].unique())
myrow.append(input("Of those above, which one bests describes the type: ").upper())
myrow.append(housemed)
myrow.append(percentage)

columns = ["Bathrooms", "Car Spaces", "Land size in SQM", "Price", "Bedrooms", \
           "Suburb", "Type", "Median of Suburb (or avg if unrecognized)", "40+ Percentage (Study Scores"]
print("This is your input")
for (col, val) in zip(columns, myrow):
    print(col + " : " + str(val))

print("\nNeighbours: ")
myrow = dictify(myrow)
neighbours = neighbour_finder(10, df, myrow)
price = get_price(neighbours)
print("\nEstimated Price: ")
print("$"+str(price))
