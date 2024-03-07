import streamlit as st

Homepage.py # This is the file you run with "streamlit run"
└─── pages/
  └─── 1_Age_group.py.py # This is a page
  └─── 2_INterests_per_continent.py # This is another page
  └─── 3_Conclusie.py # So is this


st.set_page_config(page_title="Case 2 groep 5")

st.write("# Social media interesses over de wereld")



st.markdown(
    """
    Welkom op de site van groep 5 over de verschillende interesses van mensen wereldwijd op social media. In dit dashboard kan je met interactieve grafieken meer inzicht krijgen in de verschillende interesses over de wereld op social media.
"""
)

st.image('https://static.vecteezy.com/ti/gratis-vector/p3/4695784-social-media-verbinding-concept-wireframe-bol-gemaakt-van-een-andere-social-media-en-computer-iconen-wereldkaart-punt-en-lijn-compositie-aarde-bol-in-wireframe-hand-illustratie-vector.jpg', use_column_width=True)


st.markdown(
    """
    ### Instructie voor gebruik: 
"""
)

st.write(
            "•	De inhoudsopgave aan de linker kant kan gebruikt worden om naar de verschillende visualisaties te gaan."
    )
st.write(
       
    "•	Pas het plot met de slider aan om patronen te ontdekken in de data."
    )


    
    
st.markdown(
    """
    De gebruikte datasets zijn verkregen van Kaggle via een API. We hebben gebruik gemaakt van de Kaggle API. Hiervoor hebben we gebruik gemaakt van de twee library’s, os en opendatasets. De code die we gebruikt hebben ziet er als volgt uit:
    
#De URL van de Kaggle-dataset toewijzen aan de variabele

dataset1 = 'https://www.kaggle.com/datasets/arindamsahoo/social-media-users'

#Downloaden van dataset

od.download(dataset1)

#De URL van de Kaggle-dataset toewijzen aan de variabele

dataset2 = 'https://www.kaggle.com/datasets/hserdaraltan/countries-by-continent'

#Downloaden van dataset

od.download(dataset1)

Na het runnen van deze code moet er een gebruikersnaam en key opgegeven worden. De key is uniek voor elke Kaggle gebruiker en kan gevonden worden in een te downloaden json bestand.
"""
)

st.markdown(
    """De eerste dataset informatie over gebruikers op sociale media. Het bevat velden zoals UserID, Naam, Geslacht, Geboortedatum (DOB), Interesses, Stad en Land.
    """
)

st.markdown(
    """De tweede dataset die we gebruikt hebben is een dataset over alle landen en in welk continent ze liggen. In de dataset staan 196 landen, eerste kolom is de lijst met landen, de tweede kolom zijn de continenten van deze landen
    """
)

st.markdown(
    """Dit dashboard is gemaakt door Igor Baars, Jarno Bosman, Rik Schipper en Chaunce Yuen.
    """
)

