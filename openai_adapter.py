import openai
import warnings
import dotenv
import os
import json
import sys
import streamlit as st
from db_connection import DBConnection


warnings.simplefilter("ignore")

# API key
key = st.secrets["api_key"]
openai.api_key = key

# 生成の最大試行回数
max_attempts = 10


class OpenAIAdapter:
    """
    OpenAI APIとの通信を行うクラス
    """

    def __init__(self):
        # system_prompt.txtからpromptを読み込む
        with open("system_prompt.txt", "r", encoding="utf-8") as f:
            self.system_prompt = f.read()

    def _create_message(self, role: str, message: str):
        """
        OpenAIのAPIに渡すpromptを作成する

        Parameters
        ----------
        role : str
            メッセージの送信者
        message : str
            メッセージの内容

        Returns
        -------
        dict
            メッセージ
        """
        return {
            "role": role,
            "content": message
        }

    def create_chapter(self, topic: str, model_name: str, temperature: float, max_tokens: int = 2048) -> str:
        '''
        目次を作成する

        Parameters
        ----------
        topic : str
            教材のタイトル
        model_name : str
            使用するモデルの名前
        temperature : float
            温度
        max_tokens : int, optional
            生成するトークンの最大数, by default 2048

        Returns
        -------
        str
            目次
        '''

        template = f"""
        あなたは先生で，全てJSON形式で出力します．
        「{topic}」というタイトルで教材を作成してください．
        ユーザーが段階的に技能・知識を身につけられるよう，テーマを分解し，適切なサブトピック，つまり，教材の目次を作成してください．
        「{topic}」を学ぶにあたって，最低限必要だと考えられるサブトピックのみを作成してください．
        ```jsonのようにjsonを囲むことは不要です．json形式のまま出力してください．
        必ず以下のようなPythonのjsonライブラリのjson.loadsで処理できるjson形式で回答を出力してください．
    
        {{
            {{1}}:{{サブトピック名}},
            {{2}}:{{サブトピック名}},
            {{3}}:{{サブトピック名}},
            ...
        }}
        """

        system_message = self._create_message("system", self.system_prompt)
        user_message = self._create_message("user", template)
        messages = [system_message, user_message]

        res = openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
        )

        topics = res["choices"][0]["message"]["content"]
        return topics

    def create_contens(self, topic: str, dict_chapters: [str, str], chapter: int, max_tokens: int) -> str:
        '''
        教材の内容を作成する

        Parameters
        ----------
        topic : str
            教材のタイトル
        dict_chapters : [str, str]
            教材の目次
        chapter : int
            担当する章
        max_tokens : int
            生成するトークンの最大数

        Returns
        -------
        str
            教材の内容
        '''

        template = f"""
        「{topic}」というタイトルで教材を作成している．
        教材の目次は以下の通りである．
        {dict_chapters}
        このうち，あなたは「{dict_chapters[chapter]}」の部分を作成する担当になった．
        担当部分に関して，小中学生を対象にユーモアを交えて楽しく知識・技能を身につけられるように教材を作成してください．
        以下の条件を満たすように教材を作成してください．
        - 必ずマークダウン形式であること
        - ```markdownのようにmarkdownを囲むことは不要です
        - プログラミングに関するトピックでは，生徒が実際に試すことができる実践的なコードを記述すること
        - 担当部分以外のトピックに関する説明をあなたの担当部分に記述しないこと
        - # {chapter}. {dict_chapters[chapter]} という見出しで始まること
        - 内部でサブトピックを分ける場合は，階層構造になるように見出しを記述すること．
          例：
          # chapter. chapter
            ...
          ## chapter.1 サブトピック名
            ...
        """
        system_message = self._create_message("system", self.system_prompt)
        user_message = self._create_message("user", template)
        messages = [system_message, user_message]

        res = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            messages=messages,
            max_tokens=max_tokens,
        )

        contents = res["choices"][0]["message"]["content"]

        return contents

    def create(self, theme, model_name, temperature):
        """
        教材を作成する

        Parameters
        ----------
        theme : str
            教材のタイトル
        model_name : str
            使用するモデルの名前
        temperature : float
            温度
        """

        db = DBConnection()
        for attempt in range(max_attempts):
            try:
                response = self.create_chapter(theme, model_name, temperature)
                response_json = json.loads(response)
                break
            except json.decoder.JSONDecodeError as e:
                print(f"JSONDecodeError: {e}")
                if attempt == max_attempts - 1:
                    raise e
                else:
                    print("Retrying...")
                    continue
            except Exception as e:
                st.error(f"予期せぬエラーが発生しました: {e}")
                sys.exit(1)
        print(f"num_chapters: {len(response_json)}")
        db.add("books", theme, {"pages": len(response_json)})
        for page, key in enumerate(response_json.keys()):
            content = self.create_contens(theme, response_json, key, 2048)
            db.add("bookcontents", f"{theme}_page{page+1}", {"text": content})
