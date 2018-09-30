#!/usr/bin/env python
# encoding: utf-8
"""
@version: Python 2.7.6 on win10(64)
@author: BingZhen Zhou
@contact: 953129171@qq.com
@file name: water1
@time: 2018/2/21  18:58
"""
import numpy as np
import collections

class SchoolMember(object):
    '''学习成员基类'''
    member = 0

    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex
        self.enroll()

    def enroll(self):
        '注册'
        print('just enrolled a new school member [%s].' % self.name)
        SchoolMember.member += 1

    def tell(self):
        print('----%s----' % self.name)
        for k, v in self.__dict__.items():
            print(k, v)
        print('----end-----')

    def __del__(self):
        print('开除了[%s]' % self.name)
        SchoolMember.member -= 1


class Teacher(SchoolMember):
    '教师'
    def __init__(self, name, age, sex, salary, course):
        SchoolMember.__init__(self, name, age, sex)
        self.salary = salary
        self.course = course

    def teaching(self):
        print('Teacher [%s] is teaching [%s]' % (self.name, self.course))


class Student(SchoolMember):
    '学生'

    def __init__(self, name, age, sex, course, tuition):
        SchoolMember.__init__(self, name, age, sex)
        self.course = course
        self.tuition = tuition
        self.amount = 0

    def pay_tuition(self, amount):
        print('student [%s] has just paied [%s]' % (self.name, amount))
        self.amount += amount

t1 = Teacher('Wusir', 28, 'M', 3000, 'python')
t1.tell()
s1 = Student('haitao', 38, 'M', 'python', 30000)
s1.tell()
s2 = Student('lichuang', 12, 'M', 'python', 11000)
print(SchoolMember.member)
del s2

print(SchoolMember.member)

# a = [[]]*3
# # a = [[1,2],[2,3],[1,2,3],[1,2,3,4]]
# a[1] = a[1] + [2]
# print a
#
# a = np.array([1,4,3])
# print np.argwhere(a==1)[0][0]
#
#
# a,b = set([2,3])
#
# a = set([3,3,1])
# b = set([3,2,1])
# print a&b
# a = [[1,2],[2,3],[1,2,3],[1,2,3,4]]
# a = np.array(a)
# print a.flatten()
# print np.count_nonzero(np.array(a) == 4)
# a = np.array([0, 3, 0, 1, 0, 1, 2, 1, 0, 0, 0, 0, 1, 3, 4])
# print dict(zip(*np.unique(a, return_counts=True)))
# unique, counts = np.unique(a, return_counts=True)
# print counts
# print a[[2,2,1]]
# a = [0,0,5,1,2,3,2,4,1,3,4,5,1,2]
# a = np.array(a)
# print np.count_nonzero(a == 0)

# lst = []    # lst存放所谓的100万个元素
# d = collections.Counter(lst)
#
#
#
# a = [5,1,2,3,2,4,1,3,4,5,1,2]
#
# d = collections.Counter(a)
# v = np.array(d.values())
# k = np.array(d.keys())
# print k[np.where(v == 2)[0]]
# print

# print d
# for k in d:
#     print k,d[k]
#
# a = np.array([[1, 2, 3], [3, 1, 2], [2, 3, 4]])
# b = a.reshape((1,9))
# print np.unique(a, return_index=True)
# u, indices = np.unique(b, return_inverse=True)
# print indices
#


# f = lambda x: np.where(a == x)
# print map(f, range(5))
# x = [[]]*3
# x[0] = [1,2]
# x[1] = [3,4]
# x[2] = [1,4,5]
# x[0] += [3,8,2]
# print np.array(x)
# print set([1,2,3]) & set([3,4,5])