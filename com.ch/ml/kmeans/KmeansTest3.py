#!/usr/bin/python env
# coding:utf-8
from numpy import *
from matplotlib import pyplot as plt


def loadDataSet(fileName):
    datamat = []
    fr = open(fileName)
    for line in fr.readlines():
        curline = line.strip().split('\t')
        fltline = map(float, curline)
        datamat.append(fltline)
    return datamat


# 计算两个向量的距离，用的是欧式距离
def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))


# 随机生成初始的质心（ng的课说的初始方式是随机选K个点）
def randCent(dataSet, k):
    n = shape(dataSet)[1]
    # 　中心点
    centroids = mat(zeros((k, n)))
    # print "n=", n, ",k=", k,"centroids=", centroids
    for j in range(n):
        minJ = min(dataSet[:, j])
        rangeJ = float(max(array(dataSet)[:, j]) - minJ)
        centroids[:, j] = minJ + rangeJ * random.rand(k, 1)  # 填充一个四行2列的矩阵，也就是四个中心点
        # print "j=", j, ",rangeJ=", rangeJ, ",centroids=",centroids, ",minj=", minJ,",max=", max(array(dataSet)[:, j])
    return centroids


# 散点和中心点的样式
def getMarks():
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    markpoint = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
    return mark, markpoint


def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m, 2)))  # create mat to assign data points
    # to a centroid, also holds SE of each point
    centroids = createCent(dataSet, k)
    clusterChanged = True
    num = 0
    plt.figure(figsize=(19, 19))
    while clusterChanged:
        clusterChanged = False
        for i in range(m):  # for each data point assign it to the closest centroid
            minDist = inf
            minIndex = -1
            for j in range(k):
                distJI = distMeas(centroids[j, :], dataSet[i, :])
                if distJI < minDist:
                    minDist = distJI
                    minIndex = j
            print "value=",clusterAssment[i, 0] ,",minIndex=", minIndex
            if clusterAssment[i, 0] != minIndex:
                clusterChanged = True
            clusterAssment[i, :] = minIndex, minDist ** 2
        # print "count=",num,centroids
        for cent in range(k):  # recalculate centroids
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0]]  # get all the point in this cluster
            centroids[cent, :] = mean(ptsInClust, axis=0)  # assign centroid to mean

        num += 1
        if num < 9:
            show(dataSet, k, centroids, clusterAssment, m, num)
    return centroids, clusterAssment


# 显示聚类的过程
def show(dataSet, k, centroids, clusterAssment, m, num):
    plt.subplot(330 + num)
    mark, markpoint = getMarks()
    for i in xrange(m):
        markIndex = int(clusterAssment[i, 0])
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])
    for i in range(k):
        plt.plot(centroids[i, 0], centroids[i, 1], markpoint[i], markersize=12)
    plt.title(str(num))
    # plt.tight_layout()
    plt.grid()
    # plt.show()


# 展示最终结果
def Finalyshow(dataSet, k, centroids, clusterAssment):
    numSamples, dim = dataSet.shape
    show(dataSet, k, centroids, clusterAssment, numSamples, 9)
    plt.title("finaly")
    plt.tight_layout()
    plt.show()

def main():
    dataMat = mat(loadDataSet('data/testSet80.txt'))
    # print type(dataMat) # <class 'numpy.matrixlib.defmatrix.matrix'>
    k = 4
    myCentroids, clustAssing = kMeans(dataMat, k)
    print myCentroids
    Finalyshow(dataMat, k, myCentroids, clustAssing)

if __name__ == "__main__":
    main()
