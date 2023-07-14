import streamlit as st
from globals import message
from globals import tips
from metrics import meta_data

def render(url, res, tips):
    meta_data.render(url, res, tips)