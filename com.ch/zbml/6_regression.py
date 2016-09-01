#!/usr/bin/ env python
# coding=utf-8


# 回归code
def calcCoefficient(data,listA,listW,listLostFunction):
    N = len(data[0]) #维度
    w = [0 for i in range(N)]
    wNew = [0 for i in range(N)]
    g = [0 for i in range(N)]

    times=0
    alpha = 100 #学习率随意初始化
    while times <10000:
        j =0
        while j<N:
            g[j]=gradient(data,w,j)
            j += 1
        normalize(g) #正则化梯度
        alpha = calcAlpha(w,g,alpha,data)
        numberProduct(alpha,g,wNew)

        print "times,alpha,fw,w,g:\t",times,alpha,fw(w,data),w,g
        if isSame(w,wNew):
            break
        assign2(w,wNew) #更新权值
        times += 1

        listA.append(alpha)
        listW.append(assign(w))
        listLostFunction.append(fw(w,data))
    return w


#学习率code

# w为当前值，g 当前梯度方向  a 当前学习率  data 数据
def calcAlpha(w,g,a,data):
     c1 = 0.3
     now =fw(w,data)
     wNext = assign(w)
     numberProduct(a,g,wNext)
     next = fw(wNext,data)

     #寻找足够大的a，使得h(a)>0
     count =30
     while next < now:
         a *= 2
         wNext = assign(w)
         numberProduct(a, g, wNext)
         next = fw(wNext, data)
         count -= 1
         if count ==0:
             break

     #寻找合适的学习率
     count = 50
     while next > now - c1*a*dotProduct(g,g):
         a /=2
         wNext=assign(w)
         numberProduct(a, g, wNext)
         next = fw(wNext, data)

         count -= 1
         if count == 0:
             break
     return a


