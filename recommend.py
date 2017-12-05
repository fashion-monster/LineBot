# coding: UTF-8
from pprint import pprint
import csv

# generate dictionaly
def generate_each_rank_dict_by_user_id(row):
    '''
    {
        '1':[
                {...},
                {...},
            ],
        '2':[
                {...},
                {...},
        ]
    }
    '''

    if row[0] != user_id :
        return False
    rank = row[4]
    if rank in sim_dict :
        tmp_dict = {
            'type':row[3],
            'user_clothes':row[1],
            'rank_clothes':row[2],
            'similarity':round(float(row[5]),5)
        }
        sim_dict[rank].append(tmp_dict)
    else :
        sim_dict[row[4]] = [{
            'type':row[3],
            'user_clothes':row[1],
            'rank_clothes':row[2],
            'similarity':round(float(row[5]),5)
        }]


def get_best_clothes_by_rank(rank_list,self_rank):

    '''
        {
        'tops':[{
                'rank_clothes':'',
                'user_clothes':'',
                'similarity':0}],
        'bottoms':[{
                'rank_clothes':'',
                'user_clothes':'',
                'similarity':0}],
        'similarity':0
    }
    '''

    rank = {
        'Tops':[],
        'Bottoms':[],
        'similarity':1
    }

    for row in rank_list:
        if rank[row['type']] == [] and row['similarity'] != 0:
            rank[row['type']] = [{
                'rank_clothes':row['rank_clothes'],
                'user_clothes':row['user_clothes'],
                'similarity':row['similarity']
            }]
        if any(d['rank_clothes'] != row['rank_clothes'] for d in rank[row['type']]) and row['similarity'] != 0:
            rank[row['type']].append({
                'rank_clothes':row['rank_clothes'],
                'user_clothes':row['user_clothes'],
                'similarity':row['similarity']
            })
        
        else:
            for item in rank[row['type']]:
               if item['rank_clothes'] == row['rank_clothes'] and item['user_clothes'] != row['user_clothes'] and item['similarity'] < row['similarity']:
                    item['user_clothes'] = row['user_clothes']
                    item['similarity'] = row['similarity']
        
    for row in rank['Tops']:
        rank['similarity'] = rank['similarity']*row['similarity']
    for row in rank['Bottoms']:
        rank['similarity'] = rank['similarity']*row['similarity']
    return {self_rank : rank}

with open('all_pattern_of_Similarity.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)

    user_id = 'U4fce6cc2cc3530ae2f4b7ca0609edd40'
    sim_dict = {}
    most_sim = []

    for row in reader:
        generate_each_rank_dict_by_user_id(row)

    for row in sim_dict:
        most_sim.append(get_best_clothes_by_rank(sim_dict[row],row))


    pprint(most_sim)