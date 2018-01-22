const express = require('express');
const fs = require('fs');
const parser =  require('csv-parse/lib/sync');
const BORDER_SIMILARITY = 0.5;
const RECOMMEND_MAX_NUM = 10;
const file = './all_pattern_of_Similarity2.csv';
const fetch = require('node-fetch');
const bodyParser = require('body-parser');
const app = express();
app.use(bodyParser.json());
app.post('/', (req, res) => { 
    res.setHeader('Content-Type', 'application/json');
    let response = recommend(req.body.user_id);
    res.json(response);
});
app.listen(9000);


function recommend(userId){
  // 最終的にこれを返す
  const result = {
    "recommend":[]
  };
  let rawCSV = fs.readFileSync(file);
  let allSims = parser(rawCSV);
  let simsArray = filterArrayByUserId(allSims,userId);
  let userDict = buildUserDictBySimsArray(simsArray);
  let sortedDict = sortUserDict(userDict);
  result.recommend= [...buildRecomendationList(sortedDict)];
  return JSON.stringify(result);
}


function filterArrayByUserId(array,userId){
  return array.filter((data)=>{
    if(userId === data[0]){
      return true;
    };
  })
}

function buildUserDictBySimsArray(simsArray){
  let userObjList = [];
  simsArray.map((data)=>{
    userObjList.push({
      "userImagePath":data[1],
      "modelImagePath":data[2],
      "type":data[3],
      "rank":data[6],
      "sim":data[7]
    });
  });
  return userObjList;
}

function sortUserDict(userDict){
  let score = userDict.map((data)=>{
    data.score = (100 - parseInt(data.rank)) * parseFloat(data.sim);
  })
  userDict.sort((a,b)=>{
    return a.score < b.score ? 1 : -1;
  })
  return {
    "Tops":[
      ...userDict.filter((data)=>data.type === 'Tops')
  ],
    "Bottoms":[
      ...userDict.filter((data)=>data.type === 'Bottoms')
    ]
  };
}

function buildRecomendationList(sortedList){
  let recommend_max_num = RECOMMEND_MAX_NUM;
  if(RECOMMEND_MAX_NUM > sortedList.Tops.length 
    || RECOMMEND_MAX_NUM > sortedList.Bottoms.length){
      recommend_max_num = Math.min([sortedList.Tops.length,sortedList.Bottoms.length]);
    }
    let recommendList=[];
    console.log(sortedList)
    sortedList.Tops.some((top)=>{
      if(recommendList.length === recommend_max_num){
        return true;
      }
      sortedList.Bottoms.some((bottom)=>{
        if(top.rank === bottom.rank){
          recommendList.push({
            "Tops":top.userImagePath,
            "Bottoms":bottom.userImagePath,
            "score":top.score+bottom.score
          })
          return true;
        }
      })
    })
    return recommendList;
}