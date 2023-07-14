import streamlit as st
import requests
from bs4 import BeautifulSoup
from globals import message
from globals import tips

def check_html_tag(url, res, soup, tips):
    html_tags = soup.find_all('html')
    if len(html_tags) == 0:
        message.error(f'Es wurde kein <code>HTML</code> Tag gefunden')
        if tips:
            message.tips("Hinweis", "Der <html>-Tag ist das grundlegende Strukturelement eines HTML-Dokuments und definiert den Beginn des Dokuments. Ohne diesen Tag würde das Dokument nicht als gültiges HTML-Dokument erkannt und könnte Probleme beim Rendern in einem Webbrowser verursachen.")
    elif len(html_tags) > 1:
        message.error(f'Es wurde mehr als ein <code>HTML</code> Tag gefunden')
        if tips:
            message.tips("Hinweis", "Im Dokument wurde ein verirrtes HTML-Tag gefunden. Da dieses Tag den Beginn des gesamten HTML-Dokuments definiert, sollte es nur einmal vorkommen.")
    else:
        message.success(f'Es wurde genau ein <code>HTML</code> Tag gefunden')

def check_head_tag(url, res, soup, tips):
    head_tags = soup.find_all('head')
    if len(head_tags) == 0:
        message.error(f'Es wurde kein <code>Head</code> Tag gefunden')
        if tips:
            message.tips("Hinweis", "Man darf nur ein Head-Tag pro HTML-Dokument verwenden, weil die Informationen, die dort definiert werden, nur einmal pro Seite benötigt werden sollen. Wenn man mehrere Head-Tags verwendet, kann das zu Problemen führen, da der Browser die Seite dann möglicherweise falsch darstellt und Suchmaschinen die Meta-Informationen nicht korrekt interpretieren und indexieren können.")
    elif len(head_tags) > 1:
        message.error(f'Es wurde mehr als ein <code>Head</code> Tag gefunden')
        if tips:
            message.tips("Hinweis", "Laut HTML-Spezifikation darf es nur ein Head-Tag in einem HTML-Dokument geben. Das liegt daran, dass das Head-Tag für bestimmte Informationen und Ressourcen vorgesehen ist, die nur einmal pro Seite benötigt werden, wie z.B. den Titel der Seite oder Verweise auf CSS-Dateien und Skripte.")
    else:
        message.success(f'Es wurde genau ein <code>Head</code> Tag gefunden')

def check_body_tag(url, res, soup, tips):
    body_tags = soup.find_all('body')
    if len(body_tags) == 0:
        message.error(f'Es wurde kein <code>Body</code> Tag gefunden')
        if tips:
            message.tips("Hinweis", "Der Body-Tag definiert den sichtbaren Inhalt einer Webseite und ist ein wichtiger Bestandteil des HTML-Markups, um eine funktionierende und ansprechende Webseite zu erstellen. Ohne ihn könnte der Browser die Seite nicht korrekt darstellen.")
    elif len(body_tags) > 1:
        message.error(f'Es wurde mehr als ein <code>Body</code> Tag gefunden')
        if tips:
            message.tips("Hinweis", "Der Body-Tag sollte nur einmal pro HTML-Dokument verwendet werden, um sicherzustellen, dass der Hauptinhalt der Seite korrekt dargestellt wird und dass das Markup des Dokuments gültig ist.")
    else:
        message.success(f'Es wurde genau ein <code>Body</code> Tag gefunden')

def check_main_tag(url, res, soup, tips):
    main_tags = soup.find_all('main')
    if len(main_tags) == 0:
        message.error(f'Es wurde kein <code>Main</code> Tag gefunden')
        if tips:
            message.tips("Hinweis", "Die Verwendung des <main>-Tags ist wichtig, um den Hauptinhalt einer Webseite zu kennzeichnen. Dies hilft Suchmaschinen und anderen technischen Systemen, den zentralen Inhalt einer Seite zu erkennen und besser zu verstehen. Dadurch wird die Barrierefreiheit verbessert, die Seitenstruktur klarer und die SEO-Relevanz des Hauptinhalts gesteigert.")
    elif len(main_tags) > 1:
        message.error(f'Es wurde mehr als ein <code>Main</code> Tag gefunden')
        if tips:
            message.tips("Hinweis", "In einem HTML-Dokument sollte nur ein Main-Tag verwendet werden, da er den Hauptinhalt der Webseite definiert und die Verwendung mehrerer solcher Tags zu Inkompatibilitäten und Validierungsfehlern führen kann.")
    else:
        message.success(f'Es wurde genau ein <code>Main</code> Tag gefunden')

def check_header_tag(url, res, soup, tips):
    header_tags = soup.find_all('header')
    if len(header_tags) == 0:
        message.error(f'Es wurde kein <code>Header</code> Tag gefunden')
        if tips:
            message.tips("Hinweis", "Das Verwenden von Header-Tags in HTML kann aus SEO-Gründen hilfreich sein, da sie dazu beitragen können, die semantische Struktur einer Website zu verbessern und den Inhalt der Website für Suchmaschinen besser zugänglich zu machen.")
    elif len(header_tags) > 1:
        message.error(f'Es wurde mehr als ein <code>Header</code> Tag gefunden')
        if tips:
            message.tips("Hinweis", "Es wird empfohlen, nur ein Header-Tag pro Seite zu verwenden und sicherzustellen, dass der Inhalt innerhalb des Tags den Hauptkontext der Seite gut widerspiegelt. Dadurch wird sichergestellt, dass Suchmaschinen den Inhalt der Seite besser verstehen und die SEO-Performance verbessert wird.")
    else:
        message.success(f'Es wurde genau ein <code>Header</code> Tag gefunden')

def check_footer(url, res, soup, tips):
    footers = soup.find_all('footer')
    if len(footers) == 0:
        message.error('Es wurde kein <code>Footer</code> Tag gefunden')
        if tips:
            message.tips("Hinweis", "Der Footer-Tag ist wichtig, da er den Abschluss einer Webseite definiert und es ermöglicht, zusätzliche Informationen und Links am Ende der Seite hinzuzufügen, wie z.B. das Urheberrecht, Kontaktinformationen oder Verweise auf verwandte Seiten.")
    elif len(footers) > 1:
        message.error(f'Es wurde mehr als ein <code>Footer</code> Tag gefunden')
        if tips:
            message.tips("Hinweis", "Man sollte in einem HTML-Dokument nicht mehr als einen Footer-Tag verwenden, da dieser nur den Abschluss der Seite definiert und die Verwendung mehrerer Footer-Tags zu Validierungsfehlern und inkonsistentem Verhalten führen kann.")
    else:
        message.success(f'Es wurde genau ein <code>Footer</code> Tag gefunden')

def check_nav_tag(url, res, soup):
    nav_tags = soup.find_all('nav')
    if len(nav_tags) == 0:
        message.error(f'Es wurde kein <code>Nav</code> Tag gefunden')
    elif len(nav_tags) > 1:
        message.warning(f'Es wurden mehrere <code>Nav</code> Tags gefunden')
        with st.expander('Alle gefundenen <nav>-Tags anzeigen'):
            st.write(nav_tags)
    else:
        message.success(f'Es wurde genau ein <code>Nav</code> Tag wurde gefunden')
        with st.expander('Alle gefundenen <nav>-Tags anzeigen'):
            st.write(nav_tags)

def check_section_tag(url, res, soup, tips):
    sections = soup.find_all('section')
    if len(sections)>0:
        message.success('Es wurden {} <code>Section</code> Tags gefunden'.format(len(sections)))
        with st.expander('Alle gefundenen <section>-Tags anzeigen'):
            st.write(sections)
    else:
        message.warning(f'Es wurden keine <code>Section</code> Tags gefunden')
        if tips:
            message.tips("Hinweis", "Der Section-Tag ist wichtig, da er eine semantische Strukturierung des Inhalts ermöglicht, was wiederum die Zugänglichkeit, SEO und allgemeine Lesbarkeit der Webseite verbessert. Er hilft dabei, den Inhalt in logische Abschnitte zu unterteilen, was es den Suchmaschinen erleichtert, den Inhalt zu indexieren und zu verstehen.")

def check_paragraph_tag(url, res, soup):
    paragraphs = soup.find_all('p')
    if len(paragraphs)>0:
        message.success('Es wurden {} <code>Paragraph</code> Tags gefunden'.format(len(paragraphs)))
        with st.expander('Alle gefundenen <p>-Tags anzeigen'):
            st.write(paragraphs)
    else:
        message.error(f'Es wurden keine <code>Paragraph</code> Tags gefunden')

def check_article_tag(url, res, soup, tips):
    article_tags = soup.find_all('article')
    if len(article_tags) == 0:
        message.info(f'Es wurde kein <code>Article</code> Tag gefunden')
        if tips:
            message.tips("Hinweis", "Der Article-Tag ist wichtig, da er eine semantische Strukturierung des Inhalts ermöglicht, was wiederum die Zugänglichkeit, SEO und allgemeine Lesbarkeit der Webseite verbessert. Er hilft dabei, einzelne Artikel oder Inhaltsblöcke innerhalb der Webseite hervorzuheben, was für Suchmaschinen und Nutzer gleichermaßen von Vorteil ist.")
    elif len(article_tags) > 1:
        message.success('Es wurden {} <code>Article</code> Tags gefunden'.format(len(article_tags)))
        with st.expander('Alle gefundenen <article>-Tags anzeigen'):
            st.write(article_tags)
    else:
        message.success(f'Es wurde genau ein <code>Article</code> Tag gefunden')
        with st.expander('Alle gefundenen <article>-Tags anzeigen'):
            st.write(article_tags)

def check_aside_tag(url, res, soup, tips):
    aside_tags = soup.find_all('aside')
    if len(aside_tags) == 0:
        message.info(f'Es wurde kein <code>Aside</code> Tag gefunden')
        if tips:
            message.tips("Hinweis", "Der Aside-Tag ist potenziell wichtig, da er eine semantische Strukturierung des Inhalts ermöglicht, was wiederum die Zugänglichkeit, SEO und allgemeine Lesbarkeit der Webseite verbessert. Er hilft dabei, zusätzlichen Inhalt, wie z.B. Anzeigen, Verweise oder zugehörige Inhalte, vom Hauptinhalt der Webseite zu trennen und zu kennzeichnen, was für Suchmaschinen und Nutzer gleichermaßen von Vorteil ist.")
    elif len(aside_tags) > 1:
        message.success('Es wurden {} <code>Aside</code> Tags gefunden'.format(len(aside_tags)))
        with st.expander('Alle gefundenen <aside>-Tags anzeigen'):
            st.write(aside_tags)
    else:
        message.success(f'Es wurde genau ein <code>Aside</code> Tag gefunden')
        with st.expander('Alle gefundenen <p>-Tags anzeigen'):
            st.write(aside_tags)

def check_h1_tag(url, res, soup, tips):
    h1_tags = soup.find_all('h1')
    if len(h1_tags) == 0:
        message.error(f'Es wurde kein <code>H1</code> Tag gefunden')
        if tips:
            message.tips("Rankingfaktor", "Im Dokument wurde keine H1-Überschrift gefunden. Die H1-Überschrift ist ein wichtiger Rankingfaktor, da in ihr in den meisten Fällen das Fokus-Keyword enthalten ist. Diese Überschrift hat die stärkste Gewichtung und ist somit am wichtigsten.")
    elif len(h1_tags) > 1:
        message.error('Es wurden {} <code>H1</code> Tags gefunden'.format(len(h1_tags)))
        with st.expander('Alle gefundenen <h1>-Tags anzeigen'):
            st.write(h1_tags)
        if tips:
            message.tips("Rankingfaktor", "Es wird empfohlen, nur einen H1-Tag pro Seite zu verwenden, um den Haupttitel der Seite auszuzeichnen und somit eine klare Hierarchie des Inhalts zu schaffen, was für Suchmaschinen und Nutzer gleichermaßen von Vorteil ist.")
    else:
        message.success(f'Es wurde genau ein <code>H1</code> Tag gefunden')
        with st.expander('Alle gefundenen <h1>-Tags anzeigen'):
            st.write(h1_tags)

def check_all_headings(url, res, soup):
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    if len(headings)>0:
        message.success('Es wurden {} <code>Überschriften</code> Tags gefunden'.format(len(headings)))
        with st.expander('Alle gefundenen Überschriften anzeigen'):
            st.write(headings)
    else:
        message.info(f'Es wurden keine <code>Überschriften</code> Tags gefunden')

def check_headings_hierarchy(url, res, soup, tips):
    try:
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])

        hierarchy = {'h1': 0, 'h2': 1, 'h3': 2, 'h4': 3, 'h5': 4, 'h6': 5}
        errors = []
        for i in range(1, len(headings)):
            curr_heading = headings[i]
            prev_heading = headings[i-1]
            curr_level = hierarchy[curr_heading.name]
            prev_level = hierarchy[prev_heading.name]
            if curr_level > prev_level + 1:
                errors.append(f'{prev_heading.name} ({prev_heading.text.strip()}) - gefolgt von - {curr_heading.name} ({curr_heading.text.strip()})')

        if errors:
            message.error('Die  Überschriften haben eine fehlerhafte Hierarchie')
            with st.expander('Fehlerhafte Hierachie anzeigen'):
                for error in errors:
                    message.text(error)
            if tips:
                message.tips("Rankingfaktor", "Eine wichtige SEO-Praxis ist es, die wichtigsten Keywords und Phrasen in die Überschriften einzubinden und diese möglicherweise weiter oben in der Hierarchie zu platzieren, um die semantische Struktur und Relevanz der Seite für Suchmaschinen zu verbessern. Eine klare Hierarchie der Überschriften von H1 bis H6 ist dabei entscheidend, um eine gut strukturierte und leicht verständliche Seite zu schaffen.")
        else:
            message.success('Die Überschriften haben eine korrekte Hierarchie')
    except requests.exceptions.RequestException as e:
        message.error('Fehler beim Abrufen der Seite:', e)

def check_ul_tag(url, res, soup):
    u_list = soup.find_all('ul')
    if len(u_list)>0:
        message.success('Es wurden {} <code>UL</code> Tags gefunden'.format(len(u_list)))
        with st.expander('Alle gefundenen <ul>-Tags anzeigen'):
            st.write(u_list)
    else:
        message.info(f'Es wurden keine <code>UL</code> Tags gefunden')

def check_ol_tag(url, res, soup):
    o_list = soup.find_all('ol')
    if len(o_list)>0:
        message.success('Es wurden {} <code>OL</code> Tags gefunden'.format(len(o_list)))
        with st.expander('Alle gefundenen <ol>-Tags anzeigen'):
            st.write(o_list)
    else:
        message.info(f'Es wurden keine <code>OL</code> Tags gefunden')

def check_form_tag(url, res, soup):
    forms = soup.find_all('form')
    if len(forms)>0:
        message.success('Es wurden {} <code>Form</code> Tags gefunden'.format(len(forms)))
        with st.expander('Alle gefundenen <form>-Tags anzeigen'):
            st.write(forms)
    else:
        message.info(f'Es wurden keine <code>Form</code> Tags gefunden')

def check_input_text(url, res, soup):
    inputs = soup.find_all('input', {'type': 'text'})
    if len(inputs)>0:
        message.success('Es wurden {} <code>Input Text</code> Tags gefunden'.format(len(inputs)))
        with st.expander('Alle gefundenen <input>-Tags anzeigen'):
            st.write(inputs)
    else:
        message.info(f'Es wurden keine <code>Input Text</code> Tags gefunden')

def check_input_email(url, res, soup):
    inputs = soup.find_all('input', {'type': 'email'})
    if len(inputs)>0:
        message.success('Es wurden {} <code>Input E-Mail</code> Tags gefunden'.format(len(inputs)))
        with st.expander('Alle gefundenen <input>-Tags anzeigen'):
            st.write(inputs)
    else:
        message.info(f'Es wurden keine <code>Input E-Mail</code> Tags gefunden')

def check_input_password(url, res, soup):
    inputs = soup.find_all('input', {'type': 'password'})
    if len(inputs)>0:
        message.success('Es wurden {} <code>Input Password</code> Tags gefunden'.format(len(inputs)))
        with st.expander('Alle gefundenen <input>-Tags anzeigen'):
            st.write(inputs)
    else:
        message.info(f'Es wurden keine <code>Input Password</code> Tags gefunden')

def check_input_checkbox(url, res, soup):
    inputs = soup.find_all('input', {'type': 'checkbox'})
    if len(inputs)>0:
        message.success('Es wurden {} <code>Input Checkbox</code> Tags gefunden'.format(len(inputs)))
        with st.expander('Alle gefundenen <input>-Tags anzeigen'):
            st.write(inputs)
    else:
        message.info(f'Es wurden keine <code>Input Checkbox</code> Tags gefunden')

def check_input_checkbox(url, res, soup):
    inputs = soup.find_all('input', {'type': 'checkbox'})
    if len(inputs)>0:
        message.success('Es wurden {} <code>Input Checkbox</code> Tags gefunden'.format(len(inputs)))
        with st.expander('Alle gefundenen <input>-Tags anzeigen'):
            st.write(inputs)
    else:
        message.info(f'Es wurden keine <code>Input Checkbox</code> Tags gefunden')

def check_input_radiobutton(url, res, soup):
    inputs = soup.find_all('input', {'type': 'radio'})
    if len(inputs)>0:
        message.success('Es wurden {} <code>Input Radiobutton</code> Tags gefunden'.format(len(inputs)))
        with st.expander('Alle gefundenen <input>-Tags anzeigen'):
            st.write(inputs)
    else:
        message.info(f'Es wurden keine <code>Input Radiobutton</code> Tags gefunden')

def check_label_tags(url, res, soup):
    labels = soup.find_all('label')
    if len(labels)>0:
        message.success('Es wurden {} <code>Label</code> Tags gefunden'.format(len(labels)))
        with st.expander('Alle gefundenen <label>-Tags anzeigen'):
            st.write(labels)
    else:
        message.info(f'Es wurden keine <code>Label</code> Tags gefunden')

def check_input_button(url, res, soup):
    inputs = soup.find_all('input', {'type': 'button'})
    if len(inputs)>0:
        message.success('Es wurden {} <code>Input Button</code> Tags gefunden'.format(len(inputs)))
        with st.expander('Alle gefundenen <input>-Tags anzeigen'):
            st.write(inputs)
    else:
        message.info(f'Es wurden keine <code>Input Button</code> Tags gefunden')

def check_input_textarea(url, res, soup):
    inputs = soup.find_all('textarea')
    if len(inputs)>0:
        message.success('Es wurden {} <code>Textarea</code> Tags gefunden'.format(len(inputs)))
        with st.expander('Alle gefundenen <textarea>-Tags anzeigen'):
            st.write(inputs)
    else:
        message.info(f'Es wurden keine <code>Textarea</code> Tags gefunden')
    


def w3c_validation(url):
    api_url = 'https://validator.w3.org/nu/?out=json'
    headers = {'Content-Type': 'text/html; charset=utf-8'}
    data = requests.get(url, headers=headers).content

    response = requests.post(api_url, data=data, headers=headers)

    result = response.json()
    errors = []
    for element in result['messages']:
        if 'Trailing slash on void elements' in element['message']:
            pass
        else:
            errors.append(element['message'])

    if errors:
        message.error("Das HTML Dokument ist ungültig")
        with st.expander("Alle HTML Validierungsfehler anzeigen"):
            for error in errors:
                message.text(error)
    else:
        message.success("Das HTML Dokument ist gültig")

def render(url, res, soup, tips):
    options = ['Essenziell', 'Hauptstruktur', 'Navigation', 'Inhalt', 'Überschriften', 'Listen', 'Formulare']
    default_options = ['Essenziell', 'Hauptstruktur', 'Navigation', 'Inhalt', 'Überschriften']
    st.sidebar.markdown('---')
    selected_options = st.sidebar.multiselect('Verfügbare Metriken:', options, default_options)

    # tips = st.sidebar.checkbox("Tipps und Hinweise anzeigen")

    if 'Essenziell' in selected_options:
        st.subheader('Essenziell:')
        check_html_tag(url, res, soup, tips)
        check_head_tag(url, res, soup, tips)
        check_body_tag(url, res, soup, tips)

    if 'Hauptstruktur' in selected_options:
        st.subheader('Hauptstruktur:')
        check_header_tag(url, res, soup, tips)
        check_main_tag(url, res, soup, tips)
        check_footer(url, res, soup, tips)

    if 'Navigation' in selected_options:
        st.subheader('Navigation:')
        check_nav_tag(url, res, soup)

    if 'Inhalt' in selected_options:
        st.subheader('Inhalt:')
        check_section_tag(url, res, soup, tips)
        check_paragraph_tag(url, res, soup)
        check_article_tag(url, res, soup, tips)
        check_aside_tag(url, res, soup, tips)

    if 'Überschriften' in selected_options:
        st.subheader('H1 Überschrift:')
        check_h1_tag(url, res, soup, tips)
        st.subheader("Alle Überschriften:")
        check_all_headings(url, res, soup)
        st.subheader('Überschriften-Hierachie:')
        check_headings_hierarchy(url, res, soup, tips)

    if "Listen" in selected_options:
        st.subheader("Listen:")
        check_ul_tag(url, res, soup)
        check_ol_tag(url, res, soup)

    if "Formulare" in selected_options:
        st.subheader("Formulare:")
        check_form_tag(url, res, soup)
        check_input_text(url, res, soup)
        check_input_email(url, res, soup)
        check_input_password(url, res, soup)
        check_input_checkbox(url, res, soup)
        check_input_radiobutton(url, res, soup)
        check_input_textarea(url, res, soup)
        check_label_tags(url, res, soup)
        check_input_button(url, res, soup)