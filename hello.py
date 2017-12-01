# coding=utf-8
import os
import requests

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    ImageSendMessage,
    FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage, LocationMessage, ConfirmTemplate,
    MessageTemplateAction, TemplateSendMessage, ButtonsTemplate, URITemplateAction, PostbackTemplateAction
)

app = Flask(__name__)
file_path = "./image"

# Lineのアクセスキー
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/")
def route_dir():
    html = """
    <head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap.min.css" integrity="sha384-/Y6pD6FV/Vv2HJnA6t+vslU6fwYXjCFtcEpHbNJ0lyAFsXTsjBbfaDjzALeQsN6M" crossorigin="anonymous">
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper.min.js" integrity="sha384-b/U6ypiBEHpOf/4+1nzFpr53nxSS+GLCkfwBdFNTxtclqqenISfwAzpKaMNFNmj4" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/js/bootstrap.min.js" integrity="sha384-h0AbiXch4ZDo7tp9hKZ4TsHbi047NrKGLO3SEJAg45jXxnGIfYzk4Si90RDIqNm1" crossorigin="anonymous"></script>
    </head>
    <body>
    <h1>Hello world</h1>
    </body>"""
    return html


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text="登録友達追加ありがとうございます"),
            TextSendMessage(text="このbotは登録してある服から服装の提案を行います"),
            TextSendMessage(text="初めに「チュートリアル」と入力してください!")
        ]
    )


# 画像IDを返す
# @handler.add(MessageEvent, message=ImageMessage)
# def handle_image(event):
#    line_bot_api.reply_message(
#        event.reply_token,
#        TextSendMessage(text=event.message.id)
#    )


@handler.add(MessageEvent, message=ImageMessage)
def image_message(event):
    """repeat gotten image"""
    msg_id = event.message.id
    message_content = line_bot_api.get_message_content(msg_id)
    f_path = '/tmp/' + msg_id + '.jpg'
    try:
        with open('.' + f_path, 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)
<<<<<<< HEAD
        print(f_path)
        header = {'content-type': 'application/json'}
        print(requests.post(url='http://127.0.0.1:9999/resize', headers=header, data="{'image_path':'" + f_path + "'}"))
=======
                print(f_path)
                header = {'content-type':'application/json'}
        print(requests.post(url='http://127.0.0.1:9999/resize',headers=header, data="{'image_path':'"+f_path+"'}"))
>>>>>>> d85f3547fb9f200325911bdc9f6498f80be9772f
        line_bot_api.reply_message(
            event.reply_token,[
                TextSendMessage(text="Topsの場合は"),
                TextSendMessage(text=msg_id + ":Tops"),
                TextSendMessage(text="Bottomsの場合は"),
                TextSendMessage(text=msg_id +":Bottoms"),
                TextSendMessage(text="と入力してください")
            ]
        )
    except:
        import traceback
        traceback.print_exc()


@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    lat = str(event.message.latitude)
    lng = str(event.message.longitude)
    msg = ('your location is ' + lat + ',' + lng)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))


# 画像保存　コメントアウト中
# @handler.add(MessageEvent, message=ImageMessage)
# def save(event):
#    MessageId = str(event.message.id)
#    message_content = line_bot_api.get_message_content(MessageId)
#    with open(file_path, 'wb') as fd:
#        for chunk in message_content.iter_content():
#            fd.write(chunk)
#            line_bot_api.reply_message(
#                event.reply_token,
#                TextSendMessage(text="保存")
#            )


# pushメッセージ
# @handler.add(MessageEvent)
# def push_message():
#    line_bot_api.push_message('U68c89b1ff06c2a997c249340fae7040b',TextMessage(text='message1'))


@handler.add(MessageEvent, message=TextMessage)
def confirm_message(event):
    text = event.message.text
    # textがconfirmなら2択表示
    if text == 'confirm':
        confirm_template = ConfirmTemplate(text='Do it?', actions=[
            MessageTemplateAction(label='Yes', text='Yes!'),
            MessageTemplateAction(label='No', text='No!'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(
            event.reply_token,
            template_message
        )
    elif text == 'buttons':
        buttons_template = ButtonsTemplate(
            title='My buttons sample', text='Hello, my buttons', actions=[
                URITemplateAction(
                    label='Go to line.me', uri='https://line.me'),
                PostbackTemplateAction(label='ping', data='ping'),
                PostbackTemplateAction(
                    label='ping with text', data='ping',
                    text='ping'),
                MessageTemplateAction(label='Translate Rice', text='米')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'チュートリアル':
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text="Topsの登録を行います"),
                TextSendMessage(text="Topsの画像を送信して、その後の指示に従ってください"),
                TextSendMessage(text="画像登録が成功すればチュートリアル終了です")
            ])
    elif text == 'テスト':
        line_bot_api.push_message('U68c89b1ff06c2a997c249340fae7040b', TextSendMessage(text='message1'))
    elif text == '確認':
        test_text = event.source.user_id
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=test_text)
        )
    elif ':Tops' in text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='登録完了です！!')
        )
    elif ':Bottoms' in text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='登録完了です！!')
        )
    else:
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='ご利用ありがとうございます'),
                TextSendMessage(text='このbotはあなたが登録した服の中から次の日の服装を提案します'),
                TextSendMessage(text='服の登録は画像の送信→服の種類選択の手順で行えます')
            ]
        )


if __name__ == "__main__":
    app.run(debug=True)
