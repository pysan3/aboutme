# mattermostに進捗をあげるlinuxコマンド

<!-- description -->
chat.esslab.jpに接続し、ch_{username}にコマンドラインで指定した文字を投稿してくれるコマンドを作成しました。作業に取り掛かる前にその日の目標などを簡単に共有することができます。さらに、進捗報告を簡単に行なうことができます。
<!-- enddescription -->

## レポジトリ

[GitLab:myStatus2mattermost](https://git.esslab.jp/takuto/mystatus2mattermost)

## インストール

```bash
git clone https://git.esslab.jp/takuto/mystatus2mattermost.git
export PATH="$PATH:/path/to/mystatus2mattermost"                # please set $PATH to execute
# ln -s $PWD/mystatus2mattermost/mattermost /path/executable    # or you can create a symbolic link
mattermost setup
```

* GitLabのレポジトリよりcloneしたのち、コマンドへパスを通してください。
  * 当コマンドは単一ファイルで実行が可能であるため、mattermostというファイルへのシンボリックリンクを貼ることでも実行することができます。
* `mattermost setup`でユーザ名やmattermostのパスワードを入力してください。

## 使い方

パスを通したあとは、任意のコマンドラインからコマンドが実行可能です。

このコマンドは計7種類のコマンドが用意されています。
また、commandを指定せずに実行すると、使用可能なオプションの一覧を見ることができます。

```bash
mattermost [command] [msg...]

    commands:
        setup           - login_id等設定
        user            - see user config
        task "msg"      - 作業内容を報告    -> 【作業開始】 msg
        done "msg"      - 進捗を報告        -> 【進捗報告】 msg
        post "msg"      - つぶやく          -> msg
        todo "msg"      - TODOを投稿        -> TODO: msg
        share "msg"     - 情報を共有        -> 【共有】\n msg
        memo "msg"      - ( ..)φメモメモ    -> [memo] msg
        quote "file.md" - ファイルの中身を```で囲って投稿
```
