########################################
#
# 如果选择以管理员的身份进入系统, 会切换到这篇程序, 在最下面 (AdministratorStart()函数) 进入程序,
# 这部分程序是管理员所能调用的函数, 并且对应的GUI。
#
########################################


import PySimpleGUI as sg
import pandas as pd


class Administrator:
    # 管理员的登录密码, 登录时要输入
    def __init__(self):
        self.password = '12345'

    # 管理员要输入正确密码, 才能登录成功, 否则会调用 WrongPassword() 函数
    def Login(self):
        sg.theme('Dark Grey 13')
        layout = [[sg.Text('Please enter the admin password')],
                  [sg.In(size=(25, 1), enable_events=True, key='Password')],
                  [sg.Button('Okay'), sg.Button('Cancel')]]
        window = sg.Window('Admin Login', layout)
        while True:
            event, values = window.read()
            if event == 'Cancel' or event == sg.WIN_CLOSED:
                window.close()
                return
            if event == 'Okay':
                password = values['Password']
                if password == self.password:
                    window.close()
                    return 'Successful'
                else:
                    self.WrongPassword()

    # 如果密码输错, 调用这个函数, 给管理员显示提示
    def WrongPassword(self):
        sg.theme('Dark Grey 13')
        layout = [[sg.Text('Wrong Password, please try again.')],
                  [sg.Button('Okay')]]
        window = sg.Window('Wrong password', layout)
        while True:
            event, values = window.read()
            if event == 'Okay' or event == sg.WIN_CLOSED:
                window.close()
                return

    # 如果管理员在 AdministratorControl() 函数中选择批准新用户的注册, 会调用此函数,
    # 将新用户的信息加到 'CurrentUsers' 列表, 并从 'NewUsers' 列表删除
    def ApproveNewUser(self, userList, selectedUser, userInfo):
        userRow = pd.Series([userInfo[0][0], userInfo[0][1], userInfo[0][2], userInfo[0][3], userInfo[0][4]],
                            index=userList['CurrentUsers'].columns)
        userList['CurrentUsers'] = userList['CurrentUsers'].append(userRow, ignore_index=True)
        index = userList['NewUsers'].index[userList['NewUsers']['Name'] == selectedUser][0]
        userList['NewUsers'].drop(index, axis=0, inplace=True)
        return userList

    # 如果管理员在 AdministratorControl() 函数中选择不批准新用户的注册, 会调用此函数,
    # 将新用户的信息从 'NewUsers' 列表删除
    def RemoveNewUser(self, userList, selectedUser):
        index = userList['NewUsers'].index[userList['NewUsers']['Name'] == selectedUser][0]
        userList['NewUsers'].drop(index, axis=0, inplace=True)
        return userList

    # 重新命名被选的属性,
    # 提供输入框, 管理员输入新的属性名, 并点击'Okay'
    def RenameAttribute(self, articlesList, typeName, attributeName):
        sg.theme('Dark Grey 13')
        layout = [[sg.Text('Enter new name for this attribute:')],
                  [sg.In(size=(25, 1), enable_events=True, key='-Input-')],
                  [sg.Button('Okay'), sg.Button('Cancel')]]
        window = sg.Window('Rename attribute', layout)
        while True:
            event, values = window.read()
            if event == 'Cancel' or event == sg.WIN_CLOSED:
                window.close()
                return articlesList
            if event == 'Okay':
                newName = str(values['-Input-'])
                articlesList[typeName].rename(columns={attributeName: newName}, inplace=True)
                window.close()
                return articlesList

    # 删掉被选的属性,
    # 提供确认提示, 如果管理员点击'Yes', 则删掉属性
    def DeleteAttribute(self, articlesList, typeName, attributeName):
        sg.theme('Dark Grey 13')
        layout = [[sg.Text('Are you sure you want to delete this attribute?')],
                  [sg.Button('Yes'), sg.Button('No')]]
        window = sg.Window('Delete attribute', layout)
        while True:
            event, values = window.read()
            if event == 'No' or event == sg.WIN_CLOSED:
                window.close()
                return articlesList
            if event == 'Yes':
                articlesList[typeName].drop(attributeName, axis=1, inplace=True)
                window.close()
                return articlesList

    # 添加新的属性,
    # 提供输入框, 点击'Okay'后对被选择的物类添加属性
    def AddAttribute(self, articlesList, typeName):
        sg.theme('Dark Grey 13')
        layout = [[sg.Text('What attribute would you like to add?')],
                  [sg.In(size=(25, 1), enable_events=True, key='-Input-')],
                  [sg.Button('Okay'), sg.Button('Cancel')]]
        window = sg.Window('Add attribute', layout)
        while True:
            event, values = window.read()
            if event == 'Cancel' or event == sg.WIN_CLOSED:
                window.close()
                return articlesList
            if event == 'Okay':
                newName = str(values['-Input-'])
                pos = len(articlesList[typeName].columns)
                articlesList[typeName].insert(pos, newName, True)
                window.close()
                return articlesList

    # 重新命名被选的物类,
    # 提供输入框, 管理员输入新的属性名, 并点击'Okay'
    def RenameType(self, articlesList, typeName):
        sg.theme('Dark Grey 13')
        layout = [[sg.Text('Enter new name for this article type:')],
                  [sg.In(size=(25, 1), enable_events=True, key='-Input-')],
                  [sg.Button('Okay'), sg.Button('Cancel')]]
        window = sg.Window('Rename article type', layout)
        while True:
            event, values = window.read()
            if event == 'Cancel' or event == sg.WIN_CLOSED:
                window.close()
                return articlesList
            if event == 'Okay':
                newName = str(values['-Input-'])
                articlesList = {newName if k == typeName else k: v for k, v in articlesList.items()}
                window.close()
                return articlesList

    # 删掉被选的物类,
    # 提供确认提示, 如果管理员点击'Yes', 则删掉物类
    def DeleteType(self, articlesList, typeName):
        sg.theme('Dark Grey 13')
        layout = [[sg.Text('Are you sure you want to delete this article type?')],
                  [sg.Button('Yes'), sg.Button('No')]]
        window = sg.Window('Delete article type', layout)
        while True:
            event, values = window.read()
            if event == 'No' or event == sg.WIN_CLOSED:
                window.close()
                return articlesList
            if event == 'Yes':
                del articlesList[typeName]
                window.close()
                return articlesList

    # 添加新的物类,
    # 提供输入框, 点击'Okay'后创建新的物类
    def AddType(self, articlesList):
        sg.theme('Dark Grey 13')
        layout = [[sg.Text('What article type would you like to add?')],
                  [sg.In(size=(25, 1), enable_events=True, key='-Input-')],
                  [sg.Button('Okay'), sg.Button('Cancel')]]
        window = sg.Window('Add article type', layout)
        while True:
            event, values = window.read()
            if event == 'Cancel' or event == sg.WIN_CLOSED:
                window.close()
                return articlesList
            if event == 'Okay':
                newName = str(values['-Input-'])
                articlesList[newName] = pd.DataFrame(columns=['Name', 'Explanation', 'Location', 'Phone Number',
                                                              'Email'])
                window.close()
                return articlesList


# 管理员主页面的布局
def GetLayoutAdminControl(articlesList, userList):
    sg.theme('Dark Grey 13')
    left_column = [[sg.Text('List of new users:')],
                   [sg.Listbox(values=userList['NewUsers']['Name'], enable_events=True, size=(40, 20), key='UserList')],
                   [sg.Text('List of article types:')],
                   [sg.Listbox(values=list(articlesList.keys()), enable_events=True, size=(40, 20), key='-TypesList-')],
                   [sg.Button('Rename', key='RenameType'), sg.Button('Delete', key='DeleteType'),
                    sg.Button('Add', key='AddType')]]
    right_column = [[sg.Text('New user information')],
                    [sg.Table(values=[], headings=list(userList['NewUsers'].columns),
                              enable_events=True, num_rows=1, auto_size_columns=True, key='UserInfo')],
                    [sg.Button('Approve'), sg.Button('Remove')],
                    [sg.Text('List of attributes')],
                    [sg.Listbox(values=[], enable_events=True, size=(40, 20), key='-Attributes-')],
                    [sg.Button('Rename', key='RenameAttr'), sg.Button('Delete', key='DeleteAttr'),
                     sg.Button('Add', key='AddAttr')]]
    layout = [[sg.Column(left_column), sg.VSeparator(), sg.Column(right_column)]]
    return layout


# 管理员程序的任务管理模块,
# 根据上面的函数 (GetLayoutAdminControl()) 创造GUI, 然后根据管理员的选择调用对应的函数
def AdministratorControl(admin, articlesList, userList):
    typeName = ''
    attributeName = ''
    selectedUser = ''
    userInfo = list()
    layout = GetLayoutAdminControl(articlesList, userList)
    window = sg.Window('Article Exchange', layout)
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-TypesList-':
            typeName = str(values['-TypesList-'])[2:-2]    # [2:-2] causes from ['Food'] to Food
            window['-Attributes-'].update(articlesList[typeName].columns)
        if event == '-Attributes-':
            attributeName = str(values['-Attributes-'])[2:-2]
        if event == 'RenameAttr':
            articlesList = admin.RenameAttribute(articlesList, typeName, attributeName)
            window['-Attributes-'].update(articlesList[typeName].columns)
        if event == 'DeleteAttr':
            articlesList = admin.DeleteAttribute(articlesList, typeName, attributeName)
            window['-Attributes-'].update(articlesList[typeName].columns)
        if event == 'AddAttr':
            articlesList = admin.AddAttribute(articlesList, typeName)
            window['-Attributes-'].update(articlesList[typeName].columns)
        if event == 'RenameType':
            articlesList = admin.RenameType(articlesList, typeName)
            window['-TypesList-'].update(list(articlesList.keys()))
        if event == 'DeleteType':
            articlesList = admin.DeleteType(articlesList, typeName)
            window['-TypesList-'].update(list(articlesList.keys()))
        if event == 'AddType':
            articlesList = admin.AddType(articlesList)
            window['-TypesList-'].update(list(articlesList.keys()))
        if event == 'UserList':
            selectedUser = str(values['UserList'])[2:-2]
            userInfo = userList['NewUsers'][userList['NewUsers']['Name'] == selectedUser]
            userInfo = (userInfo.to_numpy()).tolist()
            window['UserInfo'].update(userInfo)
        if event == 'Approve':
            userList = admin.ApproveNewUser(userList, selectedUser, userInfo)
            window['UserList'].update(userList['NewUsers']['Name'])
            window['UserInfo'].update([])
        if event == 'Remove':
            userList = admin.RemoveNewUser(userList, selectedUser)
            window['UserList'].update(userList['NewUsers']['Name'])
            window['UserInfo'].update([])
    return articlesList, userList


# 这里进入管理员的子系统,
# 首先创建管理员对象, 然后让其登录,
# 登录后才能进入管理员程序的任务管理模块。
def AdministratorStart(articlesList, userList):
    admin = Administrator()
    loginStatus = admin.Login()
    if loginStatus == 'Successful':
        articlesList, userList = AdministratorControl(admin, articlesList, userList)
    return articlesList, userList
