from notion2pandas import Notion2PandasClient
import streamlit as st
import pandas as pd
from utils import *

# Set your database id here:
NOTION_KEY = "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"
notion_database_id = "1996d88c994e802ebaf5ead0c1f37e31"

n2p = Notion2PandasClient(auth=NOTION_KEY)
df = n2p.from_notion_DB_to_dataframe(notion_database_id)
df = remove_empty_lines(df)

# Streamlit Application
st.set_page_config(
    page_title="Ressourcerie de la redirection écologique", layout="wide"
)


# Filter function
def filter_data(data, filters):
    for column, value in filters.items():
        if value:
            data = data[data[column].str.contains(value, case=False)]
    return data


def app():
    st.title("Ressourcerie de la redirection écologique 📚")
    st.sidebar.header("Filtres")

    # st.dataframe(df)

    # Multiselect pour le besoin
    filtered_data = define_filter(df, "Besoin", "## Quel est votre besoin ?")

    # Multiselect pour le thème
    filtered_data = define_filter(
        filtered_data, "Thème", "## Quelle thématique voulez-vous creuser ?"
    )

    # Multiselect pour le format
    filtered_data = define_filter(
        filtered_data, "Type", "## Avez-vous un ou des formats privilegiés"
    )

    # Multiselect pour le temps
    filtered_data = define_filter(
        filtered_data,
        "durée",
        "## Combien de temps souhaitez-vous passer sur ces ressources",
    )

    # Multiselect pour le temps
    filtered_data = define_filter(filtered_data, "Public", "Pour quel public?")

    # Affichage des résultats
    with st.container():
        if len(filtered_data.index) == 0:
            st.write(
                "### Aucune ressource ne correspond à votre recherche pour l'instant"
            )
        else:
            st.header("Ressources proposées")
            show_ressources(filtered_data)
            details = st.checkbox(
                "Plus de détails ?",
            )
            if details:
                st.dataframe(filtered_data[final_cols_order])

    st.write("Pour suivre l'évolution de cette plateforme, laissez nous votre mail")
    email = st.text_input("Email")
    check_mail(email)

    st.header(f"Merci pour votre visite!")


if __name__ == "__main__":
    app()
