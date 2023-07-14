import streamlit as st
from globals import message
from globals import tips
from metrics import html5_structure
from metrics import images
from metrics import technical

def render(url, res, soup, tips):
    options = ['Bilder', 'Überschriften', 'Links']
    default_options = ['Bilder', 'Überschriften', 'Links']
    st.sidebar.markdown('---')
    selected_options = st.sidebar.multiselect('Verfügbare Metriken:', options, default_options)

    if "Bilder" in selected_options:
        st.subheader("Bilder (Alt Attribut)")
        images.check_image_alt_attributes(url, res, tips)

        st.subheader("Bilder (Title Attribut)")
        images.check_image_title_attributes(url, res, tips)

    if "Überschriften" in selected_options:
        st.subheader("Überschriften-Hierachie")
        html5_structure.check_headings_hierarchy(url, res, soup, tips)

    if "Links" in selected_options:
        st.subheader("Links (Title Attribut)")
        technical.check_links_title_attributes(url, res, tips)