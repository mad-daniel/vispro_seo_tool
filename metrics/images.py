import requests
from bs4 import BeautifulSoup
import streamlit as st

from globals import message
from globals import tips

def check_image_alt_attributes(url, res, tips):
    try:
        soup = BeautifulSoup(res.content, "html.parser")
        images_with_missing_alt = []
        images = soup.find_all("img")
        for image in images:
            if not image.has_attr("alt"):
                images_with_missing_alt.append(image["src"])

        if len(images_with_missing_alt) == 0:
            message.success("Alle Bilder haben ein Alt-Attribut")
        elif len(images_with_missing_alt) == 1:
            message.error('Es wurde {} Bild ohne Alt Attribut gefunden'.format(len(images_with_missing_alt)))
            with st.expander('Alle gefundenen Bilder ohne Alt Attribut anzeigen'):
                for img in images_with_missing_alt:
                    st.write(img)
            if tips:
                message.tips("Rankingfaktor", "Alle Bilder auf einer Webseite sollten ein Alt-Attribut haben, um barrierefreien Zugang und eine bessere Indexierung durch Suchmaschinen zu gewährleisten.")
        else:
            message.error('Es wurden {} Bilder ohne Alt Attribut gefunden'.format(len(images_with_missing_alt)))
            with st.expander('Alle gefundenen Bilder ohne Alt Attribut anzeigen'):
                for img in images_with_missing_alt:
                    st.write(img)
            if tips:
                message.tips("Rankingfaktor", "Alle Bilder auf einer Webseite sollten ein Alt-Attribut haben, um barrierefreien Zugang und eine bessere Indexierung durch Suchmaschinen zu gewährleisten.")
       
    except:
        message.error("Ein Fehler ist aufgetreten")

def check_image_title_attributes(url, res, tips):
    try:
        soup = BeautifulSoup(res.content, "html.parser")
        images_with_missing_title = []
        images = soup.find_all("img")
        for image in images:
            if not image.has_attr("title"):
                images_with_missing_title.append(image["src"])

        if len(images_with_missing_title) == 0:
            message.success("Alle Bilder haben ein Title-Attribut")
        elif len(images_with_missing_title) == 1:
            message.warning('Es wurde {} Bild ohne Title Attribut gefunden'.format(len(images_with_missing_title)))
            with st.expander('Alle gefundenen Bilder ohne Title Attribut anzeigen'):
                st.write(images_with_missing_title)
            if tips:
                message.tips("Rankingfaktor", "Bilder sollten eventuell ein Title-Attribut haben, um weitere Informationen oder eine Beschreibung des Bildes bereitzustellen.")
        else:
            message.warning('Es wurden {} Bilder ohne Title Attribut gefunden'.format(len(images_with_missing_title)))
            with st.expander('Alle gefundenen Bilder ohne Title Attribut anzeigen'):
                st.write(images_with_missing_title)
            if tips:
                message.tips("Rankingfaktor", "Bilder sollten eventuell ein Title-Attribut haben, um weitere Informationen oder eine Beschreibung des Bildes bereitzustellen.")
    except:
        message.error("Ein Fehler ist aufgetreten.")
