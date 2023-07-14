import streamlit as st
from globals import message
from metrics import html5_structure

def render(url, res, soup, tips):
    html5_structure.render(url, res, soup, tips)