import streamlit as st
from globals import message
from metrics import technical

def render(url, res, soup, tips):
    technical.render(url, res, soup, tips)
