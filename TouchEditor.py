import re
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QTextEdit, QFileDialog
from PyQt5.QtGui import QIcon, QTextCursor, QTextCharFormat, QColor, QKeySequence
from PyQt5.QtCore import Qt

class TouchScriptEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Touch Script Editor')

        # Create actions
        new_file_action = QAction(QIcon('icons/new.png'), 'New', self)
        new_file_action.setShortcut(QKeySequence.New)
        new_file_action.triggered.connect(self.new_file)

        open_file_action = QAction(QIcon('icons/open.png'), 'Open', self)
        open_file_action.setShortcut(QKeySequence.Open)
        open_file_action.triggered.connect(self.open_file)

        save_file_action = QAction(QIcon('icons/save.png'), 'Save', self)
        save_file_action.setShortcut(QKeySequence.Save)
        save_file_action.triggered.connect(self.save_file)

        save_as_file_action = QAction(QIcon('icons/save-as.png'), 'Save As', self)
        save_as_file_action.setShortcut(QKeySequence.SaveAs)
        save_as_file_action.triggered.connect(self.save_as_file)

        # Create toolbar
        toolbar = self.addToolBar('Toolbar')
        toolbar.addAction(new_file_action)
        toolbar.addAction(open_file_action)
        toolbar.addAction(save_file_action)
        toolbar.addAction(save_as_file_action)

        # Create text editor
        self.editor = QTextEdit()
        self.editor.setStyleSheet('background-color: #2E2E2E; color: #FFFFFF;')
        self.editor.cursorPositionChanged.connect(self.highlight_current_line)
        self.setCentralWidget(self.editor)

        # Highlighting rules
        self.highlighting_rules = []
        self.highlighting_rules.append((r'\bwait\b\s+arg\s*\(\s*(\d+)\s*\)', QColor('#56B6C2')))
        self.highlighting_rules.append((r'\bhold\b\s+args\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', QColor('#F24B3C')))
        self.highlighting_rules.append((r'\bclick\b\s+args\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', QColor('#FFC107')))
        self.highlighting_rules.append((r'\bswipe\b\s+args\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', QColor(0, 255, 45)))
        self.highlighting_rules.append((r'\bdoubleclick\b\s+args\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)', QColor(0, 255, 0)))
        self.highlighting_rules.append((r'\btype\b\s+([^\n]+)', QColor(0, 0, 255)))
        self.highlighting_rules.append((r'\bhotkey\b\s+([^\n]+)', QColor(255, 0, 0)))

        # Set default font
        font = self.editor.document().defaultFont()
        font.setFamily('Courier New')
        font.setPointSize(15)
        self.editor.setFont(font)

        self.show()

    def new_file(self):
        self.editor.clear()

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'Touch Script (.tch);;All Files (.*)')
        if file_name:
            with open(file_name, 'r') as f:
                file_contents = f.read()
                self.editor.setPlainText(file_contents)

    def save_file(self):
        if self.current_file:
            self.save_to_file(self.current_file)
        else:
            self.save_as_file()

    def save_as_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save As', '', 'Touch Script (*.tch);;All Files (*.*)')
        if file_name:
            self.current_file = file_name
            self.save_to_file(self.current_file)

    def save_to_file(self, file_name):
        with open(file_name, 'w') as f:
            f.write(self.editor.toPlainText())

    def highlight_current_line(self):
        selection = QTextEdit.ExtraSelection()
        line_color = QColor(Qt.yellow).lighter(160)
        selection.format.setBackground(line_color)
        selection.format.setProperty(QTextCharFormat.FullWidthSelection, True)
        selection.cursor = self.editor.textCursor()
        selection.cursor.clearSelection()
        self.editor.setExtraSelections([selection])

        # Highlight syntax
        for pattern, color in self.highlighting_rules:
            regex = re.compile(pattern)
            matches = regex.finditer(self.editor.toPlainText())
            for match in matches:
                start = match.start()
                end = match.end()
                self.highlight(start, end, color)

    def highlight(self, start, end, color):
        cursor = self.editor.textCursor()
        cursor.setPosition(start)
        cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end - start)
        format = QTextCharFormat()
        format.setBackground(color)
        cursor.setCharFormat(format)

app = QApplication(sys.argv)
ex = TouchScriptEditor()
sys.exit(app.exec_())
