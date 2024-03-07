import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Age Groups")

st.markdown("# Ages in total & per continent ")
st.write(
    """In dit hoofdstuk zullen wij de verschillende leeftijden laten zien die zijn ondervraagd per continent en op de wereld.
    """
)

df = pd.read_csv("SocialMediaUsersDataset.csv")

#
list_0 = []
for a in df.Interests:
    if ',' in a:
        list_0 += set(eval(a))
    else:
        list_0 += [eval(a)]
        
inter_count = pd.Series(list_0).value_counts()


#import het dataframe voor de continenten
countries_continent_df = pd.read_csv('CountriesByContinent.csv')

# Merge the two datasets based on the "country" column
merged_df = pd.merge(df, countries_continent_df, on='Country', how='inner')

interests = merged_df['Interests'].str.get_dummies(', ')  # One-hot encode interests
interests.fillna(0, inplace=True)  # Replace NaN values with 0
interests.insert(0, 'UserID', merged_df['UserID'])
interests.insert(1, 'Gender', merged_df['Gender'])
interests.insert(2, "Country", merged_df["Country"])
interests.insert(3, "Continent", merged_df["Continent"])

countries_continents = interests.groupby(['Continent', 'Country', 'Gender']).sum()
countries_continents.drop("UserID", axis=1, inplace=True)

continents_sum = countries_continents.groupby(["Continent", "Gender"]).sum()

continents_sum.columns = [col[1:-1] for col in continents_sum.columns]


#Toevoegen van de nieuwe gecomprimeerde interests
# Arts and Culture
interests_merged = pd.DataFrame({})
interests_merged["Arts and Culture"] = continents_sum["Art"] + continents_sum["Beauty"] + \
                                       continents_sum["Books"] + continents_sum["Fashion"] + \
                                       continents_sum["Photography"]
# Lifestyle and Hobbies
interests_merged["Lifestyle and Hobbies"] = continents_sum["Cars and automobiles"] + continents_sum["Cooking"] + \
                                            continents_sum["DIY and crafts"]  + \
                                            continents_sum["Food and dining"] + continents_sum["Gaming"] + \
                                            continents_sum["Gardening"] + continents_sum["Outdoor activities"] + \
                                            continents_sum["Pets"]
# Knowledge and Learning
interests_merged["Knowledge and Learning"] = continents_sum["Education and learning"]+continents_sum["History"] + continents_sum["Science"] + continents_sum["Technology"]

# Entertainment and Media
interests_merged["Entertainment and Media"] = continents_sum["Movies"] + continents_sum["Music"] + \
                                              continents_sum["Gaming"]

# Society and Lifestyle
interests_merged["Society and Lifestyle"] = continents_sum["Business and entrepreneurship"] + \
                                             continents_sum["Finance and investments"] + \
                                             continents_sum["Health and wellness"] + \
                                             continents_sum["Parenting and family"] + \
                                             continents_sum["Politics"] + \
                                             continents_sum["Social causes and activism"] + \
                                             continents_sum["Sports"] + \
                                             continents_sum["Travel"] + \
                                             continents_sum["Fitness"]


# Create a new DataFrame for the interests_merged
interests_merged = pd.DataFrame({
    "Arts and Culture": continents_sum["Art"] + continents_sum["Beauty"] + continents_sum["Books"] + continents_sum["Fashion"] + continents_sum["Photography"],
    "Lifestyle and Hobbies": continents_sum["Cars and automobiles"] + continents_sum["Cooking"] + continents_sum["DIY and crafts"] + continents_sum["Food and dining"] + continents_sum["Gaming"] + continents_sum["Gardening"] + continents_sum["Outdoor activities"] + continents_sum["Pets"],
    "Knowledge and Learning": continents_sum["Education and learning"] + continents_sum["History"] + continents_sum["Science"] + continents_sum["Technology"],
    "Entertainment and Media": continents_sum["Movies"] + continents_sum["Music"] + continents_sum["Gaming"],
    "Society and Lifestyle": continents_sum["Business and entrepreneurship"] + continents_sum["Finance and investments"] + continents_sum["Health and wellness"] + continents_sum["Parenting and family"] + continents_sum["Politics"] + continents_sum["Social causes and activism"] + continents_sum["Sports"] + continents_sum["Travel"] + continents_sum["Fitness"],
    "Continent": continents_sum.index.get_level_values("Continent"),
    "Gender": continents_sum.index.get_level_values("Gender")
})

# Melt the DataFrame to have 'Interest Category' as a variable
interests_merged_melted = pd.melt(interests_merged, id_vars=["Continent", "Gender"], var_name="Interest Category", value_name="Interest Count")

# Create an interactive bar plot with a slider
slider_fig = px.bar(
    interests_merged_melted,
    x="Interest Category",
    y="Interest Count",
    color="Gender",
    animation_frame="Continent",
    range_y=[0, interests_merged_melted["Interest Count"].max()],  # Set y-axis range based on your data
    title="Interests by Continent",
    labels={"Interest Count": "Interest Count"},
    color_discrete_map={"Male": "blue", "Female": "pink"},  # Update color for men and women
    barmode="group"  # Place bars next to each other
)

# Show the plot
#slider_fig.show()

#Defining age
df["DOB"] = pd.to_datetime(df["DOB"])
df["Age"] = (pd.to_datetime("today") - df["DOB"]).astype('<m8[Y]')

#Defining age groups
bins= [0, 2, 16, 30, 45, 65, 110]
labels = ["Babies (0-2)", "Children (3-16)", "Young Adults (17-30)", "Middle-aged Adults (31-45)", "Old Adults (46-65)","Seniors (66+)"]
df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
#df.head()

merged_df = pd.merge(df, countries_continent_df, on='Country', how='inner')

a_df = []
b_df = []

unique_values, counts = np.unique(df["Age"], return_counts=True)
for value, count in zip(unique_values, counts):
    a_df.append(int(value))  # Converted value to int to remove decimals
    b_df.append(count)
data = pd.DataFrame({'Ages': a_df, 'Counts': b_df})  

plt.figure(figsize=(14, 10))
plt.xticks(rotation=65, fontsize=14)
age_total = sns.barplot(data=data, x="Ages", y="Counts", color="LightBlue")
#plt.show()
plt.close()

# Filter 'merged_df' to include only rows where 'Age' is an even number
even_ages_df = merged_df[merged_df['Age'] % 4 == 0]

# Group by 'Continent' and 'Age', then count the occurrences
grouped_data_even_ages = even_ages_df.groupby(['Continent', 'Age']).size().reset_index(name='Counts')

# Convert 'Age' to integer to avoid decimals in xticks
grouped_data_even_ages['Age'] = grouped_data_even_ages['Age'].astype(int)

# Plot
sns.set_context("poster")
plt.figure(figsize=(14, 10))

age_continent = sns.barplot(data=grouped_data_even_ages, x='Age', y='Counts', hue='Continent', width=1)

plt.xticks(rotation=65, fontsize=16)
#plt.show()
plt.close()

# Showing the graphs in streamlit 
with st.expander("Selecteer het gewenste grafiek", expanded=False):
    option = st.selectbox('', ('Totaal aantal leeftijden', 'Totaal aantal leeftijden per continent'))

# Conditional statements to display the selected graph
    if option == 'Totaal aantal leeftijden':
        st.pyplot(age_total.get_figure())
    elif option == 'Totaal aantal leeftijden per continent':
        st.pyplot(age_continent.get_figure())

