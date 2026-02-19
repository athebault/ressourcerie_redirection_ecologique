## utilitary functions for ressourcerie ##
import ast
import streamlit as st
import numpy as np

from email_validator import validate_email, EmailNotValidError

mutiselect_cols = ["Thème", "Catégorie", "Besoin", "Public"]
final_cols_order = [
    "Nom",
    "Catégorie",
    "Thème",
    "Niveau",
    "Type",
    "durée",
    "Public",
    "URL",
    "Besoin",
]

# Appliquer du CSS global pour agrandir le texte


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


# Fonction permettant de supprimer les lignes n'ayant pas de ressources
def remove_empty_lines(df):
    indices = np.where(df["Nom"].str.len() > 2)[0]
    clean_df = df.loc[indices, :]
    return clean_df


# Fonction pour transformer les chaînes de caractères en listes réelles
def parse_list(value):
    try:
        if isinstance(value, str):
            return ast.literal_eval(value)
        return value
    except (ValueError, SyntaxError):
        return []


# Fonction permettant d'extraire les options disponibles
def get_options(data, col):
    if col in mutiselect_cols:
        data[col] = data[col].apply(parse_list)
        options = set(value for sublist in data[col] for value in sublist)
    else:
        options = data[col].unique()
    return options


# Fonction pour filtrer les données selon les valeurs sélectionnées
def get_data_from_selection(data, col, selected_options):
    if not selected_options:
        return data  # Retourne toutes les données si aucune option n'est sélectionnée
    return data[
        data[col].apply(lambda x: all(option in x for option in selected_options))
    ]


# Fonction permettant de créer un filtre sur une colonne données, avec une question associée
def define_filter(data, col_name, question):
    # Afficher les options
    if col_name in mutiselect_cols:
        options = st.multiselect(question, get_options(data, col_name), default=[])
    else:
        options = st.pills(
            question, get_options(data, col_name), selection_mode="multi"
        )

    # Filtrer les données
    if options:
        filtered_data = get_data_from_selection(data, col_name, options)
    else:
        filtered_data = data

    return filtered_data


# Fonction pour styliser les tags
def render_tags(tags, bg_color="#0078D7", text_color="white"):
    """Affiche des tags sous forme de badges colorés."""
    if isinstance(tags, str):  # Vérifie si c'est une chaîne unique
        tags = [tags]
    tag_html = " ".join(
        f'<span style="background-color:{bg_color}; color:{text_color}; padding:4px 8px; '
        f'border-radius:8px; margin-right:4px; font-size:14px;">{tag}</span>'
        for tag in tags
    )
    return tag_html


# 🔹 Fonction pour afficher les ressources
def show_ressources(data):
    ressources = data["Nom"].tolist()
    urls = data["URL"].tolist()
    themes = data["Thème"].tolist()
    categories = data["Catégorie"].tolist()
    niveaux = data["Niveau"].tolist()
    publics = data["Public"].tolist()
    type = data["Type"].tolist()

    for nom, url, theme, categ, public, niveau, format in zip(
        ressources, urls, themes, categories, publics, niveaux, type
    ):
        st.subheader(nom)

        # Affichage des tags correctement (évite de passer toute la colonne au lieu de la valeur)
        if theme:
            st.markdown(
                f"*Thème : {render_tags(theme, bg_color='purple')}*",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(f"*Thème : Non défini*", unsafe_allow_html=True)
        st.markdown(
            f"*Catégorie : {render_tags(categ, bg_color='green')}*",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"*Public : {render_tags(public, bg_color='orange')}*",
            unsafe_allow_html=True,
        )
        st.markdown(f"*Niveau : {render_tags(niveau)}*", unsafe_allow_html=True)
        st.markdown(
            f"*Format : {render_tags(format, bg_color='yellow', text_color='grey')}*",
            unsafe_allow_html=True,
        )

        st.link_button(f"Ouvrir **{nom}**", url)
        st.divider()

    details = st.checkbox("Plus de détails ?")
    if details:
        st.dataframe(data[final_cols_order])


def check_mail(email):
    if not email:
        return
    try:
        # Validation de l'email
        v = validate_email(email)
        email = v["email"]
        st.write(
            f"Nous vous enverrons des nouvelles de l'évolution de la plateforme à l'adresse: {email}."
        )
    except EmailNotValidError as e:
        st.write("Adresse email non valide")
