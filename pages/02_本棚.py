import streamlit as st
import os
import common
import warnings
from db_connection import DBConnection

warnings.simplefilter("ignore")

# ページコンフィグ
st.set_page_config(
    page_title="Books",
    page_icon="📚",
    layout="wide",
)

# ログインチェック
# common.check_login()

# DB接続
db = DBConnection()

# 本のタイトルを取得
book_data = db.get_all("books")
book_titles = [b["key"] for b in book_data]
book_idx = {book_title: idx for idx, book_title in enumerate(book_titles)}
book_pagenums = {b["key"]: int(b["pages"]) for b in book_data}

# 本のタイトル選択時のon_change


def on_change_book_title():
    st.session_state.page_index = 0

# ページ選択時のon_change


def on_change_page_num():
    st.session_state.page_index = st.session_state.page_num-1

# 次へボタン押下時のon_click


def on_click_next():
    st.session_state.page_index += 1

# 前へボタン押下時のon_click


def on_click_prev():
    st.session_state.page_index -= 1


if "book_title_n" not in st.session_state and "page_index_n" not in st.session_state:
    st.session_state.book_title_n = None
    st.session_state.page_index_n = None

if st.session_state.book_title_n is not None and st.session_state.page_index_n is not None:
    st.session_state.book_title = st.session_state.book_title_n
    st.session_state.page_index = st.session_state.page_index_n
    st.session_state.book_title_n = None
    st.session_state.page_index_n = None

### 本の一覧から選択: サイドバー ###
if "book_title" not in st.session_state:
    st.sidebar.selectbox(
        "本のタイトル",
        book_titles,
        placeholder="本を選択",
        index=None,
        key="book_title",
        on_change=on_change_book_title
    )
else:
    st.sidebar.selectbox(
        "本のタイトル",
        book_titles,
        placeholder="本を選択",
        index=book_idx[st.session_state.book_title],
        key="book_title",
        on_change=on_change_book_title
    )

### ページ選択: サイドバー ###
if st.session_state.book_title is not None:
    st.sidebar.selectbox(
        "ページ",
        list(range(1, book_pagenums[st.session_state.book_title]+1)),
        placeholder="ページを選択",
        index=st.session_state.page_index,
        key="page_num",
        on_change=on_change_page_num
    )

### 内容を取得・表示：メイン ###
if st.session_state.book_title is not None and "page_index" in st.session_state:
    md_txt = db.get(
        "bookcontents", f"{st.session_state.book_title}_page{st.session_state.page_index+1}")["text"]
    st.markdown(md_txt)

    # ページ遷移
    col = st.columns((5, 1, 1, 5))
    if st.session_state.page_index > 0:
        col[1].button("前へ", on_click=on_click_prev)

    if st.session_state.page_index < book_pagenums[st.session_state.book_title]-1:
        col[2].button("次へ", on_click=on_click_next)
elif st.session_state.book_title is None:
    st.info("サイドバーから本を選択してください．")

# 生成成功時はballoonを表示
if "balloon" in st.session_state and st.session_state.balloon == True:
    st.balloons()
    st.session_state.balloon = False
