import pandas as pd

#1.Load the dataset
file_path = "appleAppData.csv"
dataset = pd.read_csv(file_path)


#Exploring the dataset
print(dataset.head()) #Display the first few rows of the dataset
print(dataset.info()) #Check the column names and data types
print(dataset.describe()) #Get a summary of numerical columns
print(dataset.shape) #Number of rows and columns



#2. Data Preprocessing

#2.1Check for missing values
missing_values = dataset.isnull().sum()

#Writing the data returned from missing_values to a text file for use in future documentation
with open("missing_values_summary.txt", "w") as file:
    file.write("Missing values in each column:\n")
    file.write(missing_values.to_string())

print("Missing values in each column: \n", missing_values)


#Drop rows with missing App_Name and Released
dataset = dataset.dropna(subset=['App_Name','Released'])

#Fill missing Size_Bytes with the median value
median_size = dataset['Size_Bytes'].median()
dataset['Size_Bytes'] = dataset['Size_Bytes'].fillna(median_size)


#Fill missing Price with 0
dataset['Price'] = dataset['Price'].fillna(0)

#Drop irrelevant columns with too many missing values
dataset = dataset.drop(columns=['Developer_Url','Developer_Website'])

# Verify missing values are handled
print("Remaining missing values:\n", dataset.isnull().sum())