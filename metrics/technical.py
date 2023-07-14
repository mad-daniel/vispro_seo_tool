import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from globals import message
from globals import tips
import urllib.request
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor

def count_js_files(url, soup):
    js_files = []
    for script in soup.find_all("script"):
        src = script.get("src")
        if src:
            if re.search(r"\.js($|\?)", src) or re.search(r"\.min\.js($|\?)", src):
                js_files.append(src)
    return len(js_files)

def print_js_files(url, soup):
    js_files = []
    for script in soup.find_all("script"):
        src = script.get("src")
        if src:
            if re.search(r"\.js($|\?)", src) or re.search(r"\.min\.js($|\?)", src):
                js_files.append(url + src)

    if len(js_files) == 0:
        message.error("Es konnten keine Javascript Dateien gefunden werden")
    elif len(js_files) == 1:
        message.success('Es wurde {} Javascript Datei gefunden'.format(len(js_files)))
    else:
        message.success('Es wurden {} Javascript Dateien gefunden'.format(len(js_files)))

    with st.expander('Alle gefundenen Javascript Dateien anzeigen'):
        for js_file in js_files:
            st.write(js_file)


def count_css_files(url, soup):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    css_files = []
    for link in soup.find_all("link"):
        rel = link.get("rel")
        href = link.get("href")
        if rel and href and "stylesheet" in rel:
            if re.search(r"\.css($|\?)", href):
                css_files.append(url + href)
    return len(css_files)


def print_css_files(url, soup):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    css_files = []
    for link in soup.find_all("link"):
        rel = link.get("rel")
        href = link.get("href")
        if rel and href and "stylesheet" in rel:
            if re.search(r"\.css($|\?)", href):
                css_files.append(href)
    if len(css_files) == 0:
        message.error("Es konnten keine CSS Dateien gefunden werden")
    elif len(css_files) == 1:
        message.success('Es wurde {} CSS Datei gefunden'.format(len(css_files)))
    else:
        message.success('Es wurden {} CSS Dateien gefunden'.format(len(css_files)))

    with st.expander('Alle gefundenen CSS Dateien anzeigen'):
        for css_file in css_files:
            st.write(url + css_file)

def check_style_tags(url, soup, tips):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    style_tags = soup.find_all("style")

    if style_tags:
        message.warning("Es wurden {} Style-Tags gefunden".format(len(style_tags)))
        with st.expander('Alle gefundenen Style-Tags anzeigen'):
            st.write(style_tags)
        if tips:
            message.tips("Hinweis", "Style-Tags sollten in eine eigene CSS-Datei ausgelagert werden, um das HTML-Dokument schlanker zu machen und die Wartbarkeit des Codes zu verbessern.")
    else:
        message.success("Keine Style-Tags gefunden")

def get_html_size(res):
    if not res:
        return
    size = len(res.content)
    size_kb = size / 1024
    return "{:.2f} KB".format(size_kb)



def validate_url(url):
    # Prüfung auf Sonderzeichen und Umlaute
    if bool(re.search('[^a-zA-Z0-9:/._-]', url)):
        message.error("Die URL enthält ungültige Sonderzeichen oder Umlaute.")

    # Prüfung auf Zahlen
    if url.isnumeric():
        message.error("Die URL darf nicht nur aus Zahlen bestehen.")

    # Prüfung auf Länge
    if len(url) > 74:
        message.error("Die URL ist zu lang (max. 74 Zeichen erlaubt).")

    message.success("Die URL ist gültig.")

def get_status_code(url, res):
    try:
        response = requests.get(url)
        message.text(f"Status Code: {response.status_code}")
        if response.history:
            st.write("Weiterleitungen:")
            for r in response.history:
                message.text(f"{r.status_code}: {r.url}")
    except requests.exceptions.RequestException as e:
        message.errror("Error:", e)


def validate_links(url, tips):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a')

    bad_links = []

    with ThreadPoolExecutor(max_workers=250) as executor:
        futures = []

        for link in links:
            href = link.get('href')
            if href is not None:
                if href.startswith('mailto:') or href.startswith('fax:') or href.startswith('tel:'):
                    continue

                if not href.startswith('http') and not href.startswith('www'):
                    parsed_url = urlparse(href)
                    parsed_base_url = urlparse(url)

                    if parsed_url.path.startswith('/'):
                        href = urljoin(parsed_base_url.scheme + '://' + parsed_base_url.netloc, parsed_url.path)
                    else:
                        base_path = parsed_base_url.path.rsplit('/', 1)[0]
                        href = urljoin(parsed_base_url.scheme + '://' + parsed_base_url.netloc, base_path+'/'+parsed_url.path)

                futures.append(executor.submit(validate_link, href, url))

        for future in futures:
            result = future.result()
            if result is not None:
                bad_links.append(result)

    message.text(f"Insgesamt wurden <strong>{len(links)}</strong> Links gefunden")

    if len(bad_links) == 0:
        message.success("Keine defekten Links gefunden")
    elif len(bad_links) == 1:
        message.error(f"{len(bad_links)} Link ist nicht erreichbar")
        with st.expander('Defekten Link anzeigen'):
            for link in bad_links:
                st.write(link)
        if tips:
            message.tips("Rankingfaktor", "Alle Links auf einer Seite sollten erreichbar sein, um eine gute Benutzererfahrung und eine optimale Indexierung durch Suchmaschinen sicherzustellen. Das gilt auch für Klickpfade, die den Nutzern helfen, die Navigation auf der Website zu verstehen. Stelle sicher, dass alle Klickpfade funktionieren und auf die entsprechenden Seiten führen, um eine positive Nutzererfahrung zu gewährleisten.")
    else:
        message.error(f"{len(bad_links)} Links sind nicht erreichbar")
        with st.expander('Defekte Links anzeigen'):
            for link in bad_links:
                st.write(link)
        if tips:
            message.tips("Rankingfaktor", "Alle Links auf einer Seite sollten erreichbar sein, um eine gute Benutzererfahrung und eine optimale Indexierung durch Suchmaschinen sicherzustellen. Das gilt auch für Klickpfade, die den Nutzern helfen, die Navigation auf der Website zu verstehen. Stelle sicher, dass alle Klickpfade funktionieren und auf die entsprechenden Seiten führen, um eine positive Nutzererfahrung zu gewährleisten.")



def validate_links_2(url, tips):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.find_all('a')

    bad_links = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = []

        for link in links:
            href = link.get('href')
            if href is not None:
                if href.startswith('mailto:') or href.startswith('fax:') or href.startswith('tel:'):
                    continue

                if not href.startswith('http') and not href.startswith('www'):
                    parsed_url = urlparse(href)
                    parsed_base_url = urlparse(url)
                    if parsed_url.netloc == '' or parsed_url.netloc == parsed_base_url.netloc:
                        if 'localhost' in url or '127.0.0.1' in url:
                            href = urljoin(url, href.lstrip('/'))
                        else:
                            href = urljoin(url, href)

                futures.append(executor.submit(validate_link, href, url))

        for future in futures:
            result = future.result()
            if result is not None:
                bad_links.append(result)

    message.text(f"Insgesamt wurden <strong>{len(links)}</strong> Links gefunden")

    if len(bad_links) == 0:
        message.success("Keine defekten Links gefunden")
    elif len(bad_links) == 1:
        message.error(f"{len(bad_links)} Link ist nicht erreichbar")
        with st.expander('Defekten Link anzeigen'):
            for link in bad_links:
                st.write(link)
        if tips:
            message.tips("Rankingfaktor", "Alle Links auf einer Seite sollten erreichbar sein, um eine gute Benutzererfahrung und eine optimale Indexierung durch Suchmaschinen sicherzustellen. Das gilt auch für Klickpfade, die den Nutzern helfen, die Navigation auf der Website zu verstehen. Stelle sicher, dass alle Klickpfade funktionieren und auf die entsprechenden Seiten führen, um eine positive Nutzererfahrung zu gewährleisten.")
    else:
        message.error(f"{len(bad_links)} Links sind nicht erreichbar")
        with st.expander('Defekte Links anzeigen'):
            for link in bad_links:
                st.write(link)
        if tips:
            message.tips("Rankingfaktor", "Alle Links auf einer Seite sollten erreichbar sein, um eine gute Benutzererfahrung und eine optimale Indexierung durch Suchmaschinen sicherzustellen. Das gilt auch für Klickpfade, die den Nutzern helfen, die Navigation auf der Website zu verstehen. Stelle sicher, dass alle Klickpfade funktionieren und auf die entsprechenden Seiten führen, um eine positive Nutzererfahrung zu gewährleisten.")


def validate_link(href, url):
    if href == "javascript:void(0)":
        return None
    if href.startswith('https://twitter.com/'):
        return None
    parsed_url = urlparse(href)
    parsed_base_url = urlparse(url)
    if parsed_url.netloc == '' or parsed_url.netloc == parsed_base_url.netloc:
        try:
            response = requests.head(href)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            return href
    else:
        try:
            response = requests.head(href)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            return href
    return None


def check_links_title_attributes(url, res, tips):
    try:
        soup = BeautifulSoup(res.content, "html.parser")
        links_with_missing_title = []
        links = soup.find_all("a")
        for link in links:
            if not link.has_attr("title"):
                links_with_missing_title.append(link["href"])

        if len(links_with_missing_title) == 0:
            message.success("Alle Links haben ein Title-Attribut")
        elif len(links_with_missing_title) == 1:
            message.warning('Es wurde {} Link ohne Title-Attribut gefunden'.format(len(links_with_missing_title)))
            with st.expander('Alle gefundenen Links ohne Title-Attribut anzeigen'):
                st.write(links_with_missing_title)
            if tips:
                message.tips("Rankingfaktor", "Links sollten eventuell ein Title-Attribut haben, um zusätzliche Informationen über den verlinkten Inhalt bereitzustellen.")
        else:
            message.warning('Es wurden {} Links ohne Title-Attribut gefunden'.format(len(links_with_missing_title)))
            with st.expander('Alle gefundenen Links ohne Title-Attribut anzeigen'):
                st.write(links_with_missing_title)
            if tips:
                message.tips("Rankingfaktor", "Links sollten eventuell ein Title-Attribut haben, um zusätzliche Informationen über den verlinkten Inhalt bereitzustellen.")
    except:
        message.error("Ein Fehler ist aufgetreten.")

def render(url, res, soup, tips):
    options = ['Status Code', 'JS Dateien', 'CSS Dateien', 'Links']
    default_options = ['Status Code', 'JS Dateien', 'CSS Dateien', 'Links']
    st.sidebar.markdown('---')
    selected_options = st.sidebar.multiselect('Verfügbare Metriken:', options, default_options)

    if "Status Code" in selected_options:
        st.subheader("Status Code")
        get_status_code(url, res)

    if "JS Dateien" in selected_options:
        st.subheader("Javascript Dateien")
        print_js_files(url, soup)

    if "CSS Dateien" in selected_options:
        st.subheader("CSS Dateien")
        print_css_files(url, soup)
        
        st.subheader("Style Tags")
        check_style_tags(url, soup, tips)

    if "Links" in selected_options:
        st.subheader("Links")
        validate_links(url, tips)