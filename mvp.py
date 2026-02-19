from dotenv import load_dotenv

import os
import pandas as pd
import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from notion2pandas import Notion2PandasClient
from utils import *

# Get acces to database
# Local
load_dotenv()
NOTION_KEY = os.getenv("NOTION_KEY")
notion_database_id = os.getenv("notion_database_id")

# Web
# NOTION_KEY = st.secrets["NOTION_KEY"]
# notion_database_id = st.secrets["notion_database_id"]

# Get uptodate database
n2p = Notion2PandasClient(auth=NOTION_KEY)
df = n2p.from_notion_DB_to_dataframe(notion_database_id)
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

    # Initialisation du dataframe filtré
    filtered_data_content = df.copy()
    filtered_data = df.copy()

    # Filtre du dataframe
    with st.sidebar.form("Filtres"):
        # Appliquer les filtres
        filtered_data_content = define_filter(
            filtered_data_content, "Besoin", "## Quel est votre besoin ?"
        )
        filtered_data_content = define_filter(
            filtered_data_content, "Thème", "## Quelle thématique voulez-vous creuser ?"
        )
        filtered_data_content = define_filter(
            filtered_data_content, "Catégorie", "## Un sujet plus précis encore ?"
        )
        filtered_data_content = define_filter(
            filtered_data_content, "Public", "Pour quel public?"
        )
        submitted = st.form_submit_button("Afficher les ressources")

    with st.form("Filtres_format"):
        st.subheader("""⬇️ Format des Ressources""")
        if submitted:
            filtered_data_content = define_filter(
                filtered_data_content,
                "Type",
                "## Avez-vous un ou des formats privilégiés",
            )
            filtered_data_content = define_filter(
                filtered_data_content,
                "durée",
                "## Combien de temps souhaitez-vous passer sur ces ressources",
            )
            selected_data = filtered_data_content
        else:
            filtered_data = define_filter(
                filtered_data, "Type", "## Avez-vous un ou des formats privilégiés"
            )
            filtered_data = define_filter(
                filtered_data,
                "durée",
                "## Combien de temps souhaitez-vous passer sur ces ressources",
            )
            selected_data = filtered_data

        submitted_format = st.form_submit_button("Afficher les ressources")

    # Vérifier si l'utilisateur a appliqué au moins un filtre
    with st.container():
        st.header("Ressources proposées")

        if submitted and not submitted_format:
            show_ressources(filtered_data_content)

        else:
            # Affichage des résultats seulement si des filtres sont appliqués
            show_ressources(selected_data)

    with st.container():
        st.write("Pour suivre l'évolution de cette plateforme, laissez-nous votre mail")
        email = st.text_input("Email")
        check_mail(email)

        st.header(f"Merci pour votre visite!")


if __name__ == "__main__":
    app()
