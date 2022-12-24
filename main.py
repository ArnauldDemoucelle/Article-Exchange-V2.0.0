########################################
#
# “你帮我助”软件
# 物品交换软件
# 可以以管理员的身份或者以普通用户的身份登录系统, 新用户也可以注册,
# 管理员登录后可以批准新用户的注册申请, 也可以添加和修改物品类型,
# 普通用户登录后可以按照物品类型显示物品列表, 也可以查找物品的信息, 添加自己的物品并删除自己已添加的物品
#
# Written by Arnauld Demoucelle
# Version 2.0.0
# December 2022
#
########################################


import PySimpleGUI as sg
import pandas as pd
import os
import sys

import administrator
import user


# 把物品列表从数据库（Excel表格）导入到DataFrame,
# 如果数据库（Excel表格）存在, 用其数据,
# 如果数据库不存在, 创建空的DataFrame, 并创建Excel表格。
def GetArticlesData():
    storageFile = "ArticlesData.xlsx"
    if os.path.exists(storageFile):
        articlesList = pd.read_excel(storageFile, sheet_name=None)
        return articlesList
    else:
        df = pd.DataFrame(columns=['Name', 'Explanation', 'Location', 'Phone Number', 'Email'])
        df.to_excel(storageFile, sheet_name='Articles', columns=['Name', 'Explanation', 'Location', 'Phone Number',
                                                                 'Email'], index=False)
        articlesList = pd.read_excel(storageFile, sheet_name=None)
        return articlesList


# 把用户列表从数据库（Excel表格）导入到DataFrame,
# 如果数据库（Excel表格）存在, 用其数据,
# 如果数据库不存在, 创建空的DataFrame, 并创建Excel表格。
def GetUserData():
    storageFile = 'UserData.xlsx'
    if os.path.exists(storageFile):
        userList = pd.read_excel(storageFile, sheet_name=None)
        return userList
    else:
        df1 = pd.DataFrame(columns=['Name', 'Password', 'Address', 'Phone Number', 'Email'])
        df2 = df1.copy()
        writer = pd.ExcelWriter('UserData.xlsx')
        df1.to_excel(writer, index=False, sheet_name='CurrentUsers')
        df2.to_excel(writer, index=False, sheet_name='NewUsers')
        writer.save()
        userList = pd.read_excel(storageFile, sheet_name=None)
        return userList


# 让用户选择自己以哪种身份登录系统：普通用户或者管理员,
# GUI 有两个按钮, 分别对应用户和管理员。
def ChooseIdentity():
    sg.theme('Dark Grey 13')
    layout = [[sg.Text('What identity would you like to enter the system as?')],
              [sg.Button('User'), sg.Button('Administrator')]]
    window = sg.Window('Article Exchange', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            return
        if event == 'User':
            window.close()
            return 'User'
        if event == 'Administrator':
            window.close()
            return 'Admin'


# 将物品列表和用户列表分别保存到对应的Excel表格
def SaveData(articlesList, userList):
    # Save articlesList
    types = list(articlesList.keys())
    amount = len(types)
    writer = pd.ExcelWriter('ArticlesData.xlsx')
    for i in range(0, amount):
        articlesList[types[i]].to_excel(writer, index=False, sheet_name=types[i])
    writer.save()
    # Save userList
    writer = pd.ExcelWriter('UserData.xlsx')
    userList['CurrentUsers'].to_excel(writer, index=False, sheet_name='CurrentUsers')
    userList['NewUsers'].to_excel(writer, index=False, sheet_name='NewUsers')
    writer.save()


# 这是系统的任务管理模块,
# 首先调用ChooseIdentity()函数, 让用户选择自己是管理员还是普通用户,
# 然后调用下载数据的两个函数 (GetArticlesData() 和 GetUserData()), 以便得到物品列表和用户列表,
# 如果用户是普通用户, 那么切换到user.py, 如果用户是管理员, 那么切换到administrator.py,
# 最后, 调用SaveData()函数, 保存所有的数据, 并退出系统。
def Control():
    identity = ChooseIdentity()
    articlesList = GetArticlesData()
    userList = GetUserData()
    if identity == 'User':
        articlesList, userList = user.UserStart(articlesList, userList)
    if identity == 'Admin':
        articlesList, userList = administrator.AdministratorStart(articlesList, userList)
    SaveData(articlesList, userList)
    sys.exit()


# 程序开始运行时首先调用Control()函数（系统的任务管理模块）。
if __name__ == "__main__":
    Control()
