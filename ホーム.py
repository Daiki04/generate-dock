# ホーム画面

import streamlit as st
import streamlit_authenticator as stauth
import yaml
import warnings

warnings.simplefilter("ignore")

# # ユーザー情報の読み込み
# with open('config.yaml') as file:
#     config = yaml.load(file, Loader=yaml.SafeLoader)

# # 認証
# authenticator = stauth.Authenticate(
#     config['credentials'],
#     config['cookie']['name'],
#     config['cookie']['key'],
#     config['cookie']['expiry_days'],
#     config['preauthorized'],
# )


st.title("ものしり本棚")
st.write('ものしり本棚は知りたいことを入力すると，自動的に学習用テキストが生成されるサービスです')
st.warning('OpenAI APIは課金制のため，生成は1人1, 2回程度に抑えて頂けると幸いです')
st.info('多用する場合は https://github.com/Daiki04/generate-dock からソースコードをダウンロードして，API Keyを設定してくローカルで実行してください')

### ログイン処理 ###
# name, authentication_status, username = authenticator.login('Login', 'main')

### ログイン成功時 ###
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None

# if st.session_state["authentication_status"]:
if True:
    st.session_state.page_index_n = None
    st.session_state.book_title_n = None
    dir_path = './contents/'
    # tab1, tab2, tab3, tab4, tab5 = st.tabs(
    #     ["利用方法", "システム概要", "技術概要", "モデル概要", "アカウント"])
    tab1, tab2, tab3, tab4 = st.tabs(
        ["利用方法", "システム概要", "技術概要", "モデル概要"])

    with tab1:
        md_txt = open(dir_path + '説明.md', 'r', encoding='utf-8').read()
        st.markdown(md_txt)
    with tab2:
        md_txt = open(dir_path + '概要.md', 'r', encoding='utf-8').read()
        st.markdown(md_txt)
    with tab3:
        md_txt = open(dir_path + '技術概要.md', 'r', encoding='utf-8').read()
        st.markdown(md_txt)
    with tab4:
        md_txt = open(dir_path + 'モデル概要.md', 'r', encoding='utf-8').read()
        st.markdown(md_txt)
    # with tab5:
    #     st.title('アカウント')
    #     # アカウント名
    #     st.write('アカウント名：' + username)

    #     authenticator.logout('Logout', 'main')

### ログイン失敗時 ###
# elif st.session_state["authentication_status"] is False:
#     st.error('ユーザ名またはパスワードが間違っています')
# elif st.session_state["authentication_status"] is None:
#     st.info('Usenameにはjsmith，Passwordにはabcと入力してください')
#     st.warning('ユーザ名とパスワードを入力してください')
