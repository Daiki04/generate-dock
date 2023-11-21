import streamlit as st
import os
import common
from db_connection import DBConnection

# コンフィグ
st.set_page_config(
    page_title="Books",
    page_icon="📚",
    layout="wide",
)

common.check_login()

db = DBConnection()

# 本のタイトルを取得
book_data = db.get_all("books")
book_titles = [b["key"] for b in book_data]
book_idx = {book_title: idx for idx, book_title in enumerate(book_titles)}
book_pagenums = {b["key"]: int(b["pages"]) for b in book_data}

# 本の一覧から選択時のon_change
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

if st.session_state.book_title_n is not None and st.session_state.page_index_n is not None:
        st.session_state.book_title = st.session_state.book_title_n
        st.session_state.page_index = st.session_state.page_index_n
        st.session_state.book_title_n = None
        st.session_state.page_index_n = None

# 本の一覧から選択: サイドバー
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

# st.info(st.session_state.book_title)
# if st.session_state.book_title is not None:
#     st.info(book_idx[st.session_state.book_title])

# ページ選択: サイドバー
if st.session_state.book_title is not None:
    st.sidebar.selectbox(
        "ページ",
        list(range(1, book_pagenums[st.session_state.book_title]+1)),
        placeholder="ページを選択",
        index=st.session_state.page_index,
        key="page_num",
        on_change=on_change_page_num
    )

# if "page_num" in st.session_state:
#     st.info(st.session_state.page_num)
#     st.info(st.session_state.page_index)

# 内容を取得：メイン
if st.session_state.book_title is not None and "page_index" in st.session_state:
    md_txt = db.get("bookcontents", f"{st.session_state.book_title}_page{st.session_state.page_index+1}")["text"]
    st.markdown(md_txt)

    # ページ遷移
    col = st.columns((5, 1, 1, 5))
    if st.session_state.page_index > 0:
        col[1].button("前へ", on_click=on_click_prev)

    if st.session_state.page_index < book_pagenums[st.session_state.book_title]-1:
        col[2].button("次へ", on_click=on_click_next)
elif st.session_state.book_title is None:
    st.info("サイドバーから本を選択してください．")

# balloon
if "balloon" in st.session_state and st.session_state.balloon == True:
    st.balloons()
    st.session_state.balloon = False
