# -*- coding: utf-8 -*-
import numpy as np

#这里使用初等行变换实现广义矩阵求逆，原理是化成对角线为1的阶梯矩阵。选了列最大元
#a = np.array([[1,0,3],[0,1,2],[0,0,1]])  #该数据用于测试

######1第一步定义三个初等列变换
#先定义第k行同时乘以某个数r。
def arr_1(a,k,r):
    for i in range(a.shape[1]):
        a[k][i]=r*a[k][i]
    return a 
#print arr_1(a,2,10)       #测试一下 

#再定义第s行乘以某个数加r到另外一行k上去
def arr_2(a,k,s,r):
    for i in range(a.shape[1]):
        a[k][i]=a[k][i]+r*a[s][i]
    return a
#print arr_2(a,2,0,10)     #测试一下  

#定义某k，s两列交换位置,暂时不知道怎么用拿空数组实行两行交换，  
def arr_3(a,k,s):         #该方法有待改进
    if k==s:
        return a
    for i in range(a.shape[1]):
        a[k][i]=a[s][i]+a[k][i]
        a[s][i]=a[k][i]-a[s][i]
        a[k][i]=a[k][i]-a[s][i]
    return a
#print arr_3(a,2,1)         #测试一下
    
######2第二步实现广义矩阵求逆
#定义一个让一个矩阵amn主对角线上的元素akk变为1的函数，（采用列最大元方法）
def akk_1(a,k):
    m=a.shape[0]
    c=0
    for i in range(k,m):
        if c<np.abs(a[i][k]):
            c=np.abs(a[i][k])
    for i in range(k,m):     
        if a[i][k]==c:
            a=arr_3(a,k,i)
            break
    return arr_1(a,k,1.0/a[k][k])
#print akk_1(a,2)        #测试一下

#定义一个通过初等行变换，让每个主对角元素都变成1的函数，
#函数中间打印的目的是为了看出运算的过程
def akk_all(a):
    (m, n) = a.shape
    m=min(m,n-m)
    for i in range(m):
        a=akk_1(a,i)
        #print a,u"将第",i+1,u"个主对角上元素变为1"
        #print
        for j in range(a.shape[0]):
            if j!=i and a[j][i]!=0:
                a=arr_2(a,j,i,-a[j][i])
                #print a,u"将第",j+1,u"行,第",i+1,u"列元素打洞"
                #print
    return a   
#print akk_all(a)          #测试一下
            
#定义一个让一个矩阵右边增加一个单位矩阵，并通过变换返回一个主对角为1的矩阵            
def mat_inverse(a):
    m=a.shape[0]
    b=np.eye(m,)
    a=np.append(a,b,axis=1)
    return akk_all(a)

def mat_solve(a, b):
    (m, n) = a.shape
    r = min(m, n)
    b = [[e]for e in b]
    c = np.append(a, b, axis=1)
    for i in range(r):
        c=akk_1(c,i)
        for j in range(m):
            if j!=i and c[j][i]!=0:
                c=arr_2(c,j,i,-c[j][i])
    return c[:r, r:r+1] #c[:, r:r+1]

if __name__ == '__main__' :
    """
    a = np.array([[1,1,1],[4,0,2],[4,8,0],[4,5,5],[1,4,5]])
    n=a.shape[1]
    print a,u"原矩阵"
    print
    b=mat_inverse(a)
    print b
    print b[:,:n],u"广义单位化后的原矩阵"
    print
    print b[:,n:],u"广义逆矩阵"
    """
    a = [[1, 0], [0, 1],[2, 2]]
    b = [5, 6, 22]
    print mat_solve(np.array(a), np.array(b))