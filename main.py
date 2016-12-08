# -*- coding: utf-8 -*-
import sys
import os
import sqlite3
from ui_convert import UiConvert
from PyQt5 import QtWidgets, QtSvg
from jinja2 import Environment, FileSystemLoader
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtCore import QUrl, QByteArray
from PyQt5.QtWebKitWidgets import QWebView
from subprocess import check_call

# ----- debug ------
# from ui import Ui_Form
# from sub import Ui_Dialog
# ----- debug ------
cmb_data = [['', '東', '西'],
            ['', '1', '2', '3', '4'],
            ['', '1', '2', '3', '4', '5', '6', '7']]

class Form(QtWidgets.QWidget):
    def __init__(self):
        super(Form, self).__init__()

        # ---- 初期処理 -----
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.sub = Dialog()
        self.con = DbConnect('db.sqlite3')

        # ----- ヘッダー名称取得・セット -----
        header = self.con.get_header()
        self.ui.tbl_main.setColumnCount(len(header))
        self.ui.tbl_main.setHorizontalHeaderLabels(header)

        # ----- ヘッダーサイズセット -----
        self.ui.tbl_main.setColumnWidth(0, 35)
        self.ui.tbl_main.setColumnWidth(1, 75)
        self.ui.tbl_main.setColumnWidth(2, 45)
        self.ui.tbl_main.setColumnWidth(3, 25)
        self.ui.tbl_main.setColumnWidth(4, 25)
        self.ui.tbl_main.setColumnWidth(5, 30)
        self.ui.tbl_main.setColumnWidth(6, 100)
        self.ui.tbl_main.setColumnWidth(7, 100)
        self.ui.tbl_main.setColumnWidth(8, 90)
        self.ui.tbl_main.setColumnWidth(9, 90)
        self.ui.tbl_main.setColumnWidth(10, 70)
        self.ui.tbl_main.setColumnWidth(11, 70)

        # ----- コンボボックス初期値セット -----
        self.ui.cmb_jitikai.addItems(cmb_data[0])
        self.ui.cmb_kumi.addItems(cmb_data[1])
        self.ui.cmb_han.addItems(cmb_data[2])

    def __del__(self):
        # ウィンドウを閉じる時DBをclose
        self.con.db_close()

    def list_click(self, row):
        # 親ウィンドウよりNo取得
        item = self.ui.tbl_main.item(row, 0)
        # Noをキーにレコードを取得
        c = self.con.get_record(item.text())
        rec = c.fetchone()
        #  サブウィンドウにセット
        self.sub.input_data(rec)
        self.sub.show()

    def list_search(self):
        self.ui.tbl_main.clearContents()
        self.ui.tbl_main.setRowCount(0)
        jitikai = self.ui.cmb_jitikai.currentText()
        kumi = self.ui.cmb_kumi.currentText()
        han = self.ui.cmb_han.currentText()
        name = self.ui.txt_name.text()
        address = self.ui.txt_address.text()
        delflg = self.ui.chk_del.isChecked()
        c = self.con.get_data(jitikai, kumi, han, name, address, delflg)
        j = 0
        for row in c:
            col_count = len(row)
            self.ui.tbl_main.insertRow(j)
            for i in range(col_count):
                item = QtWidgets.QTableWidgetItem(str(row[i]))
                self.ui.tbl_main.setItem(j, i, item)
            j += 1

    def list_print(self):
        # テンプレートへ挿入するデータの作成
        data = []
        for i in range(self.ui.tbl_main.rowCount()):
            data.append({'no': str(self.ui.tbl_main.item(i, 0).text()),
                         'kbn': str(self.ui.tbl_main.item(i, 2).text()),
                         'kumi': str(self.ui.tbl_main.item(i, 3).text()),
                         'han': str(self.ui.tbl_main.item(i, 4).text()),
                         'name': str(self.ui.tbl_main.item(i, 6).text()),
                         })

        pdf = MakePdf()
        pdf.make(data)

    def jitikai_change(self):
        self.ui.cmb_kumi.clear()
        text = self.ui.cmb_jitikai.currentText()
        self.ui.cmb_kumi.addItem("")
        c = self.con.get_cmb_kumi(text)
        for row in c:
            self.ui.cmb_kumi.addItem(str(row[0]))

    def kumi_change(self):
        self.ui.cmb_han.clear()
        text = self.ui.cmb_kumi.currentText()
        self.ui.cmb_han.addItem("")
        c = self.con.get_cmb_han(text)
        for row in c:
            self.ui.cmb_han.addItem(str(row[0]))


class Dialog(QtWidgets.QDialog):
    def __init__(self):
        super(Dialog, self).__init__()
        # ---- 初期処理 -----
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def map_show(self):
        svg.load('map.svg')
        svg.show()

    def input_data(self, row):
        self.ui.lbl_no.setText(row[0])
        self.ui.txt_jitikai.setText(row[2])
        self.ui.txt_kumi.setText(row[3])
        self.ui.txt_han.setText(row[4])
        self.ui.txt_name.setText(row[6])
        self.ui.txt_address.setText(row[7])


class DbConnect:
    def __init__(self, str_db):
        con = sqlite3.connect(str_db)
        self.cur = con.cursor()

    def get_header(self):
        self.cur.execute("select * from '会員名簿'")
        header = []
        for colinfo in self.cur.description:
            header.append(colinfo[0])
        return header

    def get_record(self, no):
        sql = (
            "SELECT * FROM 会員名簿 "
            "WHERE No = :ID"
        )
        result = self.cur.execute(sql, {'ID': no})
        return result

    def get_data(self, jitikai, kumi, han, name, address, delflg):
        sql = (
            "SELECT * FROM 会員名簿 "
            "WHERE 自治会 LIKE :jitikai "
            "AND 組 LIKE :kumi "
            "AND 班 LIKE :han "
            "AND 氏名 LIKE :name "
            "AND 住所 LIKE :address "
        )
        if delflg is False:
            sql += "AND 退会年月日 == '' "

        sql += "ORDER BY 自治会, 組, 班, 世帯 "

        result = self.cur.execute(sql,
                                  {'jitikai': "%" if jitikai == "" else str(jitikai),
                                   'kumi': "%" if kumi == "" else str(kumi),
                                   'han': "%" if han == "" else str(han),
                                   'name': "%" if name == "" else "%" + str(name) + "%",
                                   'address': "%" if address == "" else "%" + str(address) + "%"})
        return result

    def get_cmb_kumi(self, jitikai):
        sql = (
            "SELECT DISTINCT 組 FROM 会員名簿 "
            "WHERE 自治会 = :jitikai "
        )
        result = self.cur.execute(sql, {'jitikai': "" if jitikai == "" else str(jitikai)})
        return result

    def get_cmb_han(self, kumi):
        sql = (
            "SELECT DISTINCT 班 FROM 会員名簿 "
            "WHERE 組 = :kumi "
        )
        result = self.cur.execute(sql, {'kumi': "" if kumi == "" else str(kumi)})
        return result

    def db_close(self):
        self.cur.close()


class PrinterView:
    def __init__(self, in_file, out_file):
        in_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.loadcnt = 0
        self.in_file = os.path.join(in_path, in_file)
        self.printer = QPrinter(QPrinter.HighResolution)
        self.printer.setOutputFileName(out_file)
        self.printer.setOutputFormat(QPrinter.PdfFormat)
        self.printer.setOrientation(QPrinter.Portrait)
        self.printer.setPaperSize(QPrinter.A4)
        self.printer.setFullPage(True)

        self.view = QWebView()
        self.view.setZoomFactor(1)

    def load(self):
        self.view.load(QUrl.fromLocalFile(self.in_file))
        self.loadcnt = 0
        self.view.loadFinished.connect(self.load_fin)

    def load_fin(self):
        if self.loadcnt == 0:
            self.view.print_(self.printer)
            check_call('list.pdf', shell=True)
        self.loadcnt += 1


class MakePdf:
    def __init__(self):
        # テンプレートファイルを指定
        self.env = Environment(loader=FileSystemLoader('./', encoding='utf8'))
        self.tpl = self.env.get_template('temp.html')

    def make(self, data):
        html = self.tpl.render({'data_list': data})
        tmpfile = open('list.html', 'w', encoding='utf-8')
        tmpfile.write(html)
        tmpfile.close()

        p.load()


class SvgMap:
    def __init__(self, file):
        self.svg = QtSvg.QSvgWidget(self, file)

    def map_show(self):
        self.svg.show()

    '''
    def __init__(self, in_file):
        in_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.file = os.path.join(in_path, in_file)
        data = open(self.file).read()
        self.svg = QtSvg.QSvgRenderer(QByteArray(data))
        self.web = QWebView()
        self.web.setRenderHint(QPainter.SmoothPixmapTransform)
        self.web.setRenderHint(QPainter.Antialiasing)
        self.web.setRenderHint(QPainter.TextAntialiasing)
        self.painter = QPainter()

    def show(self):
        self.web.load(self.file)
        self.web.loadFinished.connect(self.load_finished)

    def load_finished(self):
        self.web.resize(1024, 768)
        self.svg.render(self.painter)
    '''

if __name__ == '__main__':
    # ----- debug ------
    UiConvert('ui.ui', 'ui.py')
    UiConvert('sub.ui', 'sub.py')
    from ui import Ui_Form
    from sub import Ui_Dialog
    # ----- debug ------
    app = QtWidgets.QApplication(sys.argv)
    window = Form()
    p = PrinterView('list.html', 'list.pdf')
    svg = QtSvg.QSvgWidget()
    window.show()
    sys.exit(app.exec_())
