import sys

from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from PyQt5.uic import loadUi
import random


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi('mainwindow.ui', self)  # 加载UI文件
        print("self:", self)
        self.tabWidget.setVisible(False)
        self.PersonalInformationTabWidget.setVisible(False)
        self.MulPickTabWidget.setVisible(False)
        self.resize(700, 420)
        self.flag = 0
        self.flag1 = 0
        self.names = []  # 名字列表
        self.rolledNames = []  # 已点名的名字列表
        self.timer = QTimer(self)  # 创建定时器
        self.timer.timeout.connect(self.on_Timer_timeout)
        pixmap = QPixmap("1.jpg")
        self.label_7.setPixmap (pixmap)  # 在label上显示图片
        self.label_7.setScaledContents (True)  # 让图片自适应label大小
    @pyqtSlot()
    def on_Timer_timeout(self):
        if not self.names:
            QMessageBox.warning(self, '警告', '名字列表为空')
            return
        index = random.randint(0, len(self.names) - 1)
        name = self.names[index]
        self.PickResultLabel.setText(name)

    @pyqtSlot()
    def on_ShowHistoryButton_clicked(self):
        if self.flag == 0:
            # 显示
            self.tabWidget.setVisible(True)
            self.setFixedSize(self.width(), 790)
            self.flag = 1
        else:
            # 隐藏
            self.tabWidget.setVisible(False)
            self.setFixedSize(self.width(), 420)
            self.flag = 0

    @pyqtSlot()
    def on_MulPickButton_clicked(self):
        if self.flag1 == 0:
            # 显示
            self.PersonalInformationTabWidget.setVisible(True)
            self.MulPickTabWidget.setVisible(True)
            self.setFixedSize(1230, self.height())
            self.flag1 = 1
        else:
            # 隐藏
            self.PersonalInformationTabWidget.setVisible(False)
            self.MulPickTabWidget.setVisible(False)
            self.setFixedSize(700, self.height())
            self.flag1 = 0

    @pyqtSlot()
    def on_OpenNameFileButton_clicked(self):
        fileName, _ = QFileDialog.getOpenFileName(self, '打开名字文件', '', 'Text Files (*.txt)')
        if fileName:
            try:
                with open(fileName, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            self.names.append(line)
            except Exception as e:
                QMessageBox.warning(self, '打开文件失败', f'无法打开文件 {fileName}:\n{e}')

    @pyqtSlot()
    def on_PickOneButton_clicked(self):
        if not self.names:
            QMessageBox.warning(self, '警告', '名字列表为空')
            return
        # 启动定时器
        self.timer.start(100)

    @pyqtSlot()
    def on_RePickButton_clicked(self):
        ret = QMessageBox.question(self, '确认', '是否重新开始点名？')
        if ret == QMessageBox.Yes:
            self.rolledNames.clear()
            self.HistoryListWidget.clear()
            self.PickResultLabel.setText('重新开始')
            self.MulHistoryListWidget.clear()

    @pyqtSlot()
    def on_StartMulButton_clicked(self):
        count = int(self.PeopleLineEdit.text())
        if count <= 0:
            QMessageBox.warning(self, '警告', '每次连抽人数必须大于0')
            return
        if not self.names:
            QMessageBox.warning(self, '警告', '名字列表为空')
            return
        remainingCount = count
        while remainingCount > 0 and self.names:
            index = random.randint(0, len(self.names) - 1)
            name = self.names[index]
            self.MulHistoryListWidget.addItem(name)
            if name not in self.rolledNames:
                self.rolledNames.append(name)
                self.HistoryListWidget.addItem(name)
            self.names.remove(name)
            remainingCount -= 1

    @pyqtSlot()
    def on_EndButton_clicked(self):
        # 停止定时器
        self.timer.stop()
        name = self.PickResultLabel.text()
        if name not in self.rolledNames:
            self.rolledNames.append(name)
            self.HistoryListWidget.addItem(name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
