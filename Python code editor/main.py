import sys
import subprocess
from PyQt5.QtGui import QFont, QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QTextEdit, QColorDialog
from PyQt5.QtCore import Qt, QRegExp
import time

class PythonHighlighter(QSyntaxHighlighter):
    keywords = ['and', 'assert', 'break', 'class', 'continue', 'def',
                'del', 'elif', 'else', 'except', 'exec', 'finally',
                'for', 'from', 'global', 'if', 'import', 'in',
                'is', 'lambda', 'not', 'or', 'pass', 'print',
                'raise', 'return', 'try', 'while', 'yield',
                'None', 'True', 'False','list','dict','tuple','set','int',
                'str','float','chr','type',
                ':', ',', '<', '==', '>', '<=', '>=', '!=', "'","'",'"','"']

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)
        self.matchingRules = []
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor('green'))
        keywordFormat.setFontWeight(QFont.Bold)

        for word in self.keywords:
            pattern = QRegExp("\\b" + word + "\\b")
            rule = (pattern, keywordFormat)
            self.matchingRules.append(rule)

        self.commentFormat = QTextCharFormat()
        self.commentFormat.setBackground(QColor("#77ff77"))
        self.commentFormat.setForeground(QColor('gray'))
        self.commentStartExpression = QRegExp("#")

    def highlightBlock(self, text):
        for pattern, format in self.matchingRules:
            expression = QRegExp(pattern)
            index = expression.indexIn(text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)
        startIndex = 0

        if self.previousBlockState() != 1:
            startIndex = self.commentStartExpression.indexIn(text)

        while startIndex >= 0:
            endIndex = text.length()
            commentLength = endIndex - startIndex
            self.setFormat(startIndex, commentLength, self.commentFormat)
            startIndex = self.commentStartExpression.indexIn(text, startIndex + commentLength)

class Main:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = QMainWindow()
        self.main_window.setFixedSize(600, 600)

        self.text_edit = QTextEdit()
        
        self.text_edit.setStyleSheet("background-color: black; color: white;font-size: 20px;") 
        self.highlighter = PythonHighlighter(self.text_edit.document())
        self.text_edit.setTextColor(QColor(Qt.white))
        self.main_window.setCentralWidget(self.text_edit)


        self.create_button()
        self.button_run.clicked.connect(self.run)
        self.text_edit.setFontPointSize(20)
    def create_button(self):
        self.button_run = QPushButton('Run', self.main_window)
        self.button_run.move(499, 569)
        self.button_run.setStyleSheet("background-color: Purple; color: white;")
    def run(self):
        self.start_time = time.time()

        self.result_text_edit = QTextEdit()
        self.result_text_edit.setFontPointSize(15)
        self.result_text_edit.setReadOnly(True)
        self.result_text_edit.setTextColor(QColor(Qt.black))
        
        self.result_window = QMainWindow()
        self.result_window.setCentralWidget(self.result_text_edit)
        self.result_text_edit.append('Loading...')

        with open("file.py", 'w') as f:
            f.write(self.text_edit.toPlainText())

        try:
            self.subprocess_result = subprocess.run("python file.py", capture_output=True, text=True, shell=True)
            self.result_text_edit.setText(self.subprocess_result.stdout)

            if self.subprocess_result.returncode != 0:
                self.result_text_edit.append('...............')
                self.result_text_edit.append('.......Error........')
                self.result_text_edit.append('...............')
        except subprocess.CalledProcessError as e:
            self.result_text_edit.setText(str(e))

        self.result_window.show()
        self.end_time = time.time()
        print("Execution time:", self.end_time - self.start_time)

if __name__ == '__main__':
    main_app = Main()
    main_app.main_window.show()
    sys.exit(main_app.app.exec_())

