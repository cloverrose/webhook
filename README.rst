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
   .. code-block:: python
      # -*- coding:utf-8 -*-
      port = 12345  # 自動更新したいWebアプリのポート番号
      workdir = /path/to/targetproj  # 自動更新したいWebアプリのmanage.pyがあるディレクトリ
4. nohup python manage.py runserver 0.0.0.0:12344 > /tmp/nohup.out &
5. 自動更新したいWebアプリリポジトリのAdmin > Service Hooks > WebHook URLsにdomain.com:12344を追加
6. 自動更新したいWebアプリを更新してpushすれば自動更新が行われる

ToDo
====
1. masterブランチ以外の更新は無視するようにする
2. subprocess周りの使い方が正しいか確認
3. 0.0.0.0:portとしているけどそこら辺も汎化
