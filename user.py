########################################
#
# 如果选择以普通用户的身份进入系统, 会切换到这篇程序, 在最下面 (UserStart()函数) 进入程序,
# 这部分程序是普通用户所能调用的函数, 并且对应的GUI。
#
########################################


import PySimpleGUI as sg
import pandas as pd


class User:
    # 初始化用户的属性
    def __init__(self):
        self.name = 'John'
        self.password = 'aaaa'
        self.address = 'Minhang'
        self.phoneNumber = '132'
        self.email = 'john@sjtu.edu.cn'

    # 用户输入自己的用户名和密码,
    # 当用户名不在 'CurrentUsers' 列表中, 调用 UserNotFound() 函数,
    # 当用户名在列表中, 但密码错误, 调用 WrongPassword() 函数,
    # 当用户密码正确, 登录成功,
    # 用户也可以选择不登录而点击注册按钮
    def Login(self, userList):
        sg.theme('Dark Grey 13')
        layout = [[sg.Text('Please enter your name and password.')],
                  [sg.Text('Name:'), sg.In(size=(25, 1), enable_events=True, key='Name')],
                  [sg.Text('Password:'), sg.In(size=(25, 1), enable_events=True, key='Password')],
                  [sg.Button('Okay'), sg.Button('Cancel'), sg.Button('Sign Up')]]
        window = sg.Window('Login', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel':
                window.close()
                return
            if event == 'Sign Up':
                window.close()
                return 'Sign Up'
            if event == 'Okay':
                name = str(values['Name'])
                password = str(values['Password'])
                if name in userList['CurrentUsers']['Name'].values:
                    index = userList['CurrentUsers'].index[userList['CurrentUsers']['Name'] == name][0]
                    if password == str(userList['CurrentUsers'].iat[index, 1]):
                        self.name = name
                        self.password = password
                        self.address = userList['CurrentUsers'].iat[index, 2]
                        self.phoneNumber = userList['CurrentUsers'].iat[index, 3]
                        self.email = userList['CurrentUsers'].iat[index, 4]
                        window.close()
                        return 'Successful'
                    else:
                        self.WrongPassword()
                else:
                    self.UserNotFound()

    # 给用户显示提示
    def WrongPassword(self):
        sg.theme('Dark Grey 13')
        layout = [[sg.Text('Wrong Password, please try again, or click on sign up if you want to '
                           'make an account')],
                  [sg.Button('Okay')]]
        window = sg.Window('Wrong password', layout)
        while True:
            event, values = window.read()
            if event == 'Okay' or event == sg.WIN_CLOSED:
                window.close()
                return

    # 给用户显示提示
    def UserNotFound(self):
        sg.theme('Dark Grey 13')
        layout = [[sg.Text('No user found by this name, please try again, or click on sign up if you want to make '
                           'an account')],
                  [sg.Button('Okay')]]
        window = sg.Window('User not found', layout)
        while True:
            event, values = window.read()
            if event == 'Okay' or event == sg.WIN_CLOSED:
                window.close()
                return

    # 用户选择注册时, 会调用这个函数,
    # 提供五个输入框, 用户将自己的个人信息填入, 并点击'Okay',
    # 将用户的信息添加到 'NewUsers' 列表中, 等待管理员批准
    def SignUp(self, userList):
        sg.theme('Dark Grey 13')
        layout = [[sg.Text('Please enter your information.')],
                  [sg.Text('Name'), sg.In(size=(25, 1), enable_events=True, key='Name')],
                  [sg.Text('Password'), sg.In(size=(25, 1), enable_events=True, key='Password')],
                  [sg.Text('Address'), sg.In(size=(25, 1), enable_events=True, key='Address')],
                  [sg.Text('Phone Number'), sg.In(size=(25, 1), enable_events=True, key='Phone')],
                  [sg.Text('Email'), sg.In(size=(25, 1), enable_events=True, key='Email')],
                  [sg.Button('Okay'), sg.Button('Cancel')]]
        window = sg.Window('Sign Up', layout)
        while True:
            event, values = window.read()
            if event == 'Cancel' or event == sg.WIN_CLOSED:
                window.close()
                return userList
            if event == 'Okay':
                row = pd.Series([values['Name'], values['Password'], values['Address'], values['Phone'],
                                 values['Email']], index=['Name', 'Password', 'Address', 'Phone Number', 'Email'])
                userList['NewUsers'] = userList['NewUsers'].append(row, ignore_index=True)
                window.close()
                self.SignUpFinished()
                return userList

    # 给用户显示提示
    def SignUpFinished(self):
        sg.theme('Dark Grey 13')
        layout = [[sg.Text('Your application has been successfully submitted, please wait for approval.')],
                  [sg.Button('Okay')]]
        window = sg.Window('Sign up successful', layout)
        while True:
            event, values = window.read()
            if event == 'Okay' or event == sg.WIN_CLOSED:
                window.close()
                return

    # 用户选择添加物品时, 调用这个函数,
    # 给用户提供几个输入框, 填入物品信息 (输入框的个数根据物类的属性判断),
    # 将填入的信息添加到对应的物品列表 (自动填入用户的地址、手机号、邮箱)
    def AddArticle(self, articlesList, typeName, columns):
        sg.theme('Dark Grey 13')
        layout = [[]]
        if len(columns) == 5:
            layout = [[sg.Text('Please type in the article information: ')],
                      [sg.Text('Article name: '), sg.In(size=(25, 1), enable_events=True, key='Name')],
                      [sg.Text('Article description: '), sg.In(size=(25, 1), enable_events=True, key='Description')],
                      [sg.Button('Okay'), sg.Button('Cancel')]]
        if len(columns) == 6:
            layout = [[sg.Text('Please type in the article information: ')],
                      [sg.Text('Article name: '), sg.In(size=(25, 1), enable_events=True, key='Name')],
                      [sg.Text('Article description: '), sg.In(size=(25, 1), enable_events=True, key='Description')],
                      [sg.Text(columns[5]), sg.In(size=(25, 1), enable_events=True, key='Six')],
                      [sg.Button('Okay'), sg.Button('Cancel')]]
        if len(columns) == 7:
            layout = [[sg.Text('Please type in the article information: ')],
                      [sg.Text('Article name: '), sg.In(size=(25, 1), enable_events=True, key='Name')],
                      [sg.Text('Article description: '), sg.In(size=(25, 1), enable_events=True, key='Description')],
                      [sg.Text(columns[5]), sg.In(size=(25, 1), enable_events=True, key='Six')],
                      [sg.Text(columns[6]), sg.In(size=(25, 1), enable_events=True, key='Seven')],
                      [sg.Button('Okay'), sg.Button('Cancel')]]
        if len(columns) == 8:
            layout = [[sg.Text('Please type in the article information: ')],
                      [sg.Text('Article name: '), sg.In(size=(25, 1), enable_events=True, key='Name')],
                      [sg.Text('Article description: '), sg.In(size=(25, 1), enable_events=True, key='Description')],
                      [sg.Text(columns[5]), sg.In(size=(25, 1), enable_events=True, key='Six')],
                      [sg.Text(columns[6]), sg.In(size=(25, 1), enable_events=True, key='Seven')],
                      [sg.Text(columns[7]), sg.In(size=(25, 1), enable_events=True, key='Eight')],
                      [sg.Button('Okay'), sg.Button('Cancel')]]
        window = sg.Window('Add article', layout)
        while True:
            event, values = window.read()
            if event == 'Cancel' or event == sg.WIN_CLOSED:
                window.close()
                return articlesList
            if event == 'Okay':
                articleName = values['Name']
                description = values['Description']
                newArticle = pd.Series()
                if len(columns) == 5:
                    newArticle = pd.Series([articleName, description, self.address, self.phoneNumber, self.email],
                                           index=columns)
                if len(columns) == 6:
                    newArticle = pd.Series([articleName, description, self.address, self.phoneNumber, self.email,
                                            values['Six']], index=columns)
                if len(columns) == 7:
                    newArticle = pd.Series([articleName, description, self.address, self.phoneNumber, self.email,
                                            values['Six'], values['Seven']], index=columns)
                if len(columns) == 8:
                    newArticle = pd.Series([articleName, description, self.address, self.phoneNumber, self.email,
                                            values['Six'], values['Seven'], values['Eight']], index=columns)
                articlesList[typeName] = articlesList[typeName].append(newArticle, ignore_index=True)
                window.close()
                return articlesList

    # 如果用户选择删掉物品, 会调用这个函数,
    # 首先判断被选物品是否由当前用户被添加（通过比较手机号及邮箱）,
    # 如果物品是当前用户的物品, 删掉,
    # 如果物品不是当前用户的物品, 调用UnableToDelete()函数
    def DeleteArticle(self, articlesList, typeName, index):
        if str(self.phoneNumber) == str(articlesList[typeName].iat[index, 3]) and \
                str(self.email) == str(articlesList[typeName].iat[index, 4]):
            sg.theme('Dark Grey 13')
            layout = [[sg.Text('Are you sure you want to delete this article?')],
                      [sg.Button('Yes'), sg.Button('No')]]
            window = sg.Window('Delete article', layout)
            while True:
                event, values = window.read()
                if event == 'No' or event == sg.WIN_CLOSED:
                    window.close()
                    return articlesList
                if event == 'Yes':
                    articlesList[typeName].drop(index, axis=0, inplace=True)
                    window.close()
                    return articlesList
        else:
            self.UnableToDelete()
            return articlesList

    # 如果已判断用户想删掉的物品不是自己的物品, 调用这个函数,
    # 给用户显示提示
    def UnableToDelete(self):
        sg.theme('Dark Grey 13')
        layout = [[sg.Text('This article belongs to someone else, please contact them to delete it.')],
                  [sg.Button('Okay')]]
        window = sg.Window('Unable to delete', layout)
        while True:
            event, values = window.read()
            if event == 'Okay' or event == sg.WIN_CLOSED:
                window.close()
                return

    # 如果管理员选择查找物品, 会调用此函数,
    # 当被查找物品在列表中, 显示所有对应物品,
    # 当被查找物品不在列表中, 调用ArticleNotFound()函数
    def SearchArticle(self, articlesList, typeName, columns, search):
        if search in articlesList[typeName]['Name'].values:
            foundArticles = articlesList[typeName].loc[articlesList[typeName]['Name'] == search]
            foundArticles = (foundArticles.to_numpy()).tolist()
            sg.theme('Dark Grey 13')
            layout = [[sg.Text('Article found')],
                      [sg.Table(values=foundArticles, headings=columns, justification='left', key='Table',
                                num_rows=5, auto_size_columns=True)],
                      [sg.Button('Okay')]]
            window = sg.Window('Article found', layout)
            while True:
                event, values = window.read()
                if event == sg.WIN_CLOSED or event == 'Okay':
                    window.close()
                    return
        else:
            self.ArticleNotFound()
            return

    # 如果没有查到物品, 调用这个函数,
    # 给用户显示提示
    def ArticleNotFound(self):
        sg.theme('Dark Grey 13')
        layout = [[sg.Text('Article not found')],
                  [sg.Button('Okay')]]
        window = sg.Window('Article not found', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Okay':
                window.close()
                return

    # 显示被选物类的物品列表,
    # 用户可以选择添加物品、查找物品（已经提供输入框）或者删掉物品, 根据其选择调用对应的函数
    def ShowArticles(self, articlesList, typeName):
        sg.theme('Dark Grey 13')
        columns = list(articlesList[typeName].columns)
        articles = (articlesList[typeName].to_numpy()).tolist()
        index = -1
        layout = [[sg.Text('List of Articles: ')],
                  [sg.Table(values=articles, headings=columns, enable_events=True,
                            justification='left', key='Table', num_rows=30, auto_size_columns=True)],
                  [sg.Button('Delete article'), sg.Button('Add article'), sg.Text('Search for article:'),
                   sg.In(size=(25, 1), enable_events=True, key='SearchName'), sg.Button('Search'), sg.Button('Exit')]]
        window = sg.Window('Article Exchange', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                window.close()
                break
            if event == 'Add article':
                articlesList = self.AddArticle(articlesList, typeName, columns)
                articles = (articlesList[typeName].to_numpy()).tolist()
                window['Table'].update(articles)
            if event == 'Search':
                search = values['SearchName']
                self.SearchArticle(articlesList, typeName, columns, search)
            if event == 'Table':
                index = int(values['Table'][0])
            if event == 'Delete article':
                articlesList = self.DeleteArticle(articlesList, typeName, index)
                articles = (articlesList[typeName].to_numpy()).tolist()
                window['Table'].update(articles)
        return articlesList

    # 显示物类列表,
    # 用户可以选择自己想看的物类, 点击'Select'时会调用ShowArticles()函数, 显示相应的物品列表
    def SelectArticleType(self, articlesList):
        sg.theme('Dark Grey 13')
        layout = [[sg.Text('List of article types')],
                  [sg.Listbox(values=list(articlesList.keys()), enable_events=True, size=(40, 20), key='TypesList')],
                  [sg.Button('Select')]]
        typeName = ''
        window = sg.Window('Article Exchange', layout)
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
            if event == 'TypesList':
                typeName = str(values['TypesList'])[2:-2]
            if event == 'Select':
                articlesList = self.ShowArticles(articlesList, typeName)
        return articlesList


# 这里进入普通用户的子系统,
# 首先创建用户对象, 然后让其登录,
# 在登录页面可以选择不登录而注册, 此时这里会调用注册函数,
# 登录后才能看到物类列表
def UserStart(articlesList, userList):
    user = User()
    loginStatus = user.Login(userList)
    if loginStatus == 'Sign Up':
        userList = user.SignUp(userList)
    if loginStatus == 'Successful':
        articlesList = user.SelectArticleType(articlesList)
    return articlesList, userList
