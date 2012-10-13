=======
webhook
=======

目的
====
Webアプリを自動更新

Keyword
=======
Django, Github, Webhook

処理の流れ
==========
1. Webアプリを停止
2. masterブランチを更新　
3. Webアプリを起動

使い方
======
1. git clone git://github.com/cloverrose/webhook.git
2. cd webhook
3. emacs secret.py
   
   # -*- coding:utf-8 -*-
   
   port = 12345  # 自動更新したいWebアプリのポート番号
   
   workdir = /path/to/targetproj  # 自動更新したいWebアプリのmanage.pyがあるディレクトリ

   repos = { 'https://github.com/cloverrose/webhook' }  # 自動更新したいレポジトリのURL
4. nohup python manage.py runserver 0.0.0.0:12344 > /tmp/nohup.out &
5. 自動更新したいWebアプリリポジトリのAdmin > Service Hooks > WebHook URLsにdomain.com:12344を追加
6. 自動更新したいWebアプリを更新してpushすれば自動更新が行われる

ToDo
====
1. masterブランチ以外の更新は無視するようにする
   https://github.com/cloverrose/webhook/commit/c81932fd4bdea35bc0c7e9fda97f384b15c662fd で完了
2. subprocess周りの使い方が正しいか確認
3. 0.0.0.0:portとしているけどそこら辺も汎化
4. 複数Webアプリに対応
5. Unixファイルシステム以外への対応
