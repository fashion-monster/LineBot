linebotの表
===
各ポートとAPIをまとめておきます

ポート番号
### 5000

| 受信内容 |                     | 機能                                                          |
|----------|---------------------|---------------------------------------------------------------|
| フォロー |                     | ユーザIDをCSVに追加 リプライ                                  |
| 画像     |                     | 画像の保存 画像情報をQに送信 間違えなら正しい操作を促す       |
| テキスト | confirm             | confirmのリプライ                                             |
|          | buttons             | buttonsのリプライ                                             |
|          | チュートリアル      | 使い方のリプライの送信                                        |
|          | テスト              | push_message_duplicateにリクエスト                            |
|          | 確認                | 送信者のユーザIDをリプライで返す                              |
|          | おすすめ            | 服の画像送信                                                  |
|          | 'Tops' or 'Bottoms' | テキスト情報をQに送信 間違えなら正しい操作を促す              |
|          | :Topsを含む文       | csv書き込み リプライ similarityに画像が追加されたのを知らせる |
|          | :Bottomsを含む文    | csv書き込み リプライ similarityに画像が追加されたのを知らせる |
|          | クリア              | csvの初期化                                                   |
|          | その他のテキスト    | 定型文のリプライ                                              |



root一覧
/img_process_queue
img_process_queue()

/callback
callback()

/get_suggestion
get_suggestion()

/push_message_duplicate
push_message()プッシュメッセージを送る（使用しない）

/push_state
received_state()　仮で作ったまんま残っています

WebhookHandler一覧
handle_follow(event)フォローされたときユーザのID登録とリプライ送信
image_message(event)Qに画像のデータを送る
handle_location(event)緯度経度取得（現在動いてない）
confirm_message(event)テキストメッセージが送られてきたときの処理
