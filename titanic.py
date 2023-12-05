import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

titanic_data = pd.read_csv('train.csv')

# print(titanic_data.head())
# print(titanic_data.info())
# print(titanic_data.describe())

# print(titanic_data.isnull().sum()) # count missing values
titanic_data_cleaned = titanic_data.drop('Cabin', axis=1) # drop the Cabin column
titanic_data_cleaned = titanic_data_cleaned.dropna() # drop missing values

# example 1 - simple bar plot of survival counts
sb.countplot(x='Survived', data=titanic_data_cleaned)
plt.show()

# example 2 - bar plot for passenger class counts
sb.countplot(x='Pclass', data=titanic_data_cleaned, palette='viridis')
plt.xlabel('Passenger Class')
plt.ylabel('Count')
plt.title('Passenger Class Counts')
plt.show()

# example 3 - histogram for passenger ages
plt.hist(titanic_data_cleaned['Age'].dropna(), bins=30, color='skyblue', edgecolor='black')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title('Histogram for Passenger Ages')
plt.show()

# example 4 - scatter plot of fares vs ages
sb.scatterplot(x='Age', y='Fare', data=titanic_data_cleaned, hue='Survived', palette='coolwarm', alpha=0.7)
plt.xlabel('Age')
plt.ylabel('Fare')
plt.title('Scatter Plot of Fares vs Ages')
plt.legend(title='Survived', loc='upper right')
plt.show()

# example 5 - box plot of fare distibution by passenger class
sb.boxplot(x='Pclass', y='Fare', data=titanic_data_cleaned, palette='Set2')
plt.xlabel('Passenger Class')
plt.ylabel('Fare')
plt.title('Box Plot of Fare Distribution by Passenger Class')
plt.show()

# creating a new feature for 'FamilySize'
# combine 'SibSp' and 'Parch' from the data
titanic_data_cleaned['FamilySize'] = titanic_data_cleaned['SibSp'] + titanic_data_cleaned['Parch']

# historgram for  our 'FamilySize' feature
plt.hist(titanic_data_cleaned['FamilySize'], bins=range(1, max(titanic_data_cleaned['FamilySize']) + 2), edgecolor='black')
plt.xlabel('Family Size')
plt.ylabel('Count')
plt.title('Distribution of Family Sizes')
plt.show()

# bar plot for our 'FamilySize' feature
sb.barplot(x='FamilySize', y='Survived', data=titanic_data_cleaned, ci=None)
plt.xlabel('Family Size')
plt.ylabel('Survival Rate')
plt.title('Survival Rate by Family Size')
plt.show()

# faceted histogram
# # example for VT
g = sb.FacetGrid(titanic_data_cleaned, col="Pclass", height=4)

# map a histogram onto the grid
g.map(plt.hist, "Age", bins=20, color="skyblue")

# set axis labels and plot title
g.set_axis_labels("Age", "Count")
g.set_titles(col_template="{col_name} class")

# show the plot
plt.show()