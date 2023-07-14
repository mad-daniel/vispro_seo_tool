import streamlit as st

def success(text):
    st.markdown(f"<div class='success'><i class='fas fa-check'></i>{text}</div>", unsafe_allow_html=True)

def error(text):
    st.markdown(f"<div class='error'><i class='fas fa-times'></i>{text}</div>", unsafe_allow_html=True)

def warning(text):
    st.markdown(f"<div class='warning'><i class='fas fa-exclamation'></i>{text}</div>", unsafe_allow_html=True)

def info(text):
    st.markdown(f"<div class='info'><i class='fas fa-exclamation'></i>{text}</div>", unsafe_allow_html=True)

def tips(headline, text):
    st.markdown(f"<div class='tips'><h4>{headline}</h4><p>{text}</p></div>", unsafe_allow_html=True)


def text(text):
    st.markdown(f"<div class='text'>{text}</div>", unsafe_allow_html=True)
