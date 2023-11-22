import streamlit as st
import os
from streamlit_extras.switch_page_button import switch_page
import time
import common
import markdown
import warnings
from openai_adapter import OpenAIAdapter

warnings.simplefilter("ignore")

# コンフィグ
st.set_page_config(
    page_title="Generate Text",
    page_icon=":robot_face:",
    layout="wide"
)

common.check_login()

adapter = OpenAIAdapter()

model_names = {"GPT-3.5": "gpt-3.5-turbo-1106", "GPT-4": "gpt-4-1106-preview"}

st.session_state.page_index_n = None
st.session_state.book_title_n = None
# submit時の処理


def submit():
    st.session_state.submitted = True
    st.session_state.title = title
    st.session_state.model_name = model_name
    st.session_state.temperature = temperature


# 生成したい本のタイトルを入力
# labelにはmarkdownを使用
if "submitted" not in st.session_state or st.session_state.submitted == False:
    with st.form("title_form"):
        st.markdown("## 生成したい本のタイトルを入力してください")
        title = st.text_input(":book: 本のタイトル", value="",
                              placeholder="生成したい本のタイトルを入力")
        model_name = st.radio("モデル名：GPT4はGPT3.5と比べると高性能であり，精度の高い回答を行ってくれるバージョン", list(
            model_names.keys()), horizontal=True, index=0)
        temperature = st.slider("温度：温度が低いほど一貫性のある生成が期待でき，高いほど多様性のある生成が期待できる",
                                min_value=0.0, max_value=1.0, value=0.5, step=0.01)
        submitted = st.form_submit_button("生成", on_click=submit)
else:
    with st.form("title_form"):
        st.markdown("## 生成したい本のタイトルを入力してください")
        title = st.text_input(
            ":book: 本のタイトル", value=st.session_state.title, placeholder="生成したい本のタイトルを入力")
        model_name = st.radio("モデル名：GPT4はGPT3.5と比べると高性能であり，精度の高い回答を行ってくれるバージョン", list(model_names.keys(
        )), index=list(model_names.keys()).index(st.session_state.model_name), horizontal=True)
        temperature = st.slider("温度：温度が低いほど一貫性のある生成が期待でき，高いほど多様性のある生成が期待できる",
                                min_value=0.0, max_value=1.0, value=st.session_state.temperature, step=0.01)
        submitted = st.form_submit_button("生成", on_click=submit, disabled=True)
    with st.spinner("""
        生成中，しばらくお待ちください．
        生成が終わると自動的に本棚に移動します．
    """):
        st.session_state.submitted = False
        adapter.create(title, model_names[model_name], temperature=temperature)
    # 本のタイトルとページを指定して本棚に移動
    st.session_state.page_index_n = 0
    st.session_state.book_title_n = title
    # balloonを表示
    st.session_state.balloon = True
    switch_page("本棚")
