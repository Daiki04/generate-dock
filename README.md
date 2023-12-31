# generate-dock

### システム概要

#### 背景
2000年ごろからの急速なグローバル化により，様々な文化・価値観に触れる中で社会の価値観が変化し，多様性の尊重が社会的に重要なテーマとなっている．

教育の分野では「個に応じた指導」が一層重視されており，生徒の興味・関心等に応じて一人一人に対応した学習活動や学習課題に取り組む機会を提供することが求められている．教師の長時間勤務による疲弊や教員採用倍率の低下により教師不足が深刻化している中でこのようなニーズに対応するためにGIGAスクール構想のようなICTを活用した教育の充実が進められている．

#### 課題
教育現場では，異なる学習スタイル，興味や学習進度を持つ生徒たちに対応することが課題となっている．従来の教科書やカリキュラムは一般的で統一されたものであり，教師が持つ知識にも限りがあるため生徒たちの多様性への対応が限定的になっている．

#### 目的
本アプリケーションでは生徒一人ひとりの学習ニーズに合わせた学習教材を提供することを目的として，個々の生徒が自身の興味や課題を入力することで，それに対応した学習教材を提供する．


アプリケーションの提供を通して以下のようなことを期待している．
- 生徒の興味・関心に合わせた学習教材を提供することで，生徒の学習意欲を高める
- 特殊なニーズを持つ生徒に対しても，適切なサポートを提供する
- 生徒が自らの学習の状況を把握し，主体的に学習を調整することができる能力を育成する
- 地理的・経済的な要因によってアクセスできる教育リソースへの格差を解消し，教育の均等性を向上させる

### モデル概要
本アプリケーションではOpen AIの提供するGPT-3.5，GPT-4をAPI経由で使用する．

GPT-3.5はOpenAIが開発した自然言語処理のモデルであり，GPT-3（Generative Pre-trained Transformer 3）の改良版である．GPT-3.5では大量のテキストデータを学習して自然言語の理解と生成を行うことができる．GPT-3.5にはいくつかのモデルが存在し，本アプリケーションでは「gpt-3.5-turbo-1106」を使用する．

OpenAIが開発した自然言語処理のための人工知能モデルで，GPT-3，GPT-3.5から性能を向上させており，自然な対話や文章の生成が可能になるように設計されている．GPT-3よりも高度な文書の生成や自然言語理解が期待できる．GPT-4にはいくつかのモデルが存在し，本アプリケーションでは「gpt-4-1106-preview」を使用する．

以下のようなプロンプトにより，GPTモデルにキャラ付けを行っている．今回はユーザーとの対話を行わないため，プロンプトインジェクションへの対策は行わない．
```
[指示]
あなたは小中学生を生徒に持つ先生です．
名前は「タカシ」です．
あなたは幅広い知識があり，生徒からは頼りにされています．
生徒の好みに合わせて適切な教材を提供することが仕事です．
名前：タカシ
職業：教師
趣味：登山，読書
性格：他人思い、優しい，好奇心がある，ユーモアがある
出身：東京
好きな食べ物：牛タン
嫌いな食べ物：魚
好きな言葉：好奇心は全ての始まり

[タカシの情報]
幼いころから知的好奇心が強く，様々な技術・分野に触れてきた．
興味を持って何かを学びたい子供たちが学習できる環境を整えたいという思いから，教師になった．
教材を作ることも好きで，自分の教材を使って授業をすることもあり，ユーモアを交えながら小中学生でも理解できる言葉で楽しく学習できる教材作りを心がけている．
そのため教材には絵文字や「！」などが登場する．
```

モデルの詳細は[リンク](https://platform.openai.com/docs/models)を参照

### 技術概要

#### 機能要件

##### 画面

- ホーム画面
  - 利用方法，システム概要，技術概要，モデル概要，アカウント概要の表示，ログアウト・ログインを行う画面
- テキスト生成画面
  - 生成したいテキストの入力と送信，生成待機中スピナーの表示を行う画面
- 本棚
  - テキストの一覧表示と選択，選択したテキストの表示を行う画面

##### 権限

- ログインに成功したユーザーが画面にアクセスできる

##### 情報・データ

- 本システムでは以下のデータが作成され，DB に保存される
  - テキストのタイトル，ページ数データ
  - テキスト生成画面で生成された markdown 形式のテキストデータ

##### ログイン

- ログイン時にはユーザー名，パスワードを要求する

#### 非機能要件

- テキスト生成は 10 分以内で完了する
- 白を基調としたシンプルなデザインにする

### 利用方法
#### テキスト生成
1. サイドバーの「テキスト生成」をタブをクリック
2. 入力欄に生成したいテキストのテーマを入力
3. モデル名と温度を選択
4. 「生成」ボタンをクリック
5. テキストが生成されると自動的に「本棚」に遷移し，生成したテキストが表示される

#### テキストを読む 
1. サイドバーの「本棚」タブをクリック
2. サイドバーから読みたいテキストを選択
3. テキストが表示される