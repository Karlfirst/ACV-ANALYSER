#lien:http://localhost:8501/ https://acv-analyser-kqvnlvww7ex3sgzjpaha2c.streamlit.app/

#chargement les libraires
import streamlit as st
import pandas as pd
import numpy as np
#cd c:\Users\APC
#python tp2.py
#streamlit run tp2.py

st.write("Hello,world! This is a Streamlit app.")
print('Hello Streamlit')

st.title("Analyse des data de heart attack")
st.subheader("Bienvenue dans l'application interactive !")
st.text("Téléchargez un fichier CSV et explorez les données facilement.")
graph_type = st.selectbox("Choissisez un type de graphique:",["Ligne","Barres","Aucun"])

# Demande du nom de l'utilisateur
user_name = st.text_input("👤 Entrez votre prénom :")
if user_name:
    st.success(f"Bonjour {user_name}  Bienvenue dans l'application !")

# Chargement les données
uploaded_file = st.file_uploader(" Téléchargez un fichier CSV", type=["csv"])
# Dispaly panda dataframe
import pandas as pd
df = pd.read_csv(uploaded_file)
st.write("Voici un aperçu de votre fichier :")
st.dataframe(df.head())
#Affichage du graphique en fonction du type choisi
df_numeric = df.select_dtypes(include='number')
if graph_type == "Ligne":
    st.line_chart(df_numeric)
elif graph_type == "Barres":
    st.bar_chart(df_numeric)
else:
    st.write("Aucun graphique sélectionné.")
st.write("Merci d'avoir utilisé notre application Streamlit !")

df_numeric = df.select_dtypes(include='number')
columns = df_numeric.columns.tolist()

if len(columns) >= 2:
    x_col = st.selectbox("Choisissez une variable pour l'axe X", options=columns, index=0)
    y_col = st.selectbox("Choisissez une variable pour l'axe Y", options=columns, index=1)

    import plotly.express as px
    fig = px.scatter(df_numeric, x=x_col, y=y_col)
    st.plotly_chart(fig)
else:
    st.warning("Pas assez de colonnes numériques pour générer un graphique.")
# STEP 6 + STEP 7 : Analyse des corrélations (numériques + catégorielles)
st.title("STEP 7 : Corrélations avec Troponin")

if "Troponin" in df.columns:
  
    features_input_col = df.select_dtypes(include=np.number).columns.tolist()
    df_features_in = pd.DataFrame(df, columns=features_input_col)

    st.subheader(" 6 Corrélations numériques (Pearson)")
    st.markdown(" Analyse des colonnes numériques avec Troponin")

    st.markdown("** Features positively correlated with Troponin:**")
    st.write(df_features_in.corrwith(df["Troponin"], numeric_only=True).sort_values(ascending=False).head(5))

    st.markdown("* Features negatively correlated with Troponin:**")
    st.write(df_features_in.corrwith(df["Troponin"], numeric_only=True).sort_values(ascending=True).head(5))

    # STEP 7 - Categorical (One-hot encoded) correlation
    st.subheader("7 Corrélations catégorielles (via One-hot encoding)")
    st.markdown("Transformation des variables catégorielles en dummies pour corrélation")

    df_dummies = pd.get_dummies(df)  # one-hot encoding sur
    st.dataframe(df_dummies.head(10))

    st.markdown(" Features positively correlated with high Troponin:")
    st.write(df_dummies.corrwith(df["Troponin"]).sort_values(ascending=False).head(5))

    st.markdown(" Features negatively correlated with low Troponin:**")
    st.write(df_dummies.corrwith(df["Troponin"]).sort_values(ascending=True).head(5))
else:
    st.warning(" La colonne 'Troponin' n'existe pas dans le fichier.")
