from dotenv import load_dotenv

import os
import pandas as pd
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from notion2pandas import Notion2PandasClient
from utils import *

# Get uptodate database
load_dotenv()
n2p = Notion2PandasClient(auth=os.getenv("NOTION_KEY"))
df = n2p.from_notion_DB_to_dataframe(os.getenv("notion_database_id"))
df = remove_empty_lines(df)

# Streamlit Application
st.set_page_config(
    page_title="Ressourcerie de la redirection écologique",
    page_icon="img/redirect.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Define styles
local_css("style.css")
remote_css("https://fonts.googleapis.com/icon?family=Material+Icons")


def app():
    st.title("Bienvenue sur la ressourcerie de la redirection écologique 📚")

    with stylable_container(
        key="colored_container",
        css_styles="""
            {
                background-color: aliceblue;
                border: 1px solid rgba(49, 51, 63, 0.2);
                border-radius: 0.5rem;
                padding: calc(1em - 1px)
            }
            """,
    ):
        st.subheader(
            ":question: Pourquoi une ressourcerie de la redirection écologique?"
        )
        st.write(
            """
            La raison d'être de cette **ressourcerie** est lblblb
            """
        )

    st.sidebar.header("\U0001f50d Filtres")

    # Initialisation du dataframe filtré (vide au départ)
    filtered_data = df.copy()

    with st.container(border=True):
        with st.form("Filtres_format"):
            st.subheader("Format des ressources")
            filtered_data = define_filter(
                filtered_data, "Type", "## Avez-vous un ou des formats privilégiés"
            )
            filtered_data = define_filter(
                filtered_data,
                "durée",
                "## Combien de temps souhaitez-vous passer sur ces ressources",
            )
            submitted_format = st.form_submit_button("Afficher les ressources")

    with st.sidebar.form("Filtres"):
        # Appliquer les filtres
        filtered_data = define_filter(
            filtered_data, "Besoin", "## Quel est votre besoin ?"
        )
        filtered_data = define_filter(
            filtered_data, "Thème", "## Quelle thématique voulez-vous creuser ?"
        )
        filtered_data = define_filter(filtered_data, "Public", "Pour quel public?")
        submitted = st.form_submit_button("Afficher les ressources")

    # Vérifier si l'utilisateur a appliqué au moins un filtre
    if (submitted or submitted_format) and not filtered_data.empty:

        # Affichage des résultats seulement si des filtres sont appliqués
        with st.container():
            st.header("Ressources proposées")
            show_ressources(filtered_data)

            details = st.checkbox("Plus de détails ?")
            if details:
                st.dataframe(filtered_data[final_cols_order])

    elif submitted:
        with st.container():
            st.write(
                "### Aucune ressource ne correspond à votre recherche pour l'instant."
            )

    with st.container():
        st.write("Pour suivre l'évolution de cette plateforme, laissez-nous votre mail")
        email = st.text_input("Email")
        check_mail(email)

        st.header(f"Merci pour votre visite!")


if __name__ == "__main__":
    app()
