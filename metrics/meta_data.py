import streamlit as st
import requests
from bs4 import BeautifulSoup
import io
from PIL import Image
import re

from globals import message
from globals import tips

def analyze_title(url, res, tips):
    soup = BeautifulSoup(res.content, "html.parser")
    title = soup.find("title").get_text()

    if title:
        message.text(title)
        if len(title) >= 60:
            message.error("Der Seitentitel ist zu lang")
            if tips:
                message.tips("Rankingfaktor", "Der Seitentitel sollte maximal 60 Zeichen lang sein, da längere Titel von Suchmaschinen möglicherweise umgeschrieben werden.")
        elif len(title) <= 30:
            message.error("Der Seitentitel ist zu kurz")
            if tips:
                message.tips("Rankingfaktor", "Der Seitentitel sollte mindestens 30 Zeichen lang sein, da kürzere Titel von Suchmaschinen möglicherweise umgeschrieben werden.")
        elif len(title) == 0:
            message.error("Der Seitentitel darf nicht leer sein")
            if tips:
                message.tips("Rankingfaktor", "Der Seitentitel darf insbesondere aus SEO-Gründen nicht leer sein. Er sollte etwa zwischen 30 und 60 Zeichen lang sein.")
        else:
            message.success("Der Seitentitel hat eine angemessene Länge")
    else:
        message.error("Kein Seitentitel gefunden")
        if tips:
            message.tips("Rankingfaktor", "In dem Dokument wurde kein oder ein leerer Seitentitel gefunden. Ein Seitentitel ist vor allem aus SEO-Gründen unverzichtbar und sollte etwa zwischen 30 und 60 Zeichen lang sein.")


def analyze_meta_description(url, res, tips):
    soup = BeautifulSoup(res.content, "html.parser")
    meta_description = soup.find("meta", attrs={"name":"description"})

    if meta_description:
        meta_description = meta_description["content"]
        message.text(meta_description)
        if len(meta_description) >= 150:
            message.warning("Die Meta-Beschreibung ist zu lang")
            if tips:
                message.tips("Hinweis", "Eine Meta-Beschreibung sollte nicht zu lang sein und maximal 150 Zeichen enthalten, um sicherzustellen, dass sie vollständig in den Suchergebnissen angezeigt wird.")
        elif len(meta_description) <= 60:
            message.warning("Die Meta-Beschreibung ist zu kurz")
            if tips:
                message.tips("Hinweis", "Eine Meta-Beschreibung sollte nicht zu kurz sein und mindestens etwa 60 Zeichen enthalten, damit sie für Suchmaschinen und Benutzer aussagekräftig ist.")
        elif len(meta_description) == 0:
            message.warning("Die Meta-Beschreibung darf nicht leer sein")
            if tips:
                message.tips("Hinweis", "Eine leere Meta-Beschreibung bietet Suchmaschinen und Nutzern keine Vorschau auf den Inhalt einer Seite und kann die Klickrate in den Suchergebnissen negativ beeinflussen.")
        else:
            message.success("Die Meta-Beschreibung hat eine angemessene Länge")
    else:
        message.error("Keine Meta-Beschreibung gefunden")
        if tips:
            message.tips("Hinweis", "Eine Meta-Beschreibung sollte verwendet werden, um Suchmaschinen und Nutzern eine prägnante Zusammenfassung des Inhalts einer Seite zu bieten und die Wahrscheinlichkeit zu erhöhen, dass Nutzer auf den Suchergebnisseiten auf die Seite klicken.")

def analyze_og_title(url, res, tips):
    soup = BeautifulSoup(res.content, "html.parser")
    og_title = soup.find("meta", property="og:title")

    if og_title:
        og_title = og_title["content"]
        message.text(og_title)
        if len(og_title) >= 60:
            message.warning("Der Open Graph Titel ist zu lang")
            if tips:
                message.tips("Hinweis", "Ein OG-Titel sollte idealerweise nicht länger als 60 Zeichen sein, um sicherzustellen, dass er vollständig in den Suchergebnissen oder auf Social Media-Plattformen angezeigt wird und Nutzer einen klaren Überblick über den geteilten Inhalt erhalten.")
        elif len(og_title) == 0:
            message.warning("Der Open Graph Titel darf nicht leer sein")
            if tips:
                message.tips("Hinweis", "Ein leerer OG-Titel führt zu einer fehlenden oder unklaren Überschrift für den geteilten Inhalt, was das Interesse der Nutzer mindert und zu einem geringeren Klickpotenzial führt.")
        else:
            message.success("Der Open Graph Titel hat eine angemessene Länge")
    else:
        message.error("Kein Open Graph Titel gefunden")
        if tips:
            message.tips("Hinweis", "Ein OG-Titel sollte verwendet werden, um Suchmaschinen und soziale Medienplattformen eine aussagekräftige und ansprechende Überschrift für den geteilten Inhalt zu liefern und das Interesse der Nutzer zu wecken, um auf den geteilten Link zu klicken.")

def analyze_og_description(url, res, tips):
    try:
        soup = BeautifulSoup(res.content, "html.parser")
        og_description = soup.find("meta", property="og:description")

        if og_description:
            og_description = og_description["content"]
            message.text(og_description)
            if len(og_description) >= 200:
                message.warning("Die Open Graph Beschreibung ist zu lang")
                if tips:
                    message.tips("Hinweis", "Eine OG-Beschreibung sollte idealerweise nicht länger als 200 Zeichen sein, um sicherzustellen, dass sie vollständig in den Suchergebnissen oder auf Social Media-Plattformen angezeigt wird und Nutzer einen klaren Überblick über den geteilten Inhalt erhalten.")
            elif len(og_description) == 0:
                message.warning("Die Open Graph Beschreibung darf nicht leer sein")
                if tips:
                    message.tips("Hinweis", "Eine leere OG-Beschreibung bietet keine informative Zusammenfassung des geteilten Inhalts, was zu weniger Klicks führen kann. Eine aussagekräftige OG-Beschreibung steigert hingegen das Interesse der Nutzer und erhöht die Klickwahrscheinlichkeit.")
            else:
                message.success("Die Open Graph Beschreibung hat eine angemessene Länge")
        else:
            message.error("Keine Open Graph Beschreibung gefunden")
            if tips:
                message.tips("Hinweis", "Eine OG-Beschreibung sollte verwendet werden, um Suchmaschinen und sozialen Medien eine prägnante Zusammenfassung des geteilten Inhalts zu liefern und das Interesse der Nutzer zu wecken, um auf den geteilten Link zu klicken.")
    except:
        message.error("Ungültige URL oder Fehler beim Abrufen der Seite")

def analyze_og_image(url, res, tips):
    try:
        soup = BeautifulSoup(res.content, "html.parser")
        og_image = soup.find("meta", property="og:image")

        if og_image:
            og_image = og_image["content"]

            ext_end = og_image.rfind(".")
            if ext_end == -1:
                message.error("Ungültige URL oder Fehler beim Abrufen der Seite")
                return

            additional_ext_start = og_image.rfind(".", 0, ext_end)
            if additional_ext_start == -1:
                file_name = og_image[:ext_end]
                file_ext = og_image[ext_end:]
            else:
                file_name = og_image[:additional_ext_start]
                file_ext = og_image[additional_ext_start:ext_end] + og_image[ext_end:]

            message.success("Open Graph Image gefunden")
            with st.expander("Open Graph Image anzeigen:"):
                st.image(og_image, width=800)
        else:
            message.error("Kein Open Graph Image gefunden")
            if tips:
                message.tips("Hinweis", "Ein OG-Bild sollte verwendet werden, um Nutzern eine visuelle Vorschau des geteilten Inhalts zu geben und ihre Aufmerksamkeit zu erhöhen, was zu einem höheren Klickpotenzial führt.")
    except:
        message.error("Ungültige URL oder Fehler beim Abrufen der Seite")


def analyze_og_url(url, res, tips):
    try:
        soup = BeautifulSoup(res.content, "html.parser")
        og_url = soup.find("meta", property="og:url")

        if og_url:
            og_url = og_url["content"]
            message.text(og_url)
            message.success("Open Graph URL gefunden")
        else:
            message.error("Keine Open Graph URL gefunden")
            if tips:
                message.tips("Hinweis", "Eine OG-URL sollte verwendet werden, um Nutzern eine klare und vertrauenswürdige Ziel-URL des geteilten Inhalts zu präsentieren, was zu einer höheren Klickwahrscheinlichkeit führt.")
    except:
        message.error("Ungültige URL oder Fehler beim Abrufen der Seite")


def analyze_og_type(url, res, tips):
    try:
        soup = BeautifulSoup(res.content, "html.parser")
        og_type = soup.find("meta", property="og:type")

        if og_type:
            og_type = og_type["content"]
            message.text(og_type)
            if og_type == "website":
                message.success("OG-Type ist auf Website eingestellt")
            else:
                message.warning("OG-Type ist nicht auf Website eingestellt")
                if tips:
                    message.tips("Hinweis", "Der OG-Typ 'Website' sollte eingestellt werden, um Suchmaschinen und sozialen Medien mitzuteilen, dass der geteilte Link auf eine vollständige Website und nicht auf eine andere Art von Inhalt verweist. Dadurch wird die korrekte Interpretation des Links gewährleistet und die Nutzer erhalten eine klare Vorstellung davon, was sie erwartet, wenn sie darauf klicken.")
        else:
            message.error("Kein OG-Type gefunden")
            if tips:
                message.tips("Hinweis", "Der OG-Typ sollte verwendet werden, um Suchmaschinen und sozialen Medien mitzuteilen, um welche Art von Inhalt es sich bei dem geteilten Link handelt. Dadurch wird die korrekte Darstellung und Interpretation des Inhalts gewährleistet, was Nutzern dabei hilft, besser zu verstehen, was sie erwartet, wenn sie auf den Link klicken.")
    except:
        message.error("Ungültige URL oder Fehler beim Abrufen der Seite")


def analyze_og_locale(url, res, tips):
    try:
        soup = BeautifulSoup(res.content, "html.parser")
        og_locale = soup.find("meta", property="og:locale")

        if og_locale:
            og_locale = og_locale["content"]
            message.text(og_locale)
            if og_locale == "de" or og_locale == "de_DE":
                message.success("OG-Locale ist auf Deutsch eingestellt")
            else:
                message.warning("OG-Locale ist nicht auf Deutsch eingestellt")
                if tips:
                    message.tips("Hinweis", "Sprache nicht auf Deutsch eingestellt. Die Verwendung von 'og:locale' auf Deutsch signalisiert Suchmaschinen und sozialen Medien, dass der Inhalt in deutscher Sprache vorliegt, was zu einer besseren lokalen Anpassung und Sichtbarkeit für deutschsprachige Nutzer führt.")
        else:
            message.error("Kein OG-Locale gefunden")
            if tips:
                message.tips("Hinweis", "Der OG-Locale-Tag ist optional und kann verwendet werden, um Suchmaschinen und sozialen Medien die Sprache des Inhalts mitzuteilen.")
    except:
        message.error("Ungültige URL oder Fehler beim Abrufen der Seite")


def analyze_canonical(url, res, tips):
    try:
        soup = BeautifulSoup(res.content, "html.parser")
        canonical = soup.find("link", rel="canonical")

        if canonical:
            canonical = canonical["href"]
            if canonical:
                message.text(canonical)
                message.success("Canonical-Tag gefunden")
        else:
            message.error("Kein Canonical-Tag gefunden")
            if tips:
                message.tips("Rankingfaktor", "Jede Seite benötigt eine kanonische URL, um mögliche Probleme mit Duplicate Content zu vermeiden.")
    except:
        message.error("Ungültige URL oder Fehler beim Abrufen der Seite")


def analyze_meta_robots(url, res, tips):
    try:
        soup = BeautifulSoup(res.content, "html.parser")
        meta_robots = soup.find("meta", attrs={"name": "robots"})

        if meta_robots:
            meta_robots = meta_robots["content"]
            message.text(meta_robots)
            message.success("Meta-Robots gefunden")
        else:
            message.error("Keine Meta-Robots gefunden")
            if tips:
                message.tips("Rankingfaktor", "Meta-Robots-Tags ermöglichen die Steuerung des Crawling-Verhaltens von Suchmaschinen auf bestimmten Seiten, um die Sichtbarkeit und Effizienz der Indexierung zu optimieren.")
    except:
        message.error("Ungültige URL oder Fehler beim Abrufen der Seite")


def analyze_meta_author(url, res, tips):
    try:
        soup = BeautifulSoup(res.content, "html.parser")
        meta_author = soup.find("meta", attrs={"name": "author"})

        if meta_author:
            meta_author = meta_author["content"]
            message.text(meta_author)
            message.success("Meta-Author gefunden")
        else:
            message.error("Kein Meta-Author gefunden")
            if tips:
                message.tips("Hinweis", "Die Verwendung des Meta-Author-Tags ermöglicht es, den Autor einer Seite anzugeben.")
    except:
        message.error("Ungültige URL oder Fehler beim Abrufen der Seite")


def analyze_meta_viewport(url, res, tips):
    try:
        soup = BeautifulSoup(res.content, "html.parser")
        meta_viewport = soup.find("meta", attrs={"name": "viewport"})

        if meta_viewport:
            meta_viewport = meta_viewport["content"]
            message.text(meta_viewport)
            message.success("Meta-Viewport gefunden")
        else:
            message.error("Kein Meta-Viewport gefunden")
            if tips:
                message.tips("Hinweis", "Die Verwendung des Meta-Viewport-Tags ermöglicht es Website-Betreibern, die Darstellung der Seite auf mobilen Geräten zu kontrollieren und sicherzustellen, dass sie korrekt skaliert und lesbar ist. Dadurch wird die Benutzerfreundlichkeit verbessert und eine optimale Darstellung auf verschiedenen Bildschirmgrößen gewährleistet.")
    except:
        message.error("Ungültige URL oder Fehler beim Abrufen der Seite")


def analyze_favicon(url, res, tips):
    soup = BeautifulSoup(res.content, "html.parser")
    favicon = soup.find("link", rel="shortcut icon")
    if not favicon:
        favicon = soup.find("link", rel="icon")
        
    if favicon:
        favicon_url = favicon["href"]
        if not favicon_url.startswith("http"):
            favicon_url = url + favicon_url
        response = requests.get(favicon_url)
        if response.status_code == 200:
            img = Image.open(io.BytesIO(response.content))
            img_bytes = io.BytesIO()
            img.save(img_bytes, format=img.format)
            try:
                st.image(img_bytes.getvalue(), width=32)
            except Exception as e:
                message.error("Favicon konnte nicht geladen werden")
                return
            message.success("Favicon gefunden")
        else:
            message.error("Favicon konnte nicht geladen werden")
    else:
        message.error("Kein Favicon gefunden")
        if tips:
            message.tips("Hinweis", "Die Verwendung eines Favicons ermöglicht es Websites, ein kleines, erkennbares Symbol in der Browser-Tab-Leiste und den Lesezeichen anzuzeigen. Dadurch wird die Markenerkennung gestärkt, die Benutzererfahrung verbessert und die Wiedererkennbarkeit der Website erhöht.")

def display_website_link(url):
    st.markdown("[Webseite öffnen](" + url + ")", unsafe_allow_html=True)

def analyze_twitter_card_title(url, res, tips):
    soup = BeautifulSoup(res.text, "html.parser")
    twitter_card_title = soup.find("meta", attrs={"name": "twitter:title"})

    if twitter_card_title:
        twitter_card_title = twitter_card_title["content"]
        message.text(twitter_card_title)
        if len(twitter_card_title) >= 60:
            message.warning("Der Twitter Card Titel ist lang")
            if tips:
                message.tips("Hinweis", "Ein Twitter-Card-Titel sollte unter 60 Zeichen bleiben, um sicherzustellen, dass er vollständig angezeigt wird und Nutzer zum Klicken anregt.")
        elif len(twitter_card_title) == 0:
            message.warning("Der Twitter Card Titel darf nicht leer sein")
            if tips:
                message.tips("Hinweis", "Ein leerer Twitter-Card-Titel bietet keine Informationen und verringert das Interesse der Nutzer, den Link anzuklicken. Ein aussagekräftiger Titel erhöht hingegen die Klickwahrscheinlichkeit.")
        else:
            message.success("Der Twitter Card Titel hat eine angemessene Länge")
    else:
        message.error("Kein Twitter Card Titel gefunden")
        if tips:
            message.tips("Hinweis", "Ein Twitter-Card-Titel sollte verwendet werden, um das Interesse der Nutzer zu wecken und die Klickwahrscheinlichkeit zu erhöhen.")




def analyze_twitter_card_description(url, res, tips):
    soup = BeautifulSoup(res.text, "html.parser")
    twitter_card_description = soup.find("meta", attrs={"name": "twitter:description"})

    if twitter_card_description:
        twitter_card_description = twitter_card_description["content"]
        message.text(twitter_card_description)
        if len(twitter_card_description) >= 200:
            message.warning("Die Twitter Card Beschreibung ist zu lang")
            if tips:
                message.tips("Hinweis", "Eine Twitter-Card-Beschreibung sollte unter 200 Zeichen bleiben, um sicherzustellen, dass sie vollständig angezeigt wird und Nutzer einen schnellen Überblick über den Inhalt erhalten.")
        elif len(twitter_card_description) == 0:
            message.warning("Die Twitter Card Beschreibung darf nicht leer sein")
            if tips:
                message.tips("Hinweis", "Eine leere Twitter-Card-Beschreibung verringert das Interesse der Nutzer und die Wahrscheinlichkeit, dass sie den Link anklicken. Eine aussagekräftige Beschreibung hingegen erhöht die Klickrate.")
        else:
            message.success("Die Twitter Card Beschreibung hat eine angemessene Länge")
    else:
        message.error("Keine Twitter Card Beschreibung gefunden")
        if tips:
            message.tips("Hinweis", "Eine Twitter-Card-Beschreibung sollte verwendet werden, um den Nutzern eine Zusammenfassung des Inhalts zu geben und ihr Interesse zu wecken.")


def analyze_twitter_card_image(url, res, tips):
    soup = BeautifulSoup(res.text, "html.parser")
    twitter_card_image = soup.find("meta", attrs={"name": "twitter:image"})

    if twitter_card_image:
        twitter_card_image = twitter_card_image["content"]
        message.success("Twitter Card Image gefunden")
        with st.expander("Twitter Card Image anzeigen:"):
            st.image(twitter_card_image, width=800)
    else:
        message.error("Kein Twitter Card Image gefunden")
        if tips:
            message.tips("Hinweis", "Ein Twitter-Card-Bild sollte verwendet werden, um Nutzern eine visuelle Vorschau des geteilten Inhalts zu bieten und ihre Aufmerksamkeit zu steigern, was zu einer höheren Klickrate führen kann.")


def render(url, res, tips):
    options = ['Titel', 'Beschreibung', 'Autor', 'Robots', 'Viewport', 'Favicon', 'Kanonische URL', 'Open Graph', 'Twitter Card']
    default_options = ['Titel', 'Beschreibung', 'Autor', 'Robots', 'Viewport', 'Favicon', 'Kanonische URL']
    st.sidebar.markdown('---')
    selected_options = st.sidebar.multiselect('Verfügbare Metriken:', options, default_options)

    if "Titel" in selected_options:
        st.subheader("Titel der Seite")
        analyze_title(url, res, tips)

    if "Beschreibung" in selected_options:
        st.subheader("Meta Beschreibung")
        analyze_meta_description(url, res, tips)

    if "Autor" in selected_options:
        st.subheader("Meta Autor")
        analyze_meta_author(url, res, tips)    

    if "Robots" in selected_options:
        st.subheader("Meta Robots")
        analyze_meta_robots(url, res, tips)
    
    if "Viewport" in selected_options:
        st.subheader("Meta Viewport")
        analyze_meta_viewport(url, res, tips)
    
    if "Favicon" in selected_options:
        st.subheader("Favicon")
        analyze_favicon(url, res, tips)

    if "Kanonische URL" in selected_options:
        st.subheader("Kanonische URL")
        analyze_canonical(url, res, tips)

    if "Open Graph" in selected_options:
        st.subheader("Open Graph Titel")
        analyze_og_title(url, res, tips)
        st.subheader("Open Graph Beschreibung")
        analyze_og_description(url, res, tips)
        st.subheader("Open Graph Image")
        analyze_og_image(url, res, tips)
        st.subheader("Open Graph Link")
        analyze_og_url(url, res, tips)
        st.subheader("Open Graph Type")
        analyze_og_type(url, res, tips)
        st.subheader("Open Graph Locale")
        analyze_og_locale(url, res, tips)
    
    if "Twitter Card" in selected_options:
        st.subheader("Twitter Card Titel")
        analyze_twitter_card_title(url, res, tips)
        st.subheader("Twitter Card Beschreibung")
        analyze_twitter_card_description(url, res, tips)
        st.subheader("Twitter Card Image")
        analyze_twitter_card_image(url, res, tips)