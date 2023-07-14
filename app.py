# import main libraries
import streamlit as st
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# import custom packages
from categories import meta
from categories import structure
from categories import tech
from categories import accessibility
from categories import w3c_validation

from metrics import html5_structure
from metrics import technical
from metrics import meta_data
from metrics import images

from globals import tips

# import time library
import time

# streamlit page config
st.set_page_config(page_title="vispro - SEO-friendly Website Checker")

# add fontawesome and custom styles
st.markdown("<link rel='stylesheet' href='https://use.fontawesome.com/releases/v5.14.0/css/all.css' integrity='sha384-HzLeBuhoNPvSl5KYnjx0BT+WB0QEEqLprO+NBkkk5gbc67FTaL7XIGa2w1L0Xbgc' crossorigin='anonymous'>", unsafe_allow_html=True)
with open( "css/styles.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

# sidebar config
st.sidebar.markdown("<h1>vispro.</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p class='slogan'>SEO-friendly Website Checker</p>", unsafe_allow_html=True)
options = ['Übersicht', 'Technische Daten', 'Meta Daten', 'HTML5 Struktur', 'W3C Validierung', 'Barrierefreiheit']
selected_option = st.sidebar.selectbox('Kategorie auswählen:', options)

# print current category
st.header(selected_option)

# add url input
url = st.text_input("URL eingeben und Enter drücken:")
if url:
    col1, col2 = st.columns([2, 11])
    with col1:
        st.button("Neu laden")
    with col2:
        tips = st.sidebar.checkbox("Hinweise anzeigen")

# check if url is valid
if not url:
    st.markdown("<div class='no-url'><i class='fas fa-unlink'></i><p>Du hast noch keine URL eingegeben.</p></div>", unsafe_allow_html=True)
else:
    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        url = "http://" + url.strip()

    try:
        start_time = time.time()
        res = requests.get(url)
        end_time = time.time()
        load_time = end_time - start_time
        soup = BeautifulSoup(res.text, 'html.parser')
    except:
        st.write()

if url and selected_option == "Übersicht":
    try:
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        col1.metric("Antwortzeit", str(round(load_time, 2)) + " s")
        col2.metric("Status Code", res.status_code)
        col3.metric("Version", "HTTP/" +  str(res.raw.version / 10))
        col4.metric("Größe", technical.get_html_size(res))

        st.subheader("Titel der Seite")
        meta_data.analyze_title(url, res, tips)

        st.subheader("Kanonische URL")
        meta_data.analyze_canonical(url, res, tips)

        st.subheader("H1 Überschrift")
        html5_structure.check_h1_tag(url, res, soup, tips)

        st.subheader("Überschriften-Hierachie")
        html5_structure.check_headings_hierarchy(url, res, soup, tips)

        st.subheader("Bilder")
        images.check_image_alt_attributes(url, res, tips)

        st.subheader("W3C Validierung")
        html5_structure.w3c_validation(url)

        st.subheader("Links")
        technical.validate_links(url, tips)
    except:
        st.markdown("<div class='no-url'><i class='fas fa-bug'></i><p>Du hast eine fehlerhafte URL eingegeben.</p></div>", unsafe_allow_html=True)


if url and selected_option == "Technische Daten":
    try:
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        col1.metric("Status Code", res.status_code)
        col2.metric("JavaScript Dateien", technical.count_js_files(url, soup))
        col3.metric("CSS Dateien", technical.count_css_files(url, soup))
        col4.metric("Größe", technical.get_html_size(res))
        tech.render(url, res, soup, tips)
    except:
        st.markdown("<div class='no-url'><i class='fas fa-bug'></i><p>Du hast eine fehlerhafte URL eingegeben.</p></div>", unsafe_allow_html=True)

if url and selected_option == "Meta Daten":
    try:
        meta.render(url, res, tips)
    except:
        st.markdown("<div class='no-url'><i class='fas fa-bug'></i><p>Du hast eine fehlerhafte URL eingegeben.</p></div>", unsafe_allow_html=True)

if url and selected_option == "HTML5 Struktur":
    try:
        html5_structure.render(url, res, soup, tips)
    except:
        st.markdown("<div class='no-url'><i class='fas fa-bug'></i><p>Du hast eine fehlerhafte URL eingegeben.</p></div>", unsafe_allow_html=True)

if url and selected_option == "W3C Validierung":
    try:
        st.write("")
        w3c_validation.render(url)
    except:
        st.markdown("<div class='no-url'><i class='fas fa-bug'></i><p>Du hast eine fehlerhafte URL eingegeben.</p></div>", unsafe_allow_html=True)



if url and selected_option == "Barrierefreiheit":
    try:
        accessibility.render(url, res, soup, tips)
    except:
        st.markdown("<div class='no-url'><i class='fas fa-bug'></i><p>Du hast eine fehlerhafte URL eingegeben.</p></div>", unsafe_allow_html=True)
