const express = require('express');
const request = require('request');
const bodyParser = require('body-parser');
// STATE CONST VALUE
const PROCESSING_STATE_BUSY = 'busy';
const PROCESSING_STATE_EMPTY = 'empty';
// ACTION CONST VALUE
const ACTION_IMAGE_PROCESSING ='similarity';
const ACTION_MESSAGE_TEXT = 'text';
const ACTION_MESSAGE_IMAGE = 'image';
// HOST CONST VALUE
const ORIGIN_HOST = 'localhost:5001';
const GLOBAL_HOST = 'localhost:5000';
const IMAGE_PROCESSING_HOST = 'localhost:8050';
// HTTP REQUEST OPTIONS
const header = {
  'Content-Type':'application/json'
};
const options = {
  'method':'POST',
  'headers':header
};
//
const app = express();
const queue = {queue:[]};
app.use(bodyParser());
// 現在のキューを返すと嬉しい
app.get('/', (req, res)=>{ 
    res.setHeader('Content-Type','application/json');
    res.json(JSON.stringify(queue));
});

// 俗にいうエンドポイント　API仕様はここで読め
app.post('/',(req,res)=>{
  // エラーだろうが何だろうがOKと返ってくるので気をつけろ
  res.setHeader('Content-Type', 'application/json');
  res.json('{"message":"OK"}');
  // 実際のAPI部分
  if(req.body.action === ACTION_MESSAGE_TEXT){
    // TopsかBottomsのメッセージがきた時、queueに新規で追加
    
    queue.queue.push({
        "user_id":req.body.user_id,
        "cloth_type":req.body.cloth_type,
        "img_path":null,
        "processing":PROCESSING_STATE_EMPTY,
        "action":req.body.action
      })
    console.log("text:")
    console.log(queue.queue)
    }
    else if(req.body.action === ACTION_MESSAGE_IMAGE){
      // 画像が送られてきたら、送信者の最新のqueueに画像のパスを追加する
      for(let i = queue.queue.length-1;i>=0;i--){
        if(queue.queue[i].user_id === req.body.user_id){
          queue.queue[i].img_path = req.body.img_path;
          break;
        }
      }
      if(queue.queue.length === 1){
        // 画像パス追加後キューが一件だったら画像処理サーバーにリクエストを投げる
        queue.queue[0].processing = PROCESSING_STATE_BUSY;
        request({
            ...options,
            url:`http://${ORIGIN_HOST}/${ACTION_IMAGE_PROCESSING}`,
            body:{...queue.queue[0]}
          },()=>{
          console.log("processing request Done");
        })
      }
      console.log("image:")
      console.log(queue.queue)
    }
    else if(req.body.action === ACTION_IMAGE_PROCESSING){
      // 画像処理が終了した時
      queue.queue.shift();
      if(queue.queue.length !== 0){
        queue.queue[0].processing = PROCESSING_STATE_BUSY;
        request({
          ...options,
          url:`http://${ORIGIN_HOST}/${ACTION_IMAGE_PROCESSING}`,
          body:{...queue.queue[0]}
        },()=>{
          console.log("processing request Done");
        });
      }
      console.log("processing:")
      console.log(queue.queue)
    }
  })
app.listen(5001);