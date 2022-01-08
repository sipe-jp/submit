# プログラム
開発環境
windows10
SublimeText
Python 3.9.1

私の環境での動作確認は致しました。しかし、環境によってはエラーが出る可能性があります。ご承知ください。
ユーザーによる変更は変数N,t,mとなります。
監査ファイルと同じディレクトリで実行し第一引数に監査ファイルをに入力する必要があります。または、直接pathを明記することも可能です。
標準ライブラリのみで実行することができます。

#プログラムの簡単な処理の流れ<br>
ファイルを読み込み、list(list_log)化<br>
スイッチ障害判断を行うため全ての監査サーバーをネットワーク部ごとにlist(list_ipadress_server)化<br>
過負荷確認のためそれぞれのサーバーの最新ping(m個)を最大要素数mのlist(list_ping_average)化<br>
mainでは、それぞれの状態ごとに問題の通り出力する<br>
最後まで復帰していないものや過負荷なものを出力する<br>

#ファイル構造
プログラム本体はlog_analytics.pyのみ
test_fileにはテストデータ４つ(sample,test.txt)と出力結果のoutput.txtが入っています。
output.txtの出力結果は、コンソールから張り付けたものになります。

#注意
log_analytics.pyのpath=path+"/"+sys.argv[0]ではなくlog_analytics.pyのpath=path+"/"+sys.argv[1]です。
間違えていました、ここを変更しないとコンソールでエラーが出ます。
