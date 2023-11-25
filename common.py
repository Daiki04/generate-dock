import extra_streamlit_components as stx
import streamlit as st

# ログインチェック機能


def check_login():
    value = stx.CookieManager().get(cookie='some_cookie_name')
    if value == None:
        st.warning("**ログインしてください**")
        st.stop()
