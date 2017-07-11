# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ui_zhihu import Ui_Form
from ui_zhihu_registeraccount import Ui_Form_RegisterAccount
from ui_zhihu_queryaccount import Ui_Form_QueryAccount 
from ui_zhihu_addtask import Ui_Form_AddTask
from ui_zhihu_updatetask import Ui_Form_UpdateTask
from ui_zhihu_querytask import Ui_Form_QueryTask
from sqlutil import SqlUtil
from taskutil import TaskUtil
from register import Register
from register_avatar import Register_Avatar
from shenhua import Shenhua
from adsl import Adsl
import time
import random
import threading
import webbrowser
import sys
import os
import chardet

class FormBase(QMainWindow, Ui_Form):

    def __init__(self, parent=None):
        super(FormBase, self).__init__(parent)
        self.setupUi(self)


class Form(FormBase):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        
        self.addTaskForm = None
        self.addTaskWidget = None
        
        self.updateTaskForm = None
        self.updateTaskWidget = None
        
        self.queryTaskForm = None
        self.queryTaskWidget = None
        
        
        self.registerAccountWidget = None
        self.registerAccountForm = None
        self.registerAccountThread = None
        
        self.queryAccountForm = None
        self.queryAccountWidget = None
        
        
        self.sqlUtil = SqlUtil()
        
        self.init()
        
        #self.tabWidget.tabBarClicked.connect(self.tabBarClicked)
        self.pushButton_selectAllTask.clicked.connect(self.selectAllTask)
        self.pushButton_addTask.clicked.connect(self.showAddTaskForm)
        self.pushButton_deleteTask.clicked.connect(self.deleteTask)
        self.pushButton_updateTask.clicked.connect(self.showUpdateTaskForm)
        self.pushButton_queryTask.clicked.connect(self.showQueryTaskForm)
        
        self.pushButton_startTask.clicked.connect(self.startTask)
        self.pushButton_stopTask.clicked.connect(self.stopTask)
        self.pushButton_stopTask.setDisabled(True)
        
        
        self.pushButton_selectAllAccount.clicked.connect(self.selectAllAccount)
        self.pushButton_importAccount.clicked.connect(self.importAccount)
        self.pushButton_exportAccount.clicked.connect(self.exportAccount)
        self.pushButton_registerAccount.clicked.connect(self.showRegisterAccountForm)
        self.pushButton_deleteAccount.clicked.connect(self.deleteAccount)
        
        self.pushButton_queryAccount.clicked.connect(self.showQueryAccountForm)
        
        self.comboBox_accountStatus.addItems(['正常','异常', '已导出'])
        self.pushButton_updateAccount.clicked.connect(self.updateAccount)
        
       
        
        self.radioButton_benjiwangluo.toggled.connect(self.benjiwangluoToggled)
        self.radioButton_dongtaiip.toggled.connect(self.dongtaiipToggled)
        self.radioButton_adslbohao.toggled.connect(self.adslbohaoToggled)
        
        
        self.pushButton_damadenglu.clicked.connect(self.damaDenglu)
        self.pushButton_damazhuce.clicked.connect(self.damaZhuce)
        self.pushButton_jiemadenglu.clicked.connect(self.jiemaDenglu)
        self.pushButton_jiemazhuce.clicked.connect(self.jiemaZhuce)
        
        
        self.tableWidget_task.setColumnWidth(0, 50)
        self.tableWidget_task.setColumnWidth(1, 80)
        self.tableWidget_task.setColumnWidth(2, 380)
        self.tableWidget_task.setColumnWidth(3, 60)
        self.tableWidget_task.setColumnWidth(4, 60)
        self.tableWidget_task.setColumnWidth(5, 60)
        self.tableWidget_task.setColumnWidth(6, 80)
        self.tableWidget_task.setColumnWidth(7, 100)
        self.tableWidget_task.setColumnWidth(8, 100)
        self.tableWidget_task.setColumnWidth(9, 100)
        self.tableWidget_task.setColumnWidth(10, 100)
        self.tableWidget_task.setColumnWidth(11, 200)
        
        self.tableWidget_task.hideColumn(12)
        
        
        tasks = self.sqlUtil.select_task()
        taskCount = len(tasks)
        self.tableWidget_task.setRowCount(taskCount)
        i = 0
        for row in tasks:
            #print('id = '+ str(row[0]))
            select = QTableWidgetItem()
            select.setCheckState(Qt.Unchecked)
            taskIdItem = QTableWidgetItem(str(row[0]))
            taskTypeItem = QTableWidgetItem(row[1])
            taskUrlItem = QTableWidgetItem(row[2])
            taskCountItem = QTableWidgetItem(row[3])
            taskBeginCountItem = QTableWidgetItem(row[4])
            taskCurrentCountItem = QTableWidgetItem(row[5])
            taskStatusItem = QTableWidgetItem(row[6])
            taskOrderItem = QTableWidgetItem(row[7])
            taskIntervalItem = QTableWidgetItem(row[8])
            taskCustomerItem = QTableWidgetItem(row[9])
            taskDeliverItem = QTableWidgetItem(row[10])
            taskRemarkItem = QTableWidgetItem(row[11])
            
            
            self.tableWidget_task.setItem(i, 0, select)
            self.tableWidget_task.setItem(i, 1, taskTypeItem)  
            self.tableWidget_task.setItem(i, 2, taskUrlItem)
            self.tableWidget_task.setItem(i, 3, taskCountItem)
            self.tableWidget_task.setItem(i, 4, taskBeginCountItem)
            self.tableWidget_task.setItem(i, 5, taskCurrentCountItem)
            self.tableWidget_task.setItem(i, 6, taskStatusItem)
            self.tableWidget_task.setItem(i, 7, taskOrderItem)
            self.tableWidget_task.setItem(i, 8, taskIntervalItem)  
            self.tableWidget_task.setItem(i, 9, taskCustomerItem)
            self.tableWidget_task.setItem(i, 10, taskDeliverItem)
            self.tableWidget_task.setItem(i, 11, taskRemarkItem)
            self.tableWidget_task.setItem(i, 12, taskIdItem)
            
            i += 1
        
        
        
        self.tableWidget_account.setColumnCount(7)
        
        #selectAll = QCheckBox()
        #selectAll.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter|Qt.AlignCenter)
        #self.allFormatsTable.setHorizontalHeaderItem(0, selectAll)
        #self.tableWidget_account.setCellWidget(-1, -1, selectAll)
        self.tableWidget_account.setHorizontalHeaderLabels(["    ", "类型", "账号", "密码", "是否有头像", "状态", "备注"])
        #self.tableWidget_account.verticalHeader().setVisible(False)
        self.tableWidget_account.setColumnWidth(0, 50)
        self.tableWidget_account.setColumnWidth(1, 80)
        self.tableWidget_account.setColumnWidth(2, 120)
        self.tableWidget_account.setColumnWidth(3, 120)
        self.tableWidget_account.setColumnWidth(4, 100)
        self.tableWidget_account.setColumnWidth(5, 100)
        self.tableWidget_account.setColumnWidth(6, 320)
        
        accounts = self.sqlUtil.select_account()
        count = len(accounts)
        self.tableWidget_account.setRowCount(count)
        i = 0
        for row in accounts:
            select = QTableWidgetItem()
            select.setCheckState(Qt.Unchecked)
            type = QTableWidgetItem(row[3])
            account = QTableWidgetItem(row[1])
            password = QTableWidgetItem(row[2])
            avatar = QTableWidgetItem(row[4])
            status = QTableWidgetItem(row[5])
            remark = QTableWidgetItem(row[6])
            self.tableWidget_account.setItem(i, 0, select)
            self.tableWidget_account.setItem(i, 1, type)  
            self.tableWidget_account.setItem(i, 2, account)
            self.tableWidget_account.setItem(i, 3, password)
            self.tableWidget_account.setItem(i, 4, avatar)  
            self.tableWidget_account.setItem(i, 5, status)  
            self.tableWidget_account.setItem(i, 6, remark)
            i += 1
        
        self.initSettingUi()
        
    def init(self):
        #init
        self.sqlUtil.create_task_table()
        self.sqlUtil.create_account_table()
        self.sqlUtil.create_history_table()
        self.sqlUtil.create_setting_table()
        self.sqlUtil.create_setting_table()
        self.sqlUtil.create_zhihu_user_info_table()
        self.sqlUtil.insert_zhihu_user_info()
        if not os.path.exists('cookies'):
            os.mkdir('cookies')
        if not os.path.exists('avatars'):
            os.mkdir('avatars')
        if not os.path.exists('data'):
            os.mkdir('data')
            
    def selectAllAccount(self):
        
        if self.tableWidget_account.rowCount() == 0:
            QMessageBox.information(self,"提示","没有账号",QMessageBox.Ok)
            return
        
        if self.pushButton_selectAllAccount.text() == '全选':
            self.pushButton_selectAllAccount.setText('全不选')
            for i in range(self.tableWidget_account.rowCount()):
                select = self.tableWidget_account.item(i, 0)
                select.setCheckState(Qt.Checked)
        else:
            self.pushButton_selectAllAccount.setText('全选')
            for i in range(self.tableWidget_account.rowCount()):
                select = self.tableWidget_account.item(i, 0)
                select.setCheckState(Qt.Unchecked)
                
    def showAddTaskForm(self):
        
        #print('showAddTaskForm')
        self.addTaskForm = Ui_Form_AddTask()
        self.addTaskWidget = QWidget()
        self.addTaskForm.setupUi(self.addTaskWidget)
        self.addTaskWidget.show()
        
        self.addTaskForm.pushButton_addTask.clicked.connect(self.addTask)
        self.addTaskForm.pushButton_clearTask.clicked.connect(self.clearTask)
    
    def selectAllTask(self):
        
        if self.tableWidget_task.rowCount() == 0:
            QMessageBox.information(self,"提示","没有任务",QMessageBox.Ok)
            return
        
        if self.pushButton_selectAllTask.text() == '全选':
            self.pushButton_selectAllTask.setText('全不选')
            for i in range(self.tableWidget_task.rowCount()):
                select = self.tableWidget_task.item(i, 0)
                select.setCheckState(Qt.Checked)
        else:
            self.pushButton_selectAllTask.setText('全选')
            for i in range(self.tableWidget_task.rowCount()):
                select = self.tableWidget_task.item(i, 0)
                select.setCheckState(Qt.Unchecked)
                
    def addTask(self):
        #print('addTask123')
        
        #self.tableWidget_account.setRowCount(0)
        
        taskType = self.addTaskForm.comboBox_taskType.currentText()
        taskUrl = self.addTaskForm.lineEdit_taskUrl.text()
        taskCount = self.addTaskForm.lineEdit_taskCount.text()
        taskInterval = self.addTaskForm.comboBox_taskInterval.currentText()
        taskOrder = self.addTaskForm.comboBox_taskOrder.currentText()
        taskCustomer = self.addTaskForm.lineEdit_taskCustomer.text()
        taskRemark = self.addTaskForm.lineEdit_taskRemark.text()
        
        if taskUrl == '':
            #QMessageBox.information(self,"提示","任务url不能为空",QMessageBox.Ok)
            return
        
        self.addTaskWidget.hide()
        
        self.sqlUtil.insert_task(taskType, taskUrl, taskCount, '0', '0', '新建',  taskOrder, taskInterval, taskCustomer, '否', taskRemark)
    

        self.pushButton_selectAllTask.setText('全选')
        
        tasks = self.sqlUtil.select_task()
        taskCount = len(tasks)
        self.tableWidget_task.setRowCount(taskCount)
        i = 0
        for row in tasks:
            #print('id = '+ str(row[0]))
            select = QTableWidgetItem()
            select.setCheckState(Qt.Unchecked)
            taskIdItem = QTableWidgetItem(str(row[0]))
            taskTypeItem = QTableWidgetItem(row[1])
            taskUrlItem = QTableWidgetItem(row[2])
            taskCountItem = QTableWidgetItem(row[3])
            taskBeginCountItem = QTableWidgetItem(row[4])
            taskCurrentCountItem = QTableWidgetItem(row[5])
            taskStatusItem = QTableWidgetItem(row[6])
            taskOrderItem = QTableWidgetItem(row[7])
            taskIntervalItem = QTableWidgetItem(row[8])
            taskCustomerItem = QTableWidgetItem(row[9])
            taskDeliverItem = QTableWidgetItem(row[10])
            taskRemarkItem = QTableWidgetItem(row[11])
            
            
            self.tableWidget_task.setItem(i, 0, select)
            self.tableWidget_task.setItem(i, 1, taskTypeItem)  
            self.tableWidget_task.setItem(i, 2, taskUrlItem)
            self.tableWidget_task.setItem(i, 3, taskCountItem)
            self.tableWidget_task.setItem(i, 4, taskBeginCountItem)
            self.tableWidget_task.setItem(i, 5, taskCurrentCountItem)
            self.tableWidget_task.setItem(i, 6, taskStatusItem)
            self.tableWidget_task.setItem(i, 7, taskOrderItem)
            self.tableWidget_task.setItem(i, 8, taskIntervalItem)  
            self.tableWidget_task.setItem(i, 9, taskCustomerItem)
            self.tableWidget_task.setItem(i, 10, taskDeliverItem)
            self.tableWidget_task.setItem(i, 11, taskRemarkItem)
            self.tableWidget_task.setItem(i, 12, taskIdItem)
            
            i += 1
            

                
        
    def clearTask(self):
        print('clearTask')
                    
    def deleteTask(self):
        
        #print('deleteTask')
        
            
        if self.tableWidget_task.rowCount() == 0:
            QMessageBox.information(self,"提示","没有任务",QMessageBox.Ok)
            return
        
        selectItems = []
        for i in range(self.tableWidget_task.rowCount()):
            if self.tableWidget_task.item(i, 0).checkState() == Qt.Checked:
                 selectItems.append(self.tableWidget_task.item(i, 11).text())
                
        selectItemsCount = len(selectItems)
        if selectItemsCount == 0:
            QMessageBox.information(self,"提示","请勾选要删除的任务",QMessageBox.Ok)
            return
        
        reply = QMessageBox.question(self, '提示', '确认删除任务吗?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.pushButton_selectAllTask.setText('全选')
            selectItems = []
            for i in range(self.tableWidget_task.rowCount()):
                if self.tableWidget_task.item(i, 0).checkState() == Qt.Checked:
                     selectItems.append(i)
                     #print('账户 = '+str(self.tableWidget_account.item(i, 2).text()))
                     self.sqlUtil.delete_task(self.tableWidget_task.item(i, 2).text())
            
            selectItems.sort(reverse = True)            
            for item in selectItems:
                self.tableWidget_task.removeRow(item)
        
            
            
        
    
    def showUpdateTaskForm(self):
        #print('showUpdateTaskForm')
        if self.tableWidget_task.rowCount() == 0:
            QMessageBox.information(self,"提示","没有任务",QMessageBox.Ok)
            return
        selectItems = []
        for i in range(self.tableWidget_task.rowCount()):
            if self.tableWidget_task.item(i, 0).checkState() == Qt.Checked:
                 selectItems.append(self.tableWidget_task.item(i, 12).text())
                
        selectItemsCount = len(selectItems)
        
        
        
        #print('selectItemsCount = '+str(selectItemsCount))
        
        if selectItemsCount == 0:
            QMessageBox.information(self,"提示","请勾选要修改的任务",QMessageBox.Ok)
            return
        elif selectItemsCount == 1:
            self.updateTaskForm = Ui_Form_UpdateTask()
            self.updateTaskWidget = QWidget()
            self.updateTaskForm.setupUi(self.updateTaskWidget)
            self.updateTaskWidget.show()
            
            task = self.sqlUtil.query_task(selectItems[0])
            
            self.updateTaskForm.lineEdit_taskId.setVisible(False)
            self.updateTaskForm.lineEdit_taskId.setText(str(task[0][0]))
            taskTypeIndex = self.updateTaskForm.comboBox_taskType.findText(task[0][1])
            #print('taskTypeIndex = '+str(taskTypeIndex))
            self.updateTaskForm.comboBox_taskType.setCurrentIndex(taskTypeIndex)
            self.updateTaskForm.lineEdit_taskUrl.setText(task[0][2])
            self.updateTaskForm.lineEdit_taskCount.setText(task[0][3])
            self.updateTaskForm.lineEdit_taskBeginCount.setText(task[0][4])
            self.updateTaskForm.lineEdit_taskCurrentCount.setText(task[0][5])
            taskStatusIndex = self.updateTaskForm.comboBox_taskStatus.findText(task[0][6])
            self.updateTaskForm.comboBox_taskStatus.setCurrentIndex(taskStatusIndex)
            taskOrderIndex = self.updateTaskForm.comboBox_taskOrder.findText(task[0][7])
            self.updateTaskForm.comboBox_taskOrder.setCurrentIndex(taskOrderIndex)
            taskIntervalIndex = self.updateTaskForm.comboBox_taskInterval.findText(task[0][8])
            self.updateTaskForm.comboBox_taskInterval.setCurrentIndex(taskIntervalIndex)
            self.updateTaskForm.lineEdit_taskCustomer.setText(task[0][9])
            taskDeliverIndex = self.updateTaskForm.comboBox_taskDeliver.findText(task[0][10])
            self.updateTaskForm.comboBox_taskDeliver.setCurrentIndex(taskDeliverIndex)
            self.updateTaskForm.lineEdit_taskRemark.setText(task[0][11])
            
            
        elif selectItemsCount > 1:
            self.updateTaskForm = Ui_Form_UpdateTask()
            self.updateTaskWidget = QWidget()
            self.updateTaskForm.setupUi(self.updateTaskWidget)
            self.updateTaskWidget.show()
            self.updateTaskForm.lineEdit_taskId.setVisible(False)
            self.updateTaskForm.comboBox_taskType.setEnabled(False)
            self.updateTaskForm.lineEdit_taskUrl.setEnabled(False)
            self.updateTaskForm.lineEdit_taskCount.setEnabled(False)
            self.updateTaskForm.lineEdit_taskBeginCount.setEnabled(False)
            self.updateTaskForm.lineEdit_taskCurrentCount.setEnabled(False)
            self.updateTaskForm.lineEdit_taskCustomer.setEnabled(False)
            self.updateTaskForm.lineEdit_taskRemark.setEnabled(False)
            
        self.updateTaskForm.pushButton_updateTask.clicked.connect(self.updateTask)
        #self.updateTaskForm.pushButton_clearTask.clicked.connect(self.clearTask2)
        
    def showQueryTaskForm(self):
        
        #print('showQueryTaskForm')
        self.queryTaskForm = Ui_Form_QueryTask()
        self.queryTaskWidget = QWidget()
        self.queryTaskForm.setupUi(self.queryTaskWidget)
        self.queryTaskWidget.show()
        
        self.queryTaskForm.pushButton_queryTask.clicked.connect(self.queryTask)
        #self.queryTaskForm.pushButton_clearTask.clicked.connect(self.clearTask3)    
    def updateTask(self):
        #print('updateTask') 
        self.updateTaskWidget.hide()
        self.pushButton_selectAllTask.setText('全选')
        if self.updateTaskForm.comboBox_taskType.isEnabled():
            taskId = self.updateTaskForm.lineEdit_taskId.text()
            taskType = self.updateTaskForm.comboBox_taskType.currentText()
            taskUrl = self.updateTaskForm.lineEdit_taskUrl.text()
            taskCount = self.updateTaskForm.lineEdit_taskCount.text()
            taskBeginCount = self.updateTaskForm.lineEdit_taskBeginCount.text()
            taskCurrentCount = self.updateTaskForm.lineEdit_taskCurrentCount.text()
            taskStatus = self.updateTaskForm.comboBox_taskStatus.currentText()
            taskOrder = self.updateTaskForm.comboBox_taskOrder.currentText()
            taskInterval = self.updateTaskForm.comboBox_taskInterval.currentText()
            taskCustomer = self.updateTaskForm.lineEdit_taskCustomer.text()
            taskDeliver = self.updateTaskForm.comboBox_taskDeliver.currentText()
            taskRemark = self.updateTaskForm.lineEdit_taskRemark.text()
            
            self.sqlUtil.update_task(taskType, taskUrl, taskCount, taskBeginCount, taskCurrentCount, taskStatus, taskOrder, taskInterval, taskCustomer, taskDeliver, taskRemark, taskId)
            
        else:
            #print('多选')
            selectItems = []
            for i in range(self.tableWidget_task.rowCount()):
                if self.tableWidget_task.item(i, 0).checkState() == Qt.Checked:
                     selectItems.append(self.tableWidget_task.item(i, 12).text())
            
            for taskId in selectItems:
                taskStatus = self.updateTaskForm.comboBox_taskStatus.currentText()
                taskOrder = self.updateTaskForm.comboBox_taskOrder.currentText()
                taskInterval = self.updateTaskForm.comboBox_taskInterval.currentText()
                taskCustomer = self.updateTaskForm.lineEdit_taskCustomer.text()
                taskDeliver = self.updateTaskForm.comboBox_taskDeliver.currentText()
                #taskRemark = self.updateTaskForm.lineEdit_taskRemark.text()
            
                self.sqlUtil.update_task_batch(taskStatus, taskOrder, taskInterval, taskDeliver, taskId)
        
        tasks = self.sqlUtil.select_task()
        taskCount = len(tasks)
        self.tableWidget_task.setRowCount(taskCount)
        i = 0
        for row in tasks:
            #print('id = '+ str(row[0]))
            select = QTableWidgetItem()
            select.setCheckState(Qt.Unchecked)
            taskIdItem = QTableWidgetItem(str(row[0]))
            taskTypeItem = QTableWidgetItem(row[1])
            taskUrlItem = QTableWidgetItem(row[2])
            taskCountItem = QTableWidgetItem(row[3])
            taskBeginCountItem = QTableWidgetItem(row[4])
            taskCurrentCountItem = QTableWidgetItem(row[5])
            taskStatusItem = QTableWidgetItem(row[6])
            taskOrderItem = QTableWidgetItem(row[7])
            taskIntervalItem = QTableWidgetItem(row[8])
            taskCustomerItem = QTableWidgetItem(row[9])
            taskDeliverItem = QTableWidgetItem(row[10])
            taskRemarkItem = QTableWidgetItem(row[11])
            
            
            self.tableWidget_task.setItem(i, 0, select)
            self.tableWidget_task.setItem(i, 1, taskTypeItem)  
            self.tableWidget_task.setItem(i, 2, taskUrlItem)
            self.tableWidget_task.setItem(i, 3, taskCountItem)
            self.tableWidget_task.setItem(i, 4, taskBeginCountItem)
            self.tableWidget_task.setItem(i, 5, taskCurrentCountItem)
            self.tableWidget_task.setItem(i, 6, taskStatusItem)
            self.tableWidget_task.setItem(i, 7, taskOrderItem)
            self.tableWidget_task.setItem(i, 8, taskIntervalItem)  
            self.tableWidget_task.setItem(i, 9, taskCustomerItem)
            self.tableWidget_task.setItem(i, 10, taskDeliverItem)
            self.tableWidget_task.setItem(i, 11, taskRemarkItem)
            self.tableWidget_task.setItem(i, 12, taskIdItem)
            
            i += 1
                
                
    def queryTask(self):
        
        self.pushButton_selectAllTask.setText('全选')
        self.queryTaskWidget.hide()
        taskType = self.queryTaskForm.comboBox_taskType.currentText()
        taskUrl = self.queryTaskForm.lineEdit_taskUrl.text()
        taskCount = self.queryTaskForm.lineEdit_taskCount.text()
        taskBeginCount = self.queryTaskForm.lineEdit_taskBeginCount.text()
        taskCurrentCount = self.queryTaskForm.lineEdit_taskCurrentCount.text()
        taskStatus = self.queryTaskForm.comboBox_taskStatus.currentText()
        taskOrder = self.queryTaskForm.comboBox_taskOrder.currentText()
        taskInterval = self.queryTaskForm.comboBox_taskInterval.currentText()
        taskCustomer = self.queryTaskForm.lineEdit_taskCustomer.text()
        taskDeliver = self.queryTaskForm.comboBox_taskDeliver.currentText()
        taskRemark = self.queryTaskForm.lineEdit_taskRemark.text()
        
     
        
        tasks = self.sqlUtil.query_tasks(taskType, taskUrl, taskCount, taskBeginCount, taskCurrentCount, taskStatus, taskOrder, taskInterval, taskCustomer, taskDeliver, taskRemark)
        taskCount = len(tasks)
        self.tableWidget_task.setRowCount(taskCount)
        i = 0
        for row in tasks:
            select = QTableWidgetItem()
            select.setCheckState(Qt.Unchecked)
            taskTypeItem = QTableWidgetItem(row[1])
            taskUrlItem = QTableWidgetItem(row[2])
            taskCountItem = QTableWidgetItem(row[3])
            taskBeginCountItem = QTableWidgetItem(row[4])
            taskCurrentCountItem = QTableWidgetItem(row[5])
            taskStatusItem = QTableWidgetItem(row[6])
            taskOrderItem = QTableWidgetItem(row[7])
            taskIntervalItem = QTableWidgetItem(row[8])
            taskCustomerItem = QTableWidgetItem(row[9])
            taskDeliverItem = QTableWidgetItem(row[10])
            taskRemarkItem = QTableWidgetItem(row[11])
            
            self.tableWidget_task.setItem(i, 0, select)
            self.tableWidget_task.setItem(i, 1, taskTypeItem)  
            self.tableWidget_task.setItem(i, 2, taskUrlItem)
            self.tableWidget_task.setItem(i, 3, taskCountItem)
            self.tableWidget_task.setItem(i, 4, taskBeginCountItem) 
            self.tableWidget_task.setItem(i, 5, taskCurrentCountItem)  
            self.tableWidget_task.setItem(i, 6, taskStatusItem)  
            self.tableWidget_task.setItem(i, 7, taskOrderItem)
            self.tableWidget_task.setItem(i, 8, taskIntervalItem)
            self.tableWidget_task.setItem(i, 9, taskCustomerItem)
            self.tableWidget_task.setItem(i, 10, taskDeliverItem)
            self.tableWidget_task.setItem(i, 11, taskRemarkItem)
            
            i += 1          
            
            
    def importAccount(self):
        #print('importAccount')
        options = QFileDialog.Options()
        
        fileName, _ = QFileDialog.getOpenFileName(self,
                "选取文件", os.path.join(os.path.expanduser("~"), 'Desktop'),
                "Text Files (*.txt)", options=options)
        
        #print('fileName = '+fileName)
        
        if fileName == '':
            return
        f = open(fileName, 'r')  
        lines = f.readlines()
        count = len(lines)
        #print('count = '+str(count))

        self.tableWidget_account.setRowCount(count)
        
        i = 0
        
        #sqlUtil = SqlUtil()
        
        for line in lines:
            
            temp = line.split(' ')
            #select = QCheckBox()
            select = QTableWidgetItem()
            select.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            select.setCheckState(Qt.Unchecked)
            type = QTableWidgetItem('手机号')
            account = QTableWidgetItem(temp[0])
            password = QTableWidgetItem(temp[1].strip('\n'))
            avatar = QTableWidgetItem('否')
            status = QTableWidgetItem('正常')
            remark = QTableWidgetItem('导入的账号')
            
            #self.tableWidget_account.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.tableWidget_account.setItem(i, 0, select)
            self.tableWidget_account.setItem(i, 1, type)  
            self.tableWidget_account.setItem(i, 2, account)
            self.tableWidget_account.setItem(i, 3, password)
            self.tableWidget_account.setItem(i, 4, avatar)  
            self.tableWidget_account.setItem(i, 5, status)  
            self.tableWidget_account.setItem(i, 6, remark) 
            
            self.sqlUtil.insert_account(temp[0], temp[1].strip('\n'),'','', '手机号','否', '正常', '导入的账号')
            #sqlUtil.insert_account('18511339090', '123456', 'phone', '备注')
            
            i += 1
    
    def exportAccount(self):
        #print('exportAccount') 
        
        if self.tableWidget_account.rowCount() == 0:
            QMessageBox.information(self,"提示","没有账号",QMessageBox.Ok)
            return
        selectItems = []
        for i in range(self.tableWidget_account.rowCount()):
            if self.tableWidget_account.item(i, 0).checkState() == Qt.Checked:
                 selectItems.append(i)
                 
        selectItemsCount = len(selectItems)
        if selectItemsCount == 0:
            QMessageBox.information(self,"提示","请勾选要导出的账号",QMessageBox.Ok)
            return
        
        
        options = QFileDialog.Options()
        
        
        fileName, _ = QFileDialog.getSaveFileName(self,
                "导出账号",
                os.path.join(os.path.expanduser("~"), 'Desktop'),
                "Text Files (*.txt)", options=options)
        
        #print('fileName = '+fileName)
        
        if fileName == '':
            return
        
        account_data = ''
        for i in range(self.tableWidget_account.rowCount()):
            if self.tableWidget_account.item(i, 0).checkState() == Qt.Checked:
                account_data = account_data + self.tableWidget_account.item(i, 2).text() + ' ' + self.tableWidget_account.item(i, 3).text() + '\n'
                statusItem = QTableWidgetItem('已导出')
                self.tableWidget_account.setItem(i, 5, statusItem)
                self.sqlUtil.update_account( self.tableWidget_account.item(i, 2).text(), '已导出', '')
                
        with open(fileName, 'w') as f:
            f.write(account_data)
        
               
    def showRegisterAccountForm(self):
        
        #print('showRegisterAccountForm')
        self.registerAccountForm = Ui_Form_RegisterAccount()
        self.registerAccountWidget = QWidget()
        self.registerAccountForm.setupUi(self.registerAccountWidget)
        self.registerAccountWidget.show()
        
        
        self.registerAccountForm.comboBox_registerType.addItems(['否 ','是'])
        self.registerAccountForm.pushButton_registerStop.setEnabled(False)
        self.registerAccountForm.lineEdit_registerCompleteCount.setEnabled(False)
        
        self.registerAccountForm.lineEdit_registerCompleteCount.setText('0')
        
        self.registerAccountForm.pushButton_registerStart.clicked.connect(self.registerAccountStart)
        self.registerAccountForm.pushButton_registerStop.clicked.connect(self.registerAccountStop)
    
    def showQueryAccountForm(self):
        #print('showQueryForm')
        self.queryAccountForm = Ui_Form_QueryAccount()
        self.queryAccountWidget = QWidget()
        self.queryAccountForm.setupUi(self.queryAccountWidget)
        self.queryAccountWidget.show()
        
        self.queryAccountForm.pushButton_query.clicked.connect(self.queryAccount)
        self.queryAccountForm.pushButton_clear.clicked.connect(self.clearAccount)
        
            
            
    def deleteAccount(self):
        if self.tableWidget_account.rowCount() == 0:
            QMessageBox.information(self,"提示","没有账号",QMessageBox.Ok)
            return
        selectItems = []
        for i in range(self.tableWidget_account.rowCount()):
            if self.tableWidget_account.item(i, 0).checkState() == Qt.Checked:
                 selectItems.append(i)
                 
        selectItemsCount = len(selectItems)
        if selectItemsCount == 0:
            QMessageBox.information(self,"提示","请勾选要删除的账号",QMessageBox.Ok)
            return
        
        reply = QMessageBox.question(self, '提示', '确认删除账号吗?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            selectItems = []
            for i in range(self.tableWidget_account.rowCount()):
                if self.tableWidget_account.item(i, 0).checkState() == Qt.Checked:
                    selectItems.append(i)
                    self.sqlUtil.delete_account(self.tableWidget_account.item(i, 2).text())
            
            selectItems.sort(reverse = True)            
            for item in selectItems:
                self.tableWidget_account.removeRow(item)

            
    def updateAccount(self):
        if self.tableWidget_account.rowCount() == 0:
            QMessageBox.information(self,"提示","没有账号",QMessageBox.Ok)
            return
        
        selectItems = []
        for i in range(self.tableWidget_account.rowCount()):
            if self.tableWidget_account.item(i, 0).checkState() == Qt.Checked:
                 selectItems.append(i)
                 
        selectItemsCount = len(selectItems)
        if selectItemsCount == 0:
            QMessageBox.information(self,"提示","请勾选要修改的账号",QMessageBox.Ok)
            return
        
        for i in range(self.tableWidget_account.rowCount()):
            if self.tableWidget_account.item(i, 0).checkState() == Qt.Checked:
                status = self.comboBox_accountStatus.currentText()
                statusItem = QTableWidgetItem(status)
                self.tableWidget_account.setItem(i, 5, statusItem)  
                 
                self.sqlUtil.update_account( self.tableWidget_account.item(i, 2).text(), status, '' )
         
    
            
    '''    
    def registerAccountStart(self):
        #print('registerAccountStart')        
        
        
        try:
            task_count = int(self.registerAccountForm.lineEdit_registerCount.text())
            self.registerAccountForm.pushButton_registerStart.setEnabled(False)
            self.registerAccountForm.pushButton_registerStop.setEnabled(True)
            self.registerAccountThread = RegisterAccountThread(self, task_count)
            self.registerAccountThread.start()
        except:
            self.registerAccountForm.lineEdit_registerCount.setText('')
            
        
    def registerAccountStop(self):
        #print('registerAccountStop')        
        
        self.registerAccountForm.pushButton_registerStart.setEnabled(True)
        self.registerAccountForm.pushButton_registerStop.setEnabled(False)
        self.registerAccountThread.setDaemon(True)
        
    '''
        
    def queryAccount(self):
        #print('queryAccount') 
        self.queryAccountWidget.hide()
        #self.tableWidget_account.setRowCount(0)
        
        type = self.queryAccountForm.comboBox_queryType.currentText()
        account = self.queryAccountForm.lineEdit_queryAccount.text()
        password = self.queryAccountForm.lineEdit_queryPassword.text()
        avatar = self.queryAccountForm.comboBox_queryAvatar.currentText()
        status = self.queryAccountForm.comboBox_queryStatus.currentText()
        remark = self.queryAccountForm.lineEdit_queryRemark.text()
        
     
        
        accounts = self.sqlUtil.query_accounts(type, account, password, avatar, status, remark)
        count = len(accounts)
        self.tableWidget_account.setRowCount(count)
        i = 0
        for row in accounts:
            select = QTableWidgetItem()
            select.setCheckState(Qt.Unchecked)
            type = QTableWidgetItem(row[3])
            account = QTableWidgetItem(row[1])
            password = QTableWidgetItem(row[2])
            avatar = QTableWidgetItem(row[4])
            status = QTableWidgetItem(row[5])
            remark = QTableWidgetItem(row[6])
            self.tableWidget_account.setItem(i, 0, select)
            self.tableWidget_account.setItem(i, 1, type)  
            self.tableWidget_account.setItem(i, 2, account)
            self.tableWidget_account.setItem(i, 3, password)
            self.tableWidget_account.setItem(i, 4, avatar)  
            self.tableWidget_account.setItem(i, 5, status)  
            self.tableWidget_account.setItem(i, 6, remark)
            i += 1
        
    def clearAccount(self):
        #print('clearAccount') 
        self.queryAccountForm.comboBox_queryType.setCurrentIndex(0)
        self.queryAccountForm.lineEdit_queryAccount.setText('')
        self.queryAccountForm.lineEdit_queryPassword.setText('')
        self.queryAccountForm.comboBox_queryAvatar.setCurrentIndex(0)
        self.queryAccountForm.comboBox_queryStatus.setCurrentIndex(0)
        self.queryAccountForm.lineEdit_queryRemark.setText('')    
        
    
    NUM_TASK_THREADS = 3
    sig_abort_task_workers = pyqtSignal()
            
    def startTask(self):
        if self.tableWidget_task.rowCount() == 0:
            QMessageBox.information(self,"提示","没有任务",QMessageBox.Ok)
            return
        
        selectItems = []
        for i in range(self.tableWidget_task.rowCount()):
            if self.tableWidget_task.item(i, 6).text() in ('新建', '待执行', '执行中'):
                 selectItems.append(self.tableWidget_task.item(i, 12).text())
                
        selectItemsCount = len(selectItems)
        if selectItemsCount == 0:
            QMessageBox.information(self,"提示","没有需要执行的的任务",QMessageBox.Ok)
            return
        
        selectItems = []
        for i in range(self.tableWidget_task.rowCount()):
            if self.tableWidget_task.item(i, 0).checkState() == Qt.Checked and self.tableWidget_task.item(i, 6).text() in ('新建', '待执行', '执行中'):
                 selectItems.append(i)
                
        selectItemsCount = len(selectItems)
        if selectItemsCount == 0:
            QMessageBox.information(self,"提示","请勾选要执行的任务",QMessageBox.Ok)
            return
        else:
            for i in selectItems:
                taskStatusItem = QTableWidgetItem('待执行')
                self.tableWidget_task.setItem(i, 6, taskStatusItem)
                self.sqlUtil.update_task_status('待执行', self.tableWidget_task.item(i, 12).text())
           
        self.pushButton_startTask.setEnabled(False)
        self.pushButton_stopTask.setEnabled(True)
        
            
        print('使用 {}个线程'.format(self.NUM_TASK_THREADS))
        
        self.task_threads = []
        for idx in range(self.NUM_TASK_THREADS):
            print('idx = '+str(idx))
            taskThread = ProcessTaskThread(idx + 1, self)
            self.task_threads.append(taskThread) 
            taskThread.start() 
     
    def stopTask(self):
        print('stopTask')
        self.pushButton_startTask.setEnabled(True)
        self.pushButton_stopTask.setDisabled(True)
        self.stopTaskThread = StopTaskThread(self.task_threads, self)
        self.stopTaskThread.start()
        
    
    NUM_REGISTER_THREADS = 2
   
    def registerAccountStart(self):
        print('registerAccountStart')   
        
        try:
            register_type = self.registerAccountForm.comboBox_registerType.currentText()
            register_count = int(self.registerAccountForm.lineEdit_registerCount.text())
            self.registerAccountForm.pushButton_registerStart.setEnabled(False)
            self.registerAccountForm.pushButton_registerStop.setEnabled(True)
            self.registerAccountForm.lineEdit_registerCompleteCount.setText('0')
            
            print('使用 {} 个线程'.format(self.NUM_REGISTER_THREADS))
            
            self.register_threads = []
            for idx in range(self.NUM_REGISTER_THREADS):
                print('idx = '+str(idx))
                registerThread = ProcessRegisterThread(idx + 1, self, register_type, register_count)
                self.register_threads.append(registerThread) 
                registerThread.start() 
        
        except:
            self.registerAccountForm.lineEdit_registerCount.setText('')     
        
    def registerAccountStop(self):
        print('registerAccountStop')
        self.registerAccountForm.pushButton_registerStart.setEnabled(True)
        self.registerAccountForm.pushButton_registerStop.setEnabled(False) 
        self.registerAccountForm.lineEdit_registerCompleteCount.setText('0')
                                
        self.stopRegisterThread = StopRegisterThread(self.register_threads, self)
        self.stopRegisterThread.start()
                  
        
    def initSettingUi(self):
        #print('setting')
        
        wangluo = self.sqlUtil.query_settings('wangluo')
        if len(wangluo) > 0:
            if wangluo[0][0] == '1':
                self.radioButton_benjiwangluo.setChecked(True)
            elif wangluo[0][0] == '2':
                self.radioButton_dongtaiip.setChecked(True)
            elif wangluo[0][0] == '3':   
                self.radioButton_adslbohao.setChecked(True)
            
        dama = self.sqlUtil.query_settings('dama')
        if len(dama) >0:
            damaPingtaiIndex = self.comboBox_damapingtai.findText(dama[0][0])
            self.comboBox_damapingtai.setCurrentIndex(damaPingtaiIndex)
            self.lineEdit_damazhanghao.setText(dama[0][1])
            self.lineEdit_damamima.setText(dama[0][2])
        
        jiema = self.sqlUtil.query_settings('jiema')
        if len(jiema) > 0:
            jiemaPingtaiIndex = self.comboBox_jimapingtai.findText(jiema[0][0])
            self.comboBox_jimapingtai.setCurrentIndex(jiemaPingtaiIndex)
            self.lineEdit_jiemazhanghao.setText(jiema[0][1])
            self.lineEdit_jiemamima.setText(jiema[0][2])
            
    
    def benjiwangluoToggled(self):
        #print('benjiwangluoToggled')  
        if self.radioButton_benjiwangluo.isChecked():
            self.sqlUtil.sava_setting('wangluo', '1', '', '')
            #print('1')
        
     
    def dongtaiipToggled(self):
        if self.radioButton_dongtaiip.isChecked():
            self.sqlUtil.sava_setting('wangluo', '2', '', '')
                       
       
        
    def adslbohaoToggled(self):
        if self.radioButton_adslbohao.isChecked():
            self.sqlUtil.sava_setting('wangluo', '3', '', '')
            #print('3')
            
    def damaDenglu(self):
        print('damaDenglu')
        damapingtai = self.comboBox_damapingtai.currentText()
        damazhanghao = self.lineEdit_damazhanghao.text()
        damamima = self.lineEdit_damamima.text()
        self.sqlUtil.sava_setting('dama', damapingtai, damazhanghao, damamima)
        
    def damaZhuce(self):
        print('damaZhuce')
        webbrowser.open_new('www.ruokuai.com')
        
    def jiemaDenglu(self):
        print('jiemaDenglu')
        jiemapingtai = self.comboBox_jimapingtai.currentText()
        jiemazhanghao = self.lineEdit_jiemazhanghao.text()
        jiemamima = self.lineEdit_jiemamima.text()
        self.sqlUtil.sava_setting('jiema', jiemapingtai, jiemazhanghao, jiemamima)
        
    def jiemaZhuce(self):
        print('jiemaZhuce')
        webbrowser.open_new('www.shjmpt.com:8002')


class ProcessTaskThread(QThread):
    
    def __init__(self, id, ui):
        super().__init__()
        
        self.id = id
        self.ui = ui
        self.isRunning = True
        self.sqlUtil = SqlUtil()
        

    def run(self):
        if self.id != 1:
            time.sleep(self.id * 60)
        print('线程： '+str(self.id)+' 已开始执行')
        while self.isRunning:
            adsl = Adsl()
            thread_name = QThread.currentThread().objectName()
            thread_id = int(QThread.currentThreadId())  # cast to int() is necessary
            
            task = self.sqlUtil.get_pending_task()
            
            if task == None:
                print('task is None')
                self.isRunning = False
                break
            else:
                taskId = task[0]
                taskType = task[1]
                taskUrl = task[2]
                task_count = task[3]
                begin_count = task[4]
                current_count= task[5]
                task_interval = task[6]
                #self.sqlUtil.update_task_status('执行中', str(taskId))
                print('taskUrl = '+taskUrl)
                for i in range(self.ui.tableWidget_task.rowCount()):
                   
                    
                    if self.ui.tableWidget_task.item(i, 2).text() == taskUrl:
                        print('相等')
                        taskStatusItem = QTableWidgetItem('执行中')
                        self.ui.tableWidget_task.setItem(i, 6, taskStatusItem)  
                        self.sqlUtil.update_task_status('执行中', self.ui.tableWidget_task.item(i, 12).text())
             
                 
                print(' ')
                print('当前任务类型: '+taskType)
                print('当前任务url: '+taskUrl)
                
                accounts = self.sqlUtil.get_pending_accounts(taskUrl)
                account_count = len(accounts)
                
                if account_count == 0:
                    print('没有可用的账户，或者可用的账户已为改问题点过赞')
                    break
              
                for account in accounts:
                    
                    begin_count = self.sqlUtil.get_task_begin_count(taskUrl)
                    current_count = self.sqlUtil.get_task_current_count(taskUrl)
                    if int(current_count) - int(begin_count) >= int(task_count):
                        break
                    
                 
                    username = account[1]
                    password = account[2]
                    avatarFlag = account[3]
                    avatarUrl = account[4]
                    headline = account[5]
                    
                    print(' ')
                    if self.id == 1:
                        adsl.reconnect()
                    
                    taskUtil = TaskUtil(taskUrl, username, password)
                    
                    #print('username = '+username)
                    #print('password = '+password)
                    #print('avatarFlag = '+avatarFlag)
                    #print('avatarUrl = '+avatarUrl)
                    #print('headline = '+headline)
                    if avatarFlag == '是':
                       
                        if headline == None:
                            headline = self.sqlUtil.get_headline(avatarUrl)
                            taskUtil.set_guide_headline( headline)
                    
                    
                    current_count = taskUtil.get_current_count()
                   
                    
                    for i in range(self.ui.tableWidget_task.rowCount()):
                        if self.ui.tableWidget_task.item(i, 2).text() == taskUrl:
                            if self.ui.tableWidget_task.item(i, 4).text() == '0':
                                
                                taskBeginCountItem = QTableWidgetItem(str(current_count))
                                self.ui.tableWidget_task.setItem(i, 4, taskBeginCountItem)
                                self.sqlUtil.update_task_begin_count(str(current_count), self.ui.tableWidget_task.item(i, 12).text())
                            
                            taskCurrentCountItem = QTableWidgetItem(str(current_count))
                            self.ui.tableWidget_task.setItem(i, 5, taskCurrentCountItem)  
                            self.sqlUtil.update_task_current_count(str(current_count), self.ui.tableWidget_task.item(i, 12).text())
                            
                            #taskStatusItem = QTableWidgetItem('执行中')
                            #self.ui.tableWidget_task.setItem(i, 6, taskStatusItem)  
                            #self.sqlUtil.update_task_status('执行中', self.ui.tableWidget_task.item(i, 12).text())
                    
                    voteStatus, voteMsg, current_count = taskUtil.vote_answer()
                    #self.sig_msg.emit(taskUrl, str(current_count), username, voteStatus, voteMsg)
                    
                    #插入历史记录
                    self.sqlUtil.insert_history(taskUrl, username, voteStatus)
                    
                    for i in range(self.ui.tableWidget_task.rowCount()):
                        if self.ui.tableWidget_task.item(i, 2).text() == taskUrl:
                            
                            taskCurrentCountItem = QTableWidgetItem(str(current_count))
                            self.ui.tableWidget_task.setItem(i, 5, taskCurrentCountItem)  
                            self.sqlUtil.update_task_current_count(str(current_count), self.ui.tableWidget_task.item(i, 12).text())
                            if int(str(current_count)) - int(self.ui.tableWidget_task.item(i, 4).text()) >= int(self.ui.tableWidget_task.item(i, 3).text()):
                                print('任务url: '+ taskUrl + ' 已完成')
                                taskStatusItem = QTableWidgetItem('完成')
                                self.ui.tableWidget_task.setItem(i, 6, taskStatusItem) 
                                self.sqlUtil.update_task_status('完成', self.ui.tableWidget_task.item(i, 12).text())
                            #    self.stopTask()
                    
                    if voteStatus == 'E':
                        self.sqlUtil.update_account(username, '异常', voteMsg)
                        statusItem = QTableWidgetItem('异常')
                        remarkItem = QTableWidgetItem(voteMsg)
                        for i in range(self.ui.tableWidget_account.rowCount()):
                            if self.ui.tableWidget_account.item(i, 2).text() == username:
                                self.ui.tableWidget_account.setItem(i, 5, statusItem) 
                                self.ui.tableWidget_account.setItem(i, 6, remarkItem)  
                    
                    interval = random.randint(600, 1200)
                    time.sleep(interval)
                    #app.processEvents()  # this could cause change to self.__abort
                    #if self.__abort:
                    #    break
              
        print('线程： '+str(self.id)+' 已停止执行')
        #self.sig_done.emit(self.__id)
            
           
    def stopThread(self):
        print('stopThread')
        self.isRunning = False
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print('in stopThread self.isRunning is False') 


class StopTaskThread(QThread):
    
    def __init__(self, task_threads, ui):
        super().__init__()
        self.task_threads = task_threads
        self.ui = ui
        

    def run(self):
        print('StopTaskThread run')
        for task_thread in self.task_threads:
            task_thread.stopThread()
            task_thread.quit() 
            task_thread.wait()
        
        #self.ui.pushButton_startTask.setEnabled(True)
        print('所有线程已停止')          

class ProcessRegisterThread(QThread):
    
    def __init__(self, id, ui, register_type, register_count):
        super().__init__()
        self.id = id
        self.ui = ui
        self.isRunning = True
        self.register_type = register_type
        self.register_count = register_count
        self.sqlUtil = SqlUtil()
        
        

    def run(self):
        
        print('线程： '+str(self.id)+' 已开始执行')
        shenhua = Shenhua()
        success_count = 0
        print('总共任务数量 ：'+str(self.register_count))
        
        if self.register_type.strip() == '否':
            print('否')
            register = Register()
            #for i in range(self.register_count * 2):
            i = 0
            while self.isRunning:
                print(' ')
                print('开始注册第 '+str(i + 1)+' 个账号')
                i += 1
                phone_no = shenhua.get_phone()
                password = chr(random.randint(97, 122)) + chr(random.randint(97, 122)) + chr(random.randint(97, 122)) + chr(random.randint(97, 122))  + str(random.randint(0, 9))+ str(random.randint(0, 9))+ str(random.randint(0, 9))+ str(random.randint(0, 9))
       
                need_captcha_flag = register.need_captcha()
                
                if register.validate(phone_no):
                    
                    if need_captcha_flag:
                       captcha_id, captcha = register.get_captcha()
                       register.validate_captcha(captcha)
    
                    if register.send_message(phone_no):
                        time.sleep(15)
                        digits = shenhua.get_message(phone_no)
                        if digits != None:
                           
                            if register.register(phone_no, password,  digits):
                                
                                success_count += 1
                                #self.sig_msg.emit(phone_no, password, '', '')
                                maxRowIndex = self.ui.tableWidget_account.rowCount()
                                self.ui.tableWidget_account.setRowCount(maxRowIndex + 1)
                                                    
                                selectItem = QTableWidgetItem()
                                selectItem.setCheckState(Qt.Unchecked)
                                typeItem = QTableWidgetItem('手机号')
                                accountItem = QTableWidgetItem(phone_no)
                                passwordItem = QTableWidgetItem(password)
                                avatarItem = QTableWidgetItem(self.ui.registerAccountForm.comboBox_registerType.currentText())
                                statusItem = QTableWidgetItem('正常')
                                remarkItem = QTableWidgetItem('注册的账号')
                                                    
                                #self.tableWidget_account.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                                self.ui.tableWidget_account.setItem(maxRowIndex, 0, selectItem)
                                self.ui.tableWidget_account.setItem(maxRowIndex, 1, typeItem)  
                                self.ui.tableWidget_account.setItem(maxRowIndex, 2, accountItem)
                                self.ui.tableWidget_account.setItem(maxRowIndex, 3, passwordItem)
                                self.ui.tableWidget_account.setItem(maxRowIndex, 4, avatarItem)  
                                self.ui.tableWidget_account.setItem(maxRowIndex, 5, statusItem)  
                                self.ui.tableWidget_account.setItem(maxRowIndex, 6, remarkItem) 
                                
                           
                                self.sqlUtil.insert_account(phone_no, password, '', '', '手机号','否', '正常', '注册的账号')
                                       
                                complete_count = int(self.ui.registerAccountForm.lineEdit_registerCompleteCount.text()) + 1
                                self.ui.registerAccountForm.lineEdit_registerCompleteCount.setText(str(complete_count))
                                if complete_count >= self.register_count:
                                    self.isRunning = False
                                    self.ui.registerAccountForm.pushButton_registerStart.setEnabled(True)
                                    self.ui.registerAccountForm.pushButton_registerStop.setEnabled(False)
                                
                
        elif self.register_type.strip() == '是':
            print('注册类型为中文名有头像')
            register = Register_Avatar()
            i = 0
            while self.isRunning:
                print(' ')
                print('开始注册第 '+str(i + 1)+' 个账号')
                i += 1
                
                phone_no = shenhua.get_phone()
                password = chr(random.randint(97, 122)) + chr(random.randint(97, 122)) + chr(random.randint(97, 122)) + chr(random.randint(97, 122))  + str(random.randint(0, 9))+ str(random.randint(0, 9))+ str(random.randint(0, 9))+ str(random.randint(0, 9))
                fullname, avatarUrl = self.sqlUtil.get_fullname_avatar()
                need_captcha_flag = register.need_captcha()
                
                if register.validate(phone_no):
                    
                    if need_captcha_flag:
                       captcha_id, captcha = register.get_captcha()
                       register.validate_captcha(captcha)
    
                    if register.send_message(phone_no):
                        
                        time.sleep(15)
                        digits = shenhua.get_message(phone_no)
                        if digits != None:
                           
                            if register.register(phone_no, password, fullname, avatarUrl, digits):
                                
                                success_count += 1
                                #self.sig_msg.emit(phone_no, password, fullname, avatarUrl)
                                maxRowIndex = self.ui.tableWidget_account.rowCount()
                                self.ui.tableWidget_account.setRowCount(maxRowIndex + 1)
                                                    
                                selectItem = QTableWidgetItem()
                                selectItem.setCheckState(Qt.Unchecked)
                                typeItem = QTableWidgetItem('手机号')
                                accountItem = QTableWidgetItem(phone_no)
                                passwordItem = QTableWidgetItem(password)
                                avatarItem = QTableWidgetItem(self.ui.registerAccountForm.comboBox_registerType.currentText())
                                statusItem = QTableWidgetItem('正常')
                                remarkItem = QTableWidgetItem('注册的账号')
                                                    
                                #self.tableWidget_account.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                                self.ui.tableWidget_account.setItem(maxRowIndex, 0, selectItem)
                                self.ui.tableWidget_account.setItem(maxRowIndex, 1, typeItem)  
                                self.ui.tableWidget_account.setItem(maxRowIndex, 2, accountItem)
                                self.ui.tableWidget_account.setItem(maxRowIndex, 3, passwordItem)
                                self.ui.tableWidget_account.setItem(maxRowIndex, 4, avatarItem)  
                                self.ui.tableWidget_account.setItem(maxRowIndex, 5, statusItem)  
                                self.ui.tableWidget_account.setItem(maxRowIndex, 6, remarkItem) 
                                
                               
                                self.sqlUtil.insert_account(phone_no, password, fullname, avatarUrl, '手机号','是', '正常', '注册的账号')
                                              
                                complete_count = int(self.ui.registerAccountForm.lineEdit_registerCompleteCount.text()) + 1
                                self.ui.registerAccountForm.lineEdit_registerCompleteCount.setText(str(complete_count))
                                if complete_count >= self.register_count:
                                    self.isRunning = False
                                    self.ui.registerAccountForm.pushButton_registerStart.setEnabled(True)
                                    self.ui.registerAccountForm.pushButton_registerStop.setEnabled(False)
                                            
        print(' ')
        print('本次注册成功的个数：'+str(success_count))
           
            
        print('线程： '+str(self.id)+' 已停止执行')
        
    def stopThread(self):
        print('stopThread')
        self.isRunning = False
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print('in stopThread self.isRunning is False') 

class StopRegisterThread(QThread):
    
    def __init__(self, register_threads, ui):
        super().__init__()
        self.register_threads = register_threads
        self.ui = ui
        
    def run(self):
        print('StopRegisterThread run')
        for register_thread in self.register_threads:
            register_thread.stopThread()
            register_thread.quit() 
            register_thread.wait()
        
        #self.ui.pushButton_startTask.setEnabled(True)
        print('所有线程已停止')
                            

                       
if __name__ == '__main__':
    
    
    import sys

    app = QApplication(sys.argv)
    app.setApplicationName("zhihu")

    f = Form()
    f.show()
    #f.setWindowFlags(Qt.WindowMinimizeButtonHint)
    #f.resize(819, 581)

    sys.exit(app.exec_())

    #registerAccount(10)