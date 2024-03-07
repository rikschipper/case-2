import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(page_title="Conclusie")

st.markdown("# Conclusie")
st.write(
    """Allereerst is er gekeken naar de verdeling van de leeftijdsgroepen en hieruit bleek dat alle groepen vrijwel met dezelfde aantallen zijn vertegenwoordigd. Vervolgens is er gekeken naar het aantal mensen per continent, waaruit bleek dat dit in verhouding is met het aantal inwoners per continent. Dit is positief voor de plots, omdat er geen groepen onder of over vertegenwoordigd zijn. 

Aan de hand van de barplots is er vervolgens gekeken naar de interesses per continent en hierbij lijkt het alsof er een aanzienlijk verschil is tussen de continenten. Echter zijn er in het eerste plot absolute waardes gebruikt en is dat dus niet zo. Wanneer er in de plot percentages worden gebruikt, kan er geconcludeerd worden dat per continent dezelfde interesses even populair zijn."""
)
