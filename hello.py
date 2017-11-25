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
    msg_id = event.message.id
    message_content = line_bot_api.get_message_content(msg_id)
    f_path = '/tmp/' + msg_id + '.jpg'
    try:
        with open(f_path, 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)

        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(original_content_url='https://fashion.zoozoo-monster-pbl.work' + f_path,
                             preview_image_url='https://fashion.zoozoo-monster-pbl.work' + f_path)
        )
    except:
        import traceback
        traceback.print_exc()


@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    lat = str(event.message.latitude)
    lng = str(event.message.longitude)
    print(lat)
    print(lng)
    msg = ('your location is ' + lat + ',' + lng)
    print(lat)
    print(lng)

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
                TextSendMessage(text="「登録」と入力し、「Tops」をタップしてから画像の送信をしてください"),
                TextSendMessage(text="画像登録が成功すればチュートリアル終了です")
            ])
    elif text == '登録':
        confirm_template = ConfirmTemplate(text='登録する服の種類は？', actions=[
            MessageTemplateAction(label='Tops', text='Tops'),
            MessageTemplateAction(label='Bottoms', text='Bottoms'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(
            event.reply_token,
            template_message
        )
    elif text == 'Tops':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Tops')
        )
    elif text == 'Bottoms':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Bottoms')
        )
    elif text == 'テスト':
        line_bot_api.push_message('U68c89b1ff06c2a997c249340fae7040b', TextMessage(text='message1'))
    elif text == '確認':
        test_text = event.source.user_id
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=test_text)
        )
    else:
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='ご利用ありがとうございます'),
                TextSendMessage(text='このbotはあなたが登録した服の中から次の日の服装を提案します'),
                TextSendMessage(text='服の追加は「登録」→服の種類選択→画像の送信の手順で行えます')
            ]
        )


if __name__ == "__main__":
    app.run()
