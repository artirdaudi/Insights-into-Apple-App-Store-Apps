import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import textwrap

def wrap_text(text):
    return "\n".join(textwrap.wrap(text, width=95))

def maximize_plot_window():
    manager = plt.get_current_fig_manager()
    manager.window.state('zoomed')

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


#Step 3: Data Cleaning and Transformation

#3.1 Removing duplicate rows
print("Number of duplicate rows before removal: ", dataset.duplicated().sum())
dataset = dataset.drop_duplicates()
print("Number of duplicate rows after removal: ", dataset.duplicated().sum())

#3.2 Standardize formats
dataset['App_Name'] = dataset['App_Name'].str.title()

#3.3 Encode categorical variables
dataset['Primary_Genre_Encoded'] = dataset['Primary_Genre'].astype('category').cat.codes 
dataset['Content_Rating_Encoded'] = dataset['Content_Rating'].astype('category').cat.codes
dataset['Currency_Encoded'] = dataset['Currency'].astype('category').cat.codes
dataset['Developer_Encoded'] = dataset['Developer'].astype('category').cat.codes
dataset['Free'] = dataset['Free'].astype(int)


#4. Statistical Analysis & 5. Data Visualisation

#Calculate the number of apps and average ratings for each genre
genre_popularity = dataset.groupby('Primary_Genre')['App_Id'].count()
genre_ratings = dataset.groupby('Primary_Genre')['Average_User_Rating'].mean()

#Combine into a single Dataframe for easier visualization
genre_data = pd.DataFrame({'Number_of_Apps': genre_popularity, 'Average_Rating': genre_ratings}).reset_index()

# Visualization: Bar plot for Genre Popularity and Ratings
plt.figure(figsize=(15,6))
sns.barplot(x='Number_of_Apps', y='Primary_Genre', data=genre_data.sort_values('Number_of_Apps', ascending=False))
plt.title('Number of Apps per Genre')
plt.suptitle(wrap_text("Games dominate the App Store, while Developer Tools have the fewest apps"), fontsize=10, y=1, color='gray')
plt.xlabel('Number of Apps')
plt.ylabel('Genre')
plt.show()

plt.figure(figsize=(15, 6))
sns.barplot(x='Average_Rating', y='Primary_Genre', data=genre_data.sort_values('Average_Rating', ascending=False))
plt.title('Average Ratings per Genre')
plt.suptitle(wrap_text("The Weather genre has the highest average ratings, suggesting that users highly value accurate and reliable weather apps. Popular genres like Games and Photo and Video also perform well in terms of user satisfaction. However, categories like Business and Food and Drink receive comparatively lower ratings, which may indicate room for improvement in user experience or functionality within these genres."), fontsize=10, y=1, color='gray')
plt.xlabel('Average Rating')
plt.ylabel('Genre')
plt.show()



#Free vs. Paid Apps - Ratings and Reviews
free_vs_paid = dataset.groupby('Free').agg({'Average_User_Rating': 'mean', 'Reviews': 'mean'}).reset_index()
free_vs_paid['Free'] = free_vs_paid['Free'].replace({1:'Free', 0:'Paid'})


# Visualization: Reviews for Free vs. Paid Apps
plt.figure(figsize=(10, 5))
sns.barplot(x='Free', y='Reviews', data=free_vs_paid, palette='coolwarm')
plt.title('Average Reviews: Free vs. Paid Apps', fontsize=14, fontweight='bold')
plt.suptitle(wrap_text("Free apps receive significantly more reviews than paid apps, indicating higher user engagement, possibly due to lower barriers to entry for free apps."), fontsize=10, y=0.95, color='gray')
plt.xlabel('App Type')
plt.ylabel('Average Reviews')
plt.show()


# Filter apps with prices > 0 for meaningful analysis
paid_apps = dataset[dataset['Price'] > 0]

# Visualization: Price Distribution
plt.figure(figsize=(12, 6))
sns.histplot(paid_apps['Price'], bins=30, kde=True, color='blue')
plt.title('Distribution of App Prices', fontsize=14, fontweight='bold')
plt.suptitle(wrap_text("Most paid apps are priced under $10, with a few outliers priced significantly higher. This indicates that the majority of apps are affordable for general users."), fontsize=10, y=0.95, color='gray')
plt.xlabel('Price ($)')
plt.ylabel('Frequency')
plt.show()


#Release Year Trends
# Extract the release year from the 'Released' column
dataset['Release_Year'] = pd.to_datetime(dataset['Released']).dt.year

# Number of apps released per year
yearly_releases = dataset.groupby('Release_Year')['App_Id'].count()

# Average ratings per year
yearly_ratings = dataset.groupby('Release_Year')['Average_User_Rating'].mean()

# Visualization: Number of Apps Released Per Year
plt.figure(figsize=(12, 6))
yearly_releases.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Number of Apps Released Per Year', fontsize=14, fontweight='bold')
plt.suptitle(wrap_text("The number of apps released each year shows growth trends, with notable peaks potentially aligned with technological advancements or significant App Store updates."), fontsize=10, y=0.95, color='gray')
plt.xlabel('Year')
plt.ylabel('Number of Apps')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Visualization: Average Ratings Per Year
plt.figure(figsize=(12, 6))
yearly_ratings.plot(kind='line', marker='o', color='green', linewidth=2)
plt.title('Average Ratings Per Year', fontsize=14, fontweight='bold')
plt.suptitle(wrap_text("Average user ratings over the years reveal whether app quality or user satisfaction has improved, declined, or remained stable over time."), fontsize=10, y=0.95, color='gray')
plt.xlabel('Year')
plt.ylabel('Average User Rating')
plt.grid(axis='both', linestyle='--', alpha=0.7)
plt.show()

#Most popular genre
# Group data by year and genre to count the number of apps
year_genre_counts = dataset.groupby(['Release_Year', 'Primary_Genre'])['App_Id'].count().reset_index()

# For each year, find the genre with the maximum uploads
top_genre_per_year = year_genre_counts.loc[year_genre_counts.groupby('Release_Year')['App_Id'].idxmax()]

# Visualization: Most Popular Genre Each Year
plt.figure(figsize=(12, 6))
sns.barplot(x='Release_Year', y='App_Id', hue='Primary_Genre', data=top_genre_per_year, dodge=False, palette='tab10')
plt.title('Most Uploaded Genre for Each Year', fontsize=14, fontweight='bold')
plt.suptitle(wrap_text("This chart shows the dominant genre for each year in terms of app uploads. It highlights shifting trends in app development focus, such as the rise of Games or other genres over time."), fontsize=10, y=0.95, color='gray')
plt.xlabel('Year')
plt.ylabel('Number of Apps')
plt.legend(title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Exclude "Games" from the dataset
non_games_data = dataset[dataset['Primary_Genre'] != 'Games']

# Group data by year and genre to count the number of apps
year_non_game_genre_counts = non_games_data.groupby(['Release_Year', 'Primary_Genre'])['App_Id'].count().reset_index()

# For each year, find the non-game genre with the maximum uploads
top_non_game_genre_per_year = year_non_game_genre_counts.loc[year_non_game_genre_counts.groupby('Release_Year')['App_Id'].idxmax()]

# Visualization: Most Uploaded Non-Game Genre Each Year
plt.figure(figsize=(12, 6))
sns.barplot(x='Release_Year', y='App_Id', hue='Primary_Genre', data=top_non_game_genre_per_year, dodge=False, palette='tab10')
plt.title('Most Uploaded Non-Game Genre for Each Year', fontsize=14, fontweight='bold')
plt.suptitle(wrap_text("This chart shows the most uploaded non-game genre for each year, highlighting shifts in developer focus outside the dominant Games category."), fontsize=10, y=0.95, color='gray')
plt.xlabel('Year')
plt.ylabel('Number of Apps')
plt.legend(title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()


# Group by genre and calculate the percentage of paid apps
price_genre_analysis = dataset.groupby('Primary_Genre').agg(
    Total_Apps=('App_Id', 'count'),
    Paid_Apps=('Price', lambda x: (x > 0).sum())  # Count apps with Price > 0
).reset_index()
price_genre_analysis['Percentage_Paid'] = (price_genre_analysis['Paid_Apps'] / price_genre_analysis['Total_Apps']) * 100

# Sort by percentage of paid apps
price_genre_analysis = price_genre_analysis.sort_values(by='Percentage_Paid', ascending=False)

# Visualization: Price vs Genre
plt.figure(figsize=(12, 6))
sns.barplot(x='Percentage_Paid', y='Primary_Genre', data=price_genre_analysis, palette='mako')
plt.title('Percentage of Paid Apps by Genre', fontsize=14, fontweight='bold')
plt.suptitle(wrap_text("This chart shows the percentage of paid apps in each genre."), fontsize=10, y=0.95, color='gray')
plt.xlabel('Percentage of Paid Apps (%)')
plt.ylabel('Genre')
plt.show()

# Calculate estimated revenue for each app
dataset['Estimated_Revenue'] = dataset['Price'] * dataset['Reviews']

# Group by genre and sum the estimated revenue
top_earning_genres = dataset.groupby('Primary_Genre')['Estimated_Revenue'].sum().reset_index()
top_earning_genres = top_earning_genres.sort_values(by='Estimated_Revenue', ascending=False)

# Visualization: Top-Earning Genres
plt.figure(figsize=(12, 6))
sns.barplot(x='Estimated_Revenue', y='Primary_Genre', data=top_earning_genres.head(10), palette='crest')
plt.title('Top-Earning Genres (Estimated)', fontsize=14, fontweight='bold')
plt.suptitle(wrap_text("This chart estimates the top-earning genres by combining app prices and review counts. Revenue is approximated, assuming reviews are proportional to purchases."), fontsize=10, y=0.95, color='gray')
plt.xlabel('Estimated Revenue ($)')
plt.ylabel('Genre')
plt.show()


# Group by developer and count the number of apps
top_developers = dataset.groupby('Developer')['App_Id'].count().reset_index()
top_developers = top_developers.sort_values(by='App_Id', ascending=False).head(10)

# Visualization: Top Developers by Number of Apps
plt.figure(figsize=(12, 6))
sns.barplot(x='App_Id', y='Developer', data=top_developers, palette='viridis')
plt.title('Top Developers by Number of Apps', fontsize=14, fontweight='bold')
plt.suptitle(wrap_text("This chart shows the top 10 developers with the most apps on the App Store, highlighting their dominance in app releases."), fontsize=10, y=0.95, color='gray')
plt.xlabel('Number of Apps')
plt.ylabel('Developer')
plt.show()


# Calculate average ratings and total reviews for each developer
developer_performance = dataset.groupby('Developer').agg(
    Average_Rating=('Average_User_Rating', 'mean'),
    Total_Reviews=('Reviews', 'sum')
).reset_index()

# Top developers by ratings (with at least 5 apps for relevance)
top_rated_developers = dataset.groupby('Developer').filter(lambda x: len(x) >= 5)
top_rated_developers = developer_performance.sort_values(by='Average_Rating', ascending=False).head(10)

# Top developers by total reviews
top_reviewed_developers = developer_performance.sort_values(by='Total_Reviews', ascending=False).head(10)

# Visualization: Top-Rated Developers
plt.figure(figsize=(12, 6))
sns.barplot(x='Average_Rating', y='Developer', data=top_rated_developers, palette='mako')
plt.title('Top Developers by Average Rating (Min. 5 Apps)', fontsize=14, fontweight='bold')
plt.suptitle(wrap_text("This chart highlights developers with the highest-rated apps, showcasing user satisfaction with their offerings."), fontsize=10, y=0.95, color='gray')
plt.xlabel('Average User Rating')
plt.ylabel('Developer')
plt.show()

# Visualization: Top-Reviewed Developers
plt.figure(figsize=(12, 6))
sns.barplot(x='Total_Reviews', y='Developer', data=top_reviewed_developers, palette='rocket')
plt.title('Top Developers by Total Reviews', fontsize=14, fontweight='bold')
plt.suptitle(wrap_text("This chart shows developers whose apps have received the most reviews, indicating high user engagement and interaction."), fontsize=10, y=0.95, color='gray')
plt.xlabel('Total Reviews')
plt.ylabel('Developer')
plt.show()
