import re
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QTextEdit, QFileDialog, QPushButton
from PyQt5.QtGui import QIcon, QTextCursor, QTextCharFormat, QColor, QKeySequence
from PyQt5.QtCore import Qt, QSize


class TouchScriptEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Touch Script Editor')

        # Create actions
        new_file_action = QAction('New', self)
        new_file_action.setShortcut(QKeySequence.New)
        new_file_action.triggered.connect(self.new_file)

        open_file_action = QAction('Open', self)
        open_file_action.setShortcut(QKeySequence.Open)
        open_file_action.triggered.connect(self.open_file)

        save_file_action = QAction('Save', self)
        save_file_action.setShortcut(QKeySequence.Save)
        save_file_action.triggered.connect(self.save_file)

        save_as_file_action = QAction('Save As', self)
        save_as_file_action.setShortcut(QKeySequence.SaveAs)
        save_as_file_action.triggered.connect(self.save_as_file)

        # Create toolbar
        toolbar = self.addToolBar('Toolbar')
        toolbar.setMovable(False)
        toolbar.setStyleSheet("QToolBar {border: none;}")
        toolbar.setIconSize(QSize(32, 32))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        toolbar.addAction(new_file_action)
        toolbar.addAction(open_file_action)
        toolbar.addAction(save_file_action)
        toolbar.addAction(save_as_file_action)

        # Create buttons
        new_button = QPushButton("New", self)
        new_button.move(10, 30)
        new_button.resize(70, 30)
        new_button.clicked.connect(self.new_file)

        open_button = QPushButton("Open", self)
        open_button.move(90, 30)
        open_button.resize(70, 30)
        open_button.clicked.connect(self.open_file)

        save_button = QPushButton("Save", self)
        save_button.move(170, 30)
        save_button.resize(70, 30)
        save_button.clicked.connect(self.save_file)

        save_as_button = QPushButton("Save As", self)
        save_as_button.move(250, 30)
        save_as_button.resize(70, 30)
        save_as_button.clicked.connect(self.save_as_file)

        # Create text editor
        self.editor = QTextEdit()
        self.editor.setStyleSheet('background-color: #2E2E2E; color: #FFFFFF;')
        self.editor.cursorPositionChanged.connect(self.highlight_current_line)
        self.setCentralWidget(self.editor)

        # Highlighting rules
        self.highlighting_rules = []
        self.highlighting_rules.append((r'\bwait\b', QColor('#56B6C2')))
        self.highlighting_rules.append((r'\bhold\b', QColor('#F24B3C')))
        self.highlighting_rules.append((r'\bclick\b', QColor('#FFC107')))
        self.highlighting_rules.append((r'\bswipe\b', QColor(0, 255, 45)))
        self.highlighting_rules.append((r'\bdoubleclick\b', QColor(0, 255, 0)))
        self.highlighting_rules.append((r'\btype\b', QColor(250, 0, 100)))
        self.highlighting_rules.append((r'\bhotkey\b', QColor(255, 0, 0)))

        # Set default font
        font = self.editor.document().defaultFont()
        font.setFamily('Courier New')
        font.setPointSize(15)
        self.editor.setFont(font)

        self.show()

    def new_file(self):
        self.editor.clear()

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Touch Script (*.touch)')
        if file_name:
            with open(file_name, 'r') as f:
                file_content = f.read()
                self.editor.setPlainText(file_content)

    def save_file(self):
        file_name = getattr(self, 'file_name', None)
        if file_name:
            with open(file_name, 'w') as f:
                f.write(self.editor.toPlainText())
        else:
            self.save_as_file()

    def save_as_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File As', '', 'Touch Script (*.touch)')
        if file_name:
            self.file_name = file_name
            self.save_file()

    def highlight_current_line(self):
        cursor = self.editor.textCursor()
        line_number = cursor.blockNumber()
        block = cursor.block()
        text = block.text()

        # Highlighting rules
        color = QColor('#FFFFFF')  # Default color
        for pattern, rule_color in self.highlighting_rules:
            match = re.search(pattern, text)
            if match:
                color = rule_color

        # Set current line text color
        fmt = QTextCharFormat()
        fmt.setForeground(color)
        cursor.select(QTextCursor.LineUnderCursor)
        cursor.mergeCharFormat(fmt)
        cursor.clearSelection()

    # Auto-complete
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            cursor = self.editor.textCursor()
            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.select(QTextCursor.LineUnderCursor)
            line = cursor.selectedText().strip()

            for rule in self.highlighting_rules:
                if rule[0] in line:
                    command = rule[0].replace('\\b', '').replace('\\b', '').strip()
                    self.editor.insertPlainText('\n' + command + ' ')
                    return

        super().keyPressEvent(event)

app = QApplication(sys.argv)
window = TouchScriptEditor()
sys.exit(app.exec_())
