from deta import Deta
import streamlit as st

class DBConnection:
    def __init__(self):
        self.deta = Deta(st.secrets["data_key"])
        pass

    def add(self, name, key, data):
        db = self.deta.Base(name)
        db.put(data, key=key)
    
    def get_all(self, name):
        db = self.deta.Base(name)
        item = db.fetch().items
        return item
    
    def get(self, name, key):
        db = self.deta.Base(name)
        item = db.get(key)
        return item
    
if __name__ == "__main__":
    db = DBConnection()
    md_text = open("./contents/PHP/page1.md", "r", encoding="utf-8").read()
    db.add("test", "test", {"text": md_text})
    print(db.get("test", "test"))
