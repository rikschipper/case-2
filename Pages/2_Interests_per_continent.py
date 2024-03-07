import streamlit as st
import time
import numpy as np
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Continent interests")

st.markdown("# Interests per continent")
st.write(
    """Hierin zullen wij laten zien waar de meeste interesses liggen per continent in de vorm van absolute getallen en het percentage."""
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
abs_fig = px.bar(
    interests_merged_melted,
    x="Interest Category",
    y="Interest Count",
    color="Gender",
    animation_frame="Continent",
    range_y=[0, interests_merged_melted["Interest Count"].max()],  # Set y-axis range based on your data
    title="Interests by Continent",
    labels={"Interest Count": "Interest Count"},
    color_discrete_map={"Male": "blue", "Female": "purple"},  # Update color for men and women
    barmode="group"  # Place bars next to each other
)


# Bereken de som van elke rij om de totale waarden te krijgen
interests_merged["Total"] = interests_merged.drop(columns=["Continent", "Gender"]).sum(axis=1)

# Converteer absolute waarden naar percentages
interests_merged_percentage = interests_merged.iloc[:, :-3].div(interests_merged["Total"], axis=0) * 100

# Voeg de kolommen 'Continent' en 'Gender' toe aan de DataFrame
interests_merged_percentage["Continent"] = interests_merged["Continent"]
interests_merged_percentage["Gender"] = interests_merged["Gender"]

# Smelt de DataFrame om 'Interest Category' als variabele te hebben
interests_merged_melted = pd.melt(interests_merged_percentage, id_vars=["Continent", "Gender"], var_name="Interest Category", value_name="Interest Percentage")

# Maak een interactieve staafplot met een schuifregelaar
perc_fig = px.bar(
    interests_merged_melted,
    x="Interest Category",
    y="Interest Percentage",
    color="Gender",
    animation_frame="Continent",
    range_y=[0, 100],  # Stel y-as bereik in op 0-100 procent
    title="Interests by Continent",
    labels={"Interest Percentage": "Interest Percentage"},
    color_discrete_map={"Male": "blue", "Female": "purple"},  # Update kleur voor mannen en vrouwen
    barmode="group"  # Zet balken naast elkaar
)

# Streamlit checkboxes
selected_graph = st.radio('Select a graph', ('Grafiek met absolute waardes', 'Grafiek met percentages'))

# Display selected graphs
if selected_graph == "Grafiek met absolute waardes":
    st.plotly_chart(abs_fig)
if selected_graph == "Grafiek met percentages":
    st.plotly_chart(perc_fig)
        

