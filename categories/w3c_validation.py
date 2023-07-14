import streamlit as st
import requests
from globals import message

def render(url):
    api_url = 'https://validator.w3.org/nu/?out=json'
    headers = {'Content-Type': 'text/html; charset=utf-8'}
    data = requests.get(url, headers=headers).content

    response = requests.post(api_url, data=data, headers=headers)

    result = response.json()
    errors = []
    ignored = []
    for element in result['messages']:
        if 'Trailing slash on void elements' in element['message']:
            ignored.append(element['message'])
        else:
            errors.append(element['message'])

    if errors:
        message.error("Das HTML Dokument ist ungültig")
        for error in errors:
            message.text(error)
    else:
        message.success("Das HTML Dokument ist gültig")

    if ignored:
        st.write("")
        message.info("Einige Validierungsfehler wurden ignoriert")
        with st.expander("Ignorierte Fehler anzeigen"):
            for case in ignored:
                message.text(case)