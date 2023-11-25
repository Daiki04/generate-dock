from deta import Deta
import streamlit as st

# DBにはDetaを使用．Detaのキーはsecrets.toml内のdata_keyに記載
# Deta: https://deta.space/?horizon=ykr4Vc6VFg
# StreamlitでのDetalの使い方: https://docs.streamlit.io/knowledge-base/tutorials/databases/deta-base
# 使用する際は，secrets.tomlに以下のように記載すること
# deta_key = "{YOUR DETA KEY}"


class DBConnection:
    '''
    DBとの接続を行うクラス
    '''

    def __init__(self):
        '''
        DBの接続キーを読み込み
        '''
        self.deta = Deta(st.secrets["data_key"])

    def add(self, name, key, data):
        '''
        DBにデータを1件追加する

        Parameters
        ----------
        name : str
            DB名
        key : str
            キー
        data : dict
            追加するデータ
        '''
        db = self.deta.Base(name)
        db.put(data, key=key)

    def get_all(self, name):
        '''
        DBから全データを取得する

        Parameters
        ----------
        name : str
            DB名

        Returns
        -------
        item : list
            DBから取得したデータ
        '''

        db = self.deta.Base(name)
        item = db.fetch().items
        return item

    def get(self, name, key):
        '''
        DBから1件データを取得する

        Parameters
        ----------
        name : str
            DB名
        key : str

        Returns
        -------
        item : dict
            DBから取得したデータ
        '''

        db = self.deta.Base(name)
        item = db.get(key)
        return item


if __name__ == "__main__":
    db = DBConnection()
    md_text = open("./contents/PHP/page1.md", "r", encoding="utf-8").read()
    db.add("test", "test", {"text": md_text})
    print(db.get("test", "test"))
