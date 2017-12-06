(function recommend(){
    const fs = require('fs');
    const parser =  require('csv-parse/lib/sync');
    const BORDER_SIMILARITY = 0.5;
    const file = './all_pattern_of_Similarity.csv';

    let data = fs.readFileSync(file);

    let res = parser(data);

    //console.log(res)
    // ランクごとのリスト作成
    let rankList = {}
    for(let i=1;i<res.length-1;i++){
        if(!rankList.hasOwnProperty(res[i][4])){
            rankList[res[i][4]] = [
                {
                    'user':res[i][1],
                    'target':res[i][2],
                    'type':res[i][3],
                    'sim':res[i][5]
                }
            ];
        }
        else{
            rankList[res[i][4]].push({
                'user': res[i][1],
                'target': res[i][2],
                'type': res[i][3],
                'sim': res[i][5]
            });
        }
    }

    let preResult = {}
    for(row in rankList){
        for(data of rankList[row]){
            if (!preResult.hasOwnProperty(row)) {
                preResult[row] = {
                    tops: {},
                    bottoms:{}
                }
                if(data.type === "Tops"){
                    preResult[row].tops[data.target] = [{
                        'user': data.user,
                        'sim': data.sim
                    }]
                }else if (data.type === "Bottoms"){
                    preResult[row].bottoms[data.target] = [{
                        'user': data.user,
                        'sim': data.sim
                    }]
                }
            }
            else{
                if (data.type === "Tops") {
                    if (preResult[row].tops[data.target]){
                        preResult[row].tops[data.target].push({
                            'user': data.user,
                            'sim': data.sim
                        })
                    }
                    else{
                        preResult[row].tops[data.target]=[{
                            'user': data.user,
                            'sim': data.sim
                        }]
                    }
                } else if (data.type === "Bottoms") {
                    if (preResult[row].bottoms[data.target]) {
                        preResult[row].bottoms[data.target].push({
                            'user': data.user,
                            'sim': data.sim
                        })
                    }
                    else {
                        preResult[row].bottoms[data.target] = [{
                            'user': data.user,
                            'sim': data.sim
                        }]
                    }
                }
            }
        }
    }

    console.log(preResult['85'])
    let result = {};
    for(let row in preResult){
        result[row]={
            tops:{

            },
            bottoms:{},
            sim:1
        }
        for(let val in preResult[row].tops){
            Object.keys(preResult[row].tops).map((key)=>{
                let maxSimClName = {};
                let maxSim = Math.max(...preResult[row].tops[key].map((o) => {
                    maxSimClName[o.user] = o.sim;
                    return o.sim;
                }))
                let bestMatch = Object.keys(maxSimClName).filter((key) => {
                    return maxSimClName[key] == maxSim
                });
                result[row].tops[key] = {
                    user:bestMatch[0],
                    sim:maxSim
                };
                result[row].sim = result[row].sim * maxSim
            }) 
            Object.keys(preResult[row].bottoms).map((key) => {
                let maxSimClName = {};
                let maxSim = Math.max(...preResult[row].bottoms[key].map((o) => {
                    maxSimClName[o.user] = o.sim;
                    return o.sim;
                }))
                let bestMatch = Object.keys(maxSimClName).filter((key) => {
                    return maxSimClName[key] == maxSim
                });
                result[row].bottoms[key] = {
                    user: bestMatch[0],
                    sim: maxSim
                };
                result[row].sim = result[row].sim * maxSim
            })        
        }
    }
    console.log(result)
    let recommend=[];
    for(let row in result){
        let obj = {};
        obj[row] = result[row].sim;
        recommend.push(obj)
    }
    let recRes = recommend.filter((key)=>{
        for(let row in key){
            if(key[row]>BORDER_SIMILARITY)
                return key
            else
                return
        }
    })
    for(let row of recRes){
        for(let key in row){
            // key -> ランキング番号
            console.log("コーディネート番号"+key+"を紹介します")
            for(let index in result[key].tops){
                console.log("画像")
                // index -> モデル画像ID
                console.log(index)
                console.log("に近い画像は")
                // resul[key].top[index].user ->ユーザクローゼット
                console.log("クローゼットURL " + result[key].tops[index].user)
                console.log("です")
            }
        }
    }
})()