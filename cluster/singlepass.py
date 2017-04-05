import sys
import time
sys.path.append('..')
from numpy import *
from data import save_result
from dao.database import db

def load_data():
    
    '''载入文章向量数据'''
    table = db['papercluster']
    vectors = table.find({'valid':1})
    data = []
    for i in vectors:
        data += [i.get('vector')]
    return mat(data)

def distance(vecA, vecB):
    
    '''欧式距离计算'''
    difMat = mat(vecA) - mat(vecB)
    value = square(difMat)
    value = sum(value) 
    distance = sqrt(value)
    return distance

def cos(vecA,vecB):

    '''余弦相似度计算'''
    value = vecA * vecB.T
    cos = value/(sqrt(sum(square(vecA)))*sqrt(sum(square(vecB))))
    return cos

def singlepass(dataset,K=0.7,distMeas=cos):

    '''single-pass算法实现'''
    start_time = time.time()
    m = shape(dataset)[0]
    clusterassment = mat(zeros((m,1)))
    group_num = 0
    maxindex = 0
    for i in range(m):
        if i == 0:
            group_num = 1
            clusterassment[i] = 1
        else:
            record = [[],[]]
            for j in range(1,group_num+1):
                rows = nonzero(clusterassment[:].A==j)[0]
                maxsim = -inf
                for k in rows:
                    sim = distMeas(dataset[i,:],dataset[k,:])
                    if sim >= maxsim:
                        maxsim = sim
                record[1] += [j]
                record[0] += [maxsim]
            print(record[0])
            group_maxsim = max(record[0])
            if group_maxsim >= K:
                clusterassment[i] = record[1][record[0].index(group_maxsim)]
            else:
                group_num +=1
                clusterassment[i] = group_num
    print('聚类结果:分出%d类' %group_num)
    end_time = time.time()
    print('用时:' + str((end_time-start_time)) + ' s')
    return clusterassment

def singlepass_plus(dataset,K=0.1,distMeas=cos):

    '''single-pass改进算法实现'''
    start_time = time.time()
    m = shape(dataset)[0]
    clusterassment = mat(zeros((m,1)))
    group_num = 0
    maxindex = 0
    for i in range(m):
        if i == 0:
            group_num = 1
            clusterassment[i] = 1
        else:
            for j in range(1,group_num+1):
                rows = nonzero(clusterassment[:].A==j)[0]
                ptsInClust = dataset[rows]
                if ptsInClust.all()==False:
                    avematrix = mean(ptsInClust,axis=0)
                sim = distMeas(dataset[i,:],avematrix)
                maxsim = -inf
                if sim >= maxsim:
                    maxsim = sim
                maxindex = j
            print(maxsim)
            if maxsim >= K:
                clusterassment[i] = maxindex
            else:
                group_num +=1
                clusterassment[i] = group_num
    print('聚类结果:分出%d类' %group_num)
    end_time = time.time()
    print('用时:' + str((end_time-start_time)) + ' s')
    print(clusterassment)
    return clusterassment

def init_group():

    '''初始化新闻所属群为空'''
    table = db['papercluster']
    table.remove({'keyterm':{'$size':0}})
    table.remove({'keyterm':{'$size':1}})
    table.remove({'keyterm':{'$size':2}})
    table.remove({'keyterm':{'$size':3}})
    table.remove({'title':{'$regex':'.*公告'}})
    table.remove({'title':{'$regex':'.*摘要'}})
    papers = table.find({'valid':1})
    print(papers.count())
    for paper in papers:
        table.update({'title':paper.get('title')},{'$set':{'group':''}})

def run():
    init_group()
    dataset = load_data()
    cls = singlepass(dataset)
    save_result(cls)

if __name__ == "__main__":
    run()