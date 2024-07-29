import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import uuid

# Initialize session state for storing data
def init_donnees_collaborateurs():
    #if 'donnees_collaborateurs' not in st.session_state:
    st.session_state.donnees_collaborateurs = []

# Function to capture KPI data
def saisir_kpi():
    # Capture inputs
    kpi = {
        "ID": str(uuid.uuid4()),  # Unique identifier for each entry
        "Période": st.date_input("Période", value=pd.Timestamp.now()),
        "Nom du Collaborateur": st.text_input("Nom du Collaborateur"),
        "Nom du dossier": st.text_input("Nom du dossier"),
        "Typologie de marché": st.selectbox("Typologie de marché", ["Technologie", "Services", "Industrie", "Finance", "Santé"]),
        "Montant": st.number_input("Montant", step=1000000),
        "État d'avancement": st.selectbox("État d'avancement", ["En cours", "Terminé"]),
        "Type de sollicitation": st.radio("Type de sollicitation", ["Entrante", "Sortante"]),
        "Nombre d'offres envoyées par l'agent": st.number_input("Nombre d'offres envoyées par l'agent", min_value=0),
        "Phasage du projet": st.selectbox("Phasage du projet", ["Phase de conception", "Phase de réalisation", "Phase de planification", "Phase de clôture"]),
        "Modalité de paiement": st.selectbox("Modalité de paiement", ["Premier payement", "Deuxième payement", "Troisième payement", "Autre"]),
        "Zone du projet": st.selectbox("Zone du projet", ["Afrique", "Asie", "Europe", "Amérique du Nord", "Amérique du Sud"])
    }
    return kpi

# Save data to Excel
def save_data_to_excel(df):
    file_path = "donnees_kpi.xlsx"
    if os.path.exists(file_path):
        existing_data = pd.read_excel(file_path)
        # Check for duplicates
        df = df[~df['ID'].isin(existing_data['ID'])]
        df_updated = pd.concat([existing_data, df], ignore_index=True)
    else:
        df_updated = df
    
    df_updated.to_excel(file_path, index=False)
    st.success("Les données ont été enregistrées avec succès.")

# Page to input collaborator data
def page_saisie_donnees_collaborateur():
    init_donnees_collaborateurs()
    st.title("Saisie des données de collaborateurs")
    kpi = saisir_kpi()
    st.session_state.donnees_collaborateurs.append(kpi)
    df=pd.read_excel("donnees_kpi.xlsx")
    df2 = pd.DataFrame(st.session_state.donnees_collaborateurs)
    df3=pd.concat((df,df2),axis=0)
    st.write("Données saisies:")
    st.write(df2)
    st.write(df)
    
    if st.button("Enregistrer les données"):
        save_data_to_excel(df3)

# Page to display dashboard
def page_tableau_de_bord():
    file_path = "donnees_kpi.xlsx"
    if not os.path.exists(file_path):
        st.error("Le fichier des graphiques est manquant.")
        return

    df = pd.read_excel(file_path)
    
    st.title("Tableau de Bord")
    st.write("Bienvenue sur votre tableau de bord. Explorez les différentes visualisations pour comprendre vos données.")
    
    # Summary of data
    st.header("Résumé des données")
    st.write(df.head())
    st.write(df.info())
    
    # Plots
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Nombre de projets par collaborateur")
        fig, ax = plt.subplots()
        sns.histplot(df['Nom du Collaborateur'].dropna(), bins=20, kde=True, ax=ax)
        ax.set_title('Nombre de projets par collaborateur')
        st.pyplot(fig)

    with col2:
        st.subheader("Répartition des Zones du projet")
        fig, ax = plt.subplots()
        df['Zone du projet'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
        ax.set_title("Répartition des Zones du projet")
        st.pyplot(fig)

    with col3:
        st.subheader("Répartition des collaborateurs par projet")
        fig, ax = plt.subplots()
        df['Nom du dossier'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax)
        ax.set_title('Répartition des collaborateurs par projet')
        st.pyplot(fig)

# Page to display homepage
def page_accueil():
    st.title("Page d'accueil")
    st.write("Bienvenue sur votre application KPI Risk Logics!")

# Main function to switch between pages
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choisir une page", ["Page d'accueil", "Saisie des données", "Tableau de bord"])
    
    if page == "Page d'accueil":
        page_accueil()
    elif page == "Saisie des données":
        page_saisie_donnees_collaborateur()
    elif page == "Tableau de bord":
        page_tableau_de_bord()

if __name__ == "__main__":
    main()