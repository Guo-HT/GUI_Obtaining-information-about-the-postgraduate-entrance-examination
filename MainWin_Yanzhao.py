import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import sys
import yanzhao_ui
import spider_main
import re
import resource
from os import *

dm_num = ""
file_name = ""
file_type = ""


def suppress_qt_warnings():
    environ["QT_DEVICE_PIXEL_RATIO"] = "0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"


class WorkThread(QThread):
    update_ui = pyqtSignal(str)
    end = pyqtSignal()
    btn_update = pyqtSignal()
    clear_textBrowser = pyqtSignal()

    # @retry(stop_max_attempt_number=3)  # 如果报错，重试3次
    def run(self):
        global dm_num, file_name, file_type
        self.clear_textBrowser.emit()
        str_update = "开始获取数据......\n"    # 更新字符串
        self.update_ui.emit(str_update)  # 触发update_ui事件
        yz = spider_main.Yanzhao(dm_num, file_name, file_type)
        page = yz.get_page()
        num = 0
        for i in range(page):
            schools_obj = yz.get_parse_each_page(i)  # 得到每页的学校信息
            # print(f' 第{i + 1}页： {len(schools_obj)}所高校')
            # 遍历专业对应的学校b
            for school_obj in schools_obj:
                # 此循环内是单个学校
                school_line_list = list()
                school_line_str = str()
                school_line_list, school_url, school_line_str = yz.parse_school_info(school_obj, school_line_list,
                                                                                     school_line_str)
                # print(" " + school_line_list[0], end="")
                time.sleep(0.2)
                # 请求学校开设专业详情页
                exam_info_list = yz.get_school_dir(school_url)
                # 遍历每一个研究方向
                for each_exam in exam_info_list:
                    # 此循环内是每一个研究方向
                    exam_info_url, school_line_list, school_line_str = yz.parse_each_dir(each_exam, school_line_list,
                                                                                         school_line_str)
                    time.sleep(0.2)
                    # 请求每个研究方向的主页，提取考试科目
                    school_line_list, school_line_str = yz.get_exam(exam_info_url, school_line_list, school_line_str)
                school_line_str += '\n'
                # 保存！！！！！！！！！
                yz.save_school_line(school_line_list, num, school_line_str)
                num += 1

                str_update = f"{num}.{school_line_list[0]}   done."  # 更新字符串
                self.update_ui.emit(str_update)  # 触发update_ui事件
            time.sleep(0.1)

        str_update = "\n\n完成！！！"  # 更新字符串
        self.update_ui.emit(str_update)  # 触发update_ui事件
        self.end.emit()  # 触发线程结束事件
        self.btn_update.emit()  # 触发释放按钮事件


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # self.ui = yanzhao.Ui_MainWindow()
        self.ui = yanzhao_ui.Ui_MainWindow()
        self.setWindowIcon(QIcon(":exam.ico"))
        self.ui.setupUi(self)
        self.text_Browser = self.ui.textBrowser

        self.workThread = WorkThread()
        self.workThread.update_ui.connect(self.update_ui)
        self.workThread.end.connect(self.end)
        self.workThread.btn_update.connect(self.reset_btn)
        self.workThread.clear_textBrowser.connect(self.clear_textBrowser)

        self.ui.pushButton.clicked.connect(self.catch_info)

    def clear_textBrowser(self):
        self.ui.textBrowser.clear()

    def reset_btn(self):
        time.sleep(1)
        self.ui.pushButton.setEnabled(True)

    def update_ui(self, str_update):
        self.ui.textBrowser.append(str_update)

    def end(self):
        QMessageBox.information(self, '消息', '完成！', QMessageBox.Ok)

    def catch_info(self):
        # print('获取信息')
        global dm_num, file_name, file_type
        sub = self.ui.comboBox.currentText()
        file_name = self.ui.lineEdit.text()
        radiobutton_xls = self.ui.radioButton.isChecked()
        radiobutton_tsv = self.ui.radioButton_2.isChecked()
        # print(sub)
        # print(file_name)
        # print(radiobutton_xls, radiobutton_tsv)
        # ({sub["dm"]}) {sub["mc"]}
        ret = re.match(r'\((.*)\) ', sub)
        dm_num = ret.group(1)
        file_type = str()
        if radiobutton_xls:
            file_type = "1"
        elif radiobutton_tsv:
            file_type = "2"

        self.workThread.start()
        self.ui.pushButton.setEnabled(False)


if __name__ == '__main__':
    suppress_qt_warnings()
    app = QApplication(sys.argv)

    main_win = MainWindow()
    main_win.show()

    sys.exit(app.exec_())
