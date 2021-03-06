# coding=utf-8
import Queue
import csv
import json
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
    ImageSendMessage, FollowEvent, MessageEvent, TextMessage, TextSendMessage, ImageMessage, LocationMessage,
    ConfirmTemplate, UnfollowEvent,
    MessageTemplateAction, TemplateSendMessage, ButtonsTemplate, URITemplateAction, PostbackTemplateAction
)

import utils.weather as weather
from models.state import ActionState

app = Flask(__name__)
file_path = "./image"

# Lineのアクセスキー
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

q = Queue.Queue()


@app.route("/")
def route_dir():
    """assessable to 'https://www.zoozoo-monster.work/'
    Returns:
        html : html source code

    """
    html = """<head> <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/css/bootstrap
    .min.css" integrity="sha384-/Y6pD6FV/Vv2HJnA6t+vslU6fwYXjCFtcEpHbNJ0lyAFsXTsjBbfaDjzALeQsN6M"
    crossorigin="anonymous"> <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
    integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN"
    crossorigin="anonymous"></script> <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.11.0/umd/popper
    .min.js" integrity="sha384-b/U6ypiBEHpOf/4+1nzFpr53nxSS+GLCkfwBdFNTxtclqqenISfwAzpKaMNFNmj4"
    crossorigin="anonymous"></script> <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta/js/bootstrap
    .min.js" integrity="sha384-h0AbiXch4ZDo7tp9hKZ4TsHbi047NrKGLO3SEJAg45jXxnGIfYzk4Si90RDIqNm1"
    crossorigin="anonymous"></script> </head> <body> <h1>Hello world</h1> </body> """
    return html


@app.route("/callback", methods=['POST'])
def callback():
    """for LINE certificate.
    Returns:
        http status?
    """
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle web-hook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@app.route("/get_suggestion", methods=['POST'])
def get_suggestion():
    """get suggestion from sudo server, POST cloth combination to user.

    TODO: adapt to multi user

    Returns:
        http status?
    """
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    return 'OK'


@handler.add(FollowEvent)
def handle_follow(event):
    """when follow event occurred, write user id to follower.csv and reply

    Args:
        event:

    Returns:

    """
    user_id = event.source.user_id
    with open('follower.csv', 'a') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow([str(user_id)])
    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text="登録友達追加ありがとうございます"),
            TextSendMessage(text="このbotは登録してある服から服装の提案を行います"),
            TextSendMessage(text="リッチメニューから操作をお願いします")
        ]
    )


# フォロー解除イベント
@handler.add(UnfollowEvent)
def handle_unfollow(event):
    user_id = event.source.user_id  # フォロー解除したユーザのID
    list_data = []
    # csv読み込み開始
    f = open('follower.csv', 'r')
    readers = csv.reader(f)
    for row in readers:
        # フォロー解除したユーザ以外のIDをlistDataに
        if user_id not in row:
            list_data.append(row)
    # 上書き処理　csvの初期化
    with open('follower.csv', 'w') as q:
        writer = csv.writer(q, lineterminator='\n')
        for row in readers:
            writer.writerow(row)
    # listDataをcsvに書き込み
    with open('follower.csv', 'a') as q:
        writer = csv.writer(q, lineterminator='\n')
        for row1 in list_data:
            writer.writerow(row1)
    f.close()


@handler.add(MessageEvent, message=ImageMessage)
def image_message(event):
    """cropping, writing image_id to csv, sending message

    Args:
        event:

    Returns:

    """
    msg_id = event.message.id
    message_content = line_bot_api.get_message_content(msg_id)
    d = json.loads(json.loads(requests.get(url='http://127.0.0.1:5001').text))  # queue
    # 今までのキューを全部見る
    for state in d['queue']:
        if state['user_id'] != event.source.user_id:
            continue  # 1
        else:
            if (state['img_path'] is None) or (state[u'img_path'] is None):  # 正常な流れ
                try:
                    # 画像加工へ流す
                    f_path = '/tmp/' + msg_id + '.jpg'
                    with open('.' + f_path, 'wb') as fd:
                        for chunk in message_content.iter_content():
                            fd.write(chunk)
                    header = {'content-type': 'application/json'}

                    # 同期的なのでどうにかした方がいいかも
                    print(requests.post(url='http://127.0.0.1:9998/cloth_detect', headers=header, data=f_path))

                    # CSVに書く作業
                    type_list = [str(event.source.user_id), str(msg_id + '.jpg'), str(state['cloth_type'])]
                    with open('clothe_types.csv', 'a') as f:
                        writer = csv.writer(f, lineterminator='\n')
                        writer.writerow(type_list)
                    # Qに送る
                    header = {'content-type': 'application/json'}
                    # data = {'user_id': event.source.user_id, 'cloth_type': state[u'cloth_type'], 'img_path': f_path,
                    #         "action": 'image'}
                    data = ActionState(user_id=event.source.user_id,
                                       cloth_type=state['cloth_type'],
                                       img_path=msg_id+'.jpg',
                                       action='image',
                                       processing=ActionState.processing_state['busy']).to_dict()
                    # FIXME: ここも同期的なので変更したい
                    requests.post(url='http://127.0.0.1:5001', headers=header, data=json.dumps(data))
                    return True

                except Exception as e:
                    print(str(e))
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='先にトップスかボトムスを選択してください')
                    )
                    return False
        # 1
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='トップスかボトムスを選択してください')
    )
    return False
    #        line_bot_api.reply_message(
    #            event.reply_token,
    #            ImageSendMessage(original_content_url='https://fashion.zoozoo-monster-pbl.work' + f_path,
    #                             preview_image_url='https://fashion.zoozoo-monster-pbl.work' + f_path)
    #        )
    # except IOError:
    #     raise IOError
    # except:
    #     import traceback
    #     traceback.print_exc()


@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    """get location and get

    Args:
        event:

    Returns:

    """
    lat = str(event.message.latitude)
    lng = str(event.message.longitude)
    w = weather.Weather(lat=lat, lon=lng)
    temp = w.get_temp_max()
    msg = ('your location is ' + str(temp))
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))


@app.route('/push_message_duplicate', methods=['POST'])
def push_message():
    """

    Returns:

    """
    with open('follower.csv', 'r') as f:
        reader = csv.reader(f)  # readerオブジェクトを作成
        header = next(reader)  # 最初の一行をヘッダーとして取得
        print('header!!!!!!!', header)
        for _ in reader:
            line_bot_api.push_message(str(header[0]), [
                TextSendMessage(text="Topsの登録を行います"),
                TextSendMessage(text="Topsの画像を送信して、その後の指示に従ってください"),
                TextSendMessage(text="画像登録が成功すればチュートリアル終了です")  ##pushテスト用
            ])
    return "OK!"


@handler.add(MessageEvent, message=TextMessage)
def confirm_message(event):
    """


    Args:
        event:

    Returns:

    """
    text = event.message.text
    queue = json.loads(requests.get(url='http://127.0.0.1:5001').text)

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
    elif text == u'チュートリアル':
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text="おすすめは本日の服装の提案"),
                TextSendMessage(text="トップス登録はトップスボタンを押し画像送信"),
                TextSendMessage(text="ボトムス登録はボトムスボタンを押し画像送信"),
                TextSendMessage(text="あなたのMyクローゼットに服が登録されます")
            ])
    elif text == u'テスト':
        requests.post(url='https://127.0.0.1:5000/push_message_duplicate')
    elif text == u'確認':
        test_text = event.source.user_id
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=test_text)
        )
    elif text == u'おすすめ':
        # user_idを廖氏度算出にpost
        header = {'content-type': 'application/json'}
        data = {'user_id': event.source.user_id}
        r = requests.post(url='http://127.0.0.1:9000', headers=header, data=json.dumps(data))

        # 類似度算出後の画像セットを送信
        recommend = json.loads(str(r.text))
        recommend = json.loads(str(recommend))
        recommend_t = '/tmp/cropped/' + recommend["recommend"][0][u"Tops"]
        recommend_b = '/tmp/cropped/' + recommend["recommend"][0][u"Bottoms"]

        line_bot_api.reply_message(
            event.reply_token, [
                ImageSendMessage(original_content_url='https://zoozoo-monster.work' + recommend_t,
                                 preview_image_url='https://zoozoo-monster.work' + recommend_t),
                ImageSendMessage(original_content_url='https://zoozoo-monster.work' + recommend_b,
                                 preview_image_url='https://zoozoo-monster.work' + recommend_b)
            ]
        )

    elif ('Tops' in text) or ('Bottoms' in text):
        d = json.loads(queue)
        text = text.encode('ascii')
        for state in d['queue']:
            if state[u'user_id'] != event.source.user_id:
                continue
            else:
                if state['img_path'] is None or state['img_path'] == "":
                    # 連続で文字送信
                    line_bot_api.reply_message(
                        event.reply_token,
                        # TextSendMessage(text=state['cloth_type'] + 'の画像を送信後この操作が行えます')
                        TextSendMessage(text='の画像を送信後この操作が行えます')
                    )
                    return False

                else:
                    # 画像加工待ちのユーザー操作
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=text+'の画像を送信してください')
                    )
                    # Qに送る
                    # アクションステート使って
                    header = {'content-type': 'application/json'}
                    # data = {'user_id': event.source.user_id, 'cloth_type': text, 'img_path': '',
                    #         "action": 'text'}
                    data = ActionState(user_id=event.source.user_id,
                                       cloth_type=text,
                                       img_path='',
                                       action='text',
                                       processing=ActionState.processing_state['busy']).to_dict()
                    requests.post(url='http://127.0.0.1:5001', headers=header, data=json.dumps(data))
                    return True
        # 新規の正しいユーザー操作
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text+'の画像を送信してください')
        )
        # Qに送る
        header = {'content-type': 'application/json'}
        data = ActionState(user_id=event.source.user_id,
                           cloth_type=text,
                           img_path='',
                           processing='',
                           action='text').to_dict()
        requests.post(url='http://127.0.0.1:5001', headers=header, data=json.dumps(data))
        return True

    elif ':Tops' in text:
        # CSVに書く作業
        types = text.split(':')
        type_list = [str(event.source.user_id), str(types[0] + '.jpg'), str(types[1])]
        with open('clothe_types.csv', 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(type_list)
        # Userに返事
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Topsの登録完了です！')
        )

        # 白田APIに投げると
        header = {'content-type': 'application/json'}
        data = {'user_id': event.source.user_id, 'user_clothe': types[0] + '.jpg', 'user_clothe_type': 'Tops'}
        data = json.dumps(data)
        print(requests.post(url='http://127.0.0.1:8050/similarity', headers=header, data=data))  # 結果が出てくる
    elif ':Bottoms' in text:
        types = text.split(':')
        type_list = [str(event.source.user_id), str(types[0] + '.jpg'), str(types[1])]
        with open('clothe_types.csv', 'a') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(type_list)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Bottomsの登録完了です！')
        )
        header = {'content-type': 'application/json'}
        data = {'user_id': event.source.user_id, 'user_clothe': types[0] + '.jpg', 'user_clothe_type': 'Buttoms'}
        print(requests.post(url='http://127.0.0.1:8050/similarity', headers=header, data=data))
    elif u'クリア' in text:
        with open('clothe_types.csv', 'wt') as f:
            print('user,image_name,type', f)
        with open('all_pattern_of_Similarity2.csv', 'wt'):
            print('user_id,user_clothe,ranking_clothe,clothe_type,rank,similarity', f)
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='クリアしました'),
            ]
        )
    else:
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text='ご利用ありがとうございます'),
                TextSendMessage(text='このbotはあなたが登録した服の中から明日の服装を提案します'),
                TextSendMessage(text='服の登録はリッチメニューより行えます')
            ]
        )


def pick_request(image_name):
    """
    Args:
        image_name 画像の名前(パスではないです) :string

    Returns:
        画像に含まれている色ベスト3 :dictionary(json)
        ex.{"first_color":"red","second_color":"blue","third_color":"yellow"}
    """

    headers = {"Content-Type": "application/json"}
    response = requests.post('http://127.0.0.1:8050/pick', data={"image_name": image_name})
    return response.text


if __name__ == "__main__":
    app.run(debug=True)
