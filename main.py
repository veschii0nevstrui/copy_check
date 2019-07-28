#!/usr/bin/python3
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QLabel, QTextEdit, QGridLayout, QFileDialog, QMessageBox
from PyQt5.QtCore import QCoreApplication

class main_window(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.btn_gen = QPushButton("Сгенерировать списки", self)
        self.btn_open_contest = QPushButton("Открыть контест", self)
        self.btn_open_task = QPushButton("Открыть задачу", self)
        self.btn_help = QPushButton("Помощь", self)
        self.btn_exit = QPushButton("Выход", self)
        self.btn_next_codes = QPushButton("Следующие решения", self)
        self.btn_prev_codes = QPushButton("Предыдущие решения", self)
        self.btn_next_task = QPushButton("Следующая задача", self)
        self.btn_prev_task = QPushButton("Предыдущая задача", self)
        self.btn_ban = [QPushButton("Забанить!", self), QPushButton("Забанить!", self)]

        self.list_btns = [self.btn_gen, self.btn_open_contest, self.btn_open_task, self.btn_help, self.btn_exit]

        self.lbl_notification = QLabel("", self)
        self.lbl_names = [QLabel("", self), QLabel("", self)]
        self.lbl_score = QLabel("", self)
        self.lbl_task_name = QLabel("", self)

        self.codes = [QTextEdit(), QTextEdit()]
        self.list_tasks = []
        self.list_codes = []
        self.names_code = []
        self.number_pair = 0
        self.ban_list = set()

        self.number_task = 0

        self.btn_gen.clicked.connect(self.gen)
        self.btn_open_contest.clicked.connect(self.open_contest)
        self.btn_open_task.clicked.connect(self.open_task)
        self.btn_help.clicked.connect(self.help)
        self.btn_exit.clicked.connect(QCoreApplication.instance().quit)
        self.btn_next_codes.clicked.connect(self.next_codes)
        self.btn_prev_codes.clicked.connect(self.prev_codes)
        self.btn_next_task.clicked.connect(self.next_task)
        self.btn_prev_task.clicked.connect(self.prev_task)

        self.btn_next_codes.close()
        self.btn_prev_codes.close()
        self.btn_next_task.close()
        self.btn_prev_task.close()
        for i in range(2):
            self.btn_ban[i].clicked.connect(self.ban)
            self.btn_ban[i].my_number = i
            self.btn_ban[i].close()

        self.grid = QGridLayout()

        for i in range(0, len(self.list_btns)):
            self.grid.addWidget(self.list_btns[i], 1, i + 1)
        #self.grid.addWidget(self.lbl_notification, 2, 1, 2, 5)
        
        self.grid.setSpacing(10)
        self.setLayout(self.grid)      

        self.setGeometry(200, 200, 1000, 500)
        self.setWindowTitle('Проверяем детей на списывание')

        self.show()

    def new_notification(self, notification):
        self.lbl_notification.close()
        self.lbl_notification = QLabel(notification, self)
        self.grid.addWidget(self.lbl_notification, 2, 1, 2, 5)
        self.lbl_notification.show()

    def gen(self):
        subprocess.call("./find2")

    def open_contest(self):

        self.contest_name = QFileDialog.getExistingDirectory(self, "Выберите папку с контестом", '.?/')
        self.list_tasks = self.read(self.contest_name + "/tasks.txt")
        
        self.ban_list = set()

        self.number_task = 0

        self.grid.addWidget(self.btn_next_task, 5, 5)
        self.grid.addWidget(self.btn_prev_task, 7, 5)
        
        self.btn_next_task.show()
        self.btn_prev_task.show()
         
        self.ban_out = open(self.contest_name + "/ban_list.txt", "w")

        self.show_task()

    def show_task(self):
        self.task_name = self.contest_name + "/" + self.list_tasks[self.number_task][:-1]

        self.lbl_task_name.close()
        self.lbl_task_name = QLabel("Задача " + self.list_tasks[self.number_task], self)
        self.grid.addWidget(self.lbl_task_name, 6, 5)
        self.lbl_task_name.show()

        self.list_codes = self.read(self.task_name + ".txt")
        self.number_pair = 0

        self.show_codes()

    def open_task(self):
        
        self.ban_list = set()
        self.task_name = QFileDialog.getExistingDirectory(self, "Выберите папку с задачей", './')
        self.ban_out = open(self.task_name + "_ban.txt", 'w')
        
        self.btn_next_task.close()
        self.btn_prev_task.close()

        self.lbl_task_name.close()
        self.lbl_task_name = QLabel("Задача " + self.task_name.split("/")[-1])
        self.grid.addWidget(self.lbl_task_name, 6, 5)
        self.lbl_task_name.show()

        self.list_codes = self.read(self.task_name + ".txt")       
        
        self.number_pair = 0

        self.show_codes()
          
    def show_codes(self):
        
        self.lbl_notification.close()
        
        if len(self.list_codes) == 0:
            reply = QMessageBox.question(self, "Error", "По этой задаче сделано не более одной посылки, сравнивать нечего. Перейдите к другой задаче", QMessageBox.Ok, QMessageBox.Ok)
            for i in range(2):
                self.btn_ban[i].close()
                self.lbl_names[i].close()
                self.codes[i].clear()
            self.lbl_score.close()
            return

        self.names_code = self.list_codes[self.number_pair].split()
        for i in range(2):
            self.lbl_names[i].close()
            self.lbl_names[i] = QLabel(self.names_code[i], self)
            self.codes[i].clear()
            self.codes[i].setReadOnly(1)
            for s in self.read(self.task_name + "/" + self.names_code[i]):
                self.codes[i].append(s[:-1])
        
        self.lbl_score.close()
        self.lbl_score = QLabel(self.names_code[2], self)
        
        self.grid.addWidget(self.codes[0], 3, 1, 7, 2)
        self.grid.addWidget(self.codes[1], 3, 3, 7, 2)
        
        self.grid.addWidget(self.lbl_names[0], 2, 1, 1, 2)
        self.grid.addWidget(self.lbl_names[1], 2, 3, 1, 2)
        self.grid.addWidget(self.lbl_score, 2, 5)
        
        self.grid.addWidget(self.btn_ban[0], 10, 1, 1, 2)
        self.grid.addWidget(self.btn_ban[1], 10, 3, 1, 2)
        
        self.grid.addWidget(self.btn_next_codes, 3, 5)
        self.grid.addWidget(self.btn_prev_codes, 4, 5)  
        
        for i in range(2):
            self.btn_ban[i].show()

        self.btn_next_codes.show()
        self.btn_prev_codes.show()
        
        if self.names_code[0] in self.ban_list:
            self.btn_ban[0].close()
        if self.names_code[1] in self.ban_list:
            self.btn_ban[1].close()
    
    def ban(self):
        self.ban_list.add(self.names_code[self.sender().my_number])
        self.sender().close()
        s = self.task_name.split("/")[-2] + "    " + self.task_name.split("/")[-1] + "    " + self.names_code[self.sender().my_number] + "\n"
        self.ban_out.write(s)

    def help(self):
        reply = QMessageBox.question(self, "Я помогу тебе", "Пользоваться этой программой довольно просто. Надо поместить её и ещё несколько файлов в папку со скачанными контестами, и запустить генератор. Он некоторое время поработает, и после этого появятся списки на проверку. Вы можете выбрать контест или какую-нибудь конкретную задачу. Для этого необходимо выбрать папку с контестом или папку с задачей. Вы можете банить решения, тогда их списко будет заноситься в специальный файлик, с которым вы потом можете делать всё, что угодно. Остались ли вопросы?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            reply = QMessageBox.question(self, "Ну тут как бы ничего уже не поделать", "Обратитесь к создателю программы, он добрый, он поможет", QMessageBox.Yes, QMessageBox.Yes) 
    
    def next_codes(self):
        self.number_pair += 1
        if abs(self.number_pair) == len(self.list_codes):
            reply = QMessageBox.question(self, "Ошибка", "Решения закончились, перейдите к следующей задаче.", QMessageBox.Ok, QMessageBox.Ok)
            self.number_pair -= 1
            return
        self.show_codes()

    def prev_codes(self):    
        self.number_pair -= 1
        if abs(self.number_pair) == len(self.list_codes):
            reply = QMessageBox.question(self, "Ошибка", "Решения закончились, перейдите к следующей задаче.", QMessageBox.Ok, QMessageBox.Ok)
            self.number_pair += 1
            return
        self.show_codes()

    def next_task(self):
        self.number_task += 1
        if abs(self.number_task) == len(self.list_tasks):
            reply = QMessageBox.question(self, "Ошибка", "Задачи в этом контесте кончились, выберите другой", QMessageBox.Ok, QMessageBox.Ok)
            self.number_task -= 1
            return
        self.show_task()

    def prev_task(self):
        self.number_task -= 1
        if abs(self.number_task) == len(self.list_tasks):
            reply = QMessageBox.question(self, "Ошибка", "Задачи в этом контесте кончились, выберите другой", QMessageBox.Ok, QMessageBox.Ok)
            self.number_task += 1
            return
        self.show_task()

    def read(self, name):
        f = open(name)
        ans = []
        for line in f:
            ans += [line]
        return ans

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = main_window()
    sys.exit(app.exec_())
