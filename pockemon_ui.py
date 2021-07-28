from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QTextEdit, QLabel, QBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QSoundEffect


class PockeMonGame(QWidget):
    def __init__(self):
        self.callback = None
        QWidget.__init__(self)
        self.setWindowTitle("Pokemon")
        self.init_ui()
        self.inputCmdEdit.setFocusPolicy(Qt.StrongFocus)
        self.inputCmdEdit.returnPressed.connect(self.on_click)

    def setCallBack(self, callback) :
        self.callback = callback
    
    def on_click(self) :
        if self.callback != None:
            self.callback(self.inputCmdEdit.text())

    def addStory(self, story) :
        self.storyText.append(story)

    def addStatus(self, story):
        self.status.append(story)

    def addMetList(self, story):
        self.metList.append(story)

    def changeImage(self, location):
        pixmap = QPixmap(location)
        resized = pixmap.scaled(600, 400)
        self.imageLabel.setPixmap(resized)

    def addSoundEffect(self, location):
        sound = QSoundEffect(self)
        sound.setSource(QUrl.fromLocalFile(location))
        sound.play()

    def changeImage_pokemon(self, location):
        pixmap = QPixmap(location)
        resized = pixmap.scaled(400, 400)
        self.imageLabel.setPixmap(resized)
        self.imageLabel.setAlignment(Qt.AlignCenter)

    def clearCommandEdit(self) :
        self.inputCmdEdit.setText("")

    def init_ui(self):
        self.setMinimumWidth(600)
        self.setMinimumHeight(800)

        topLayout = QBoxLayout(QBoxLayout.TopToBottom)
        bottomLayout = QBoxLayout(QBoxLayout.LeftToRight)
        bottomRightLayout = QBoxLayout(QBoxLayout.TopToBottom)
        self.imageLabel = QLabel()
        pixmap = QPixmap("./pokemon_image/title.png")
        resized = pixmap.scaled(600, 400)
        self.imageLabel.setPixmap(resized)

        self.storyText = QTextEdit()
        self.status = QTextEdit()
        self.metList = QTextEdit()
        self.storyText.setReadOnly(True)
        self.status.setReadOnly(True)
        self.metList.setReadOnly(True)

        topLayout.addWidget(self.imageLabel)
        bottomRightLayout.addWidget(self.status)
        bottomRightLayout.addWidget(self.metList)

        bottomLayout.addWidget(self.storyText, 3)
        bottomLayout.addLayout(bottomRightLayout, 1)


        # setGeometry(x, y, width, height)
        inputLayout = QBoxLayout(QBoxLayout.LeftToRight)
        self.inputCmdEdit = QLineEdit()
        self.inputCmdEdit.setPlaceholderText('명령어 입력')

        self.inputBtn = QPushButton('입력')
        self.inputBtn.setToolTip('명령어를 입력하세요')
        self.inputBtn.clicked.connect(self.on_click)

        inputLayout.addWidget(self.inputCmdEdit)
        inputLayout.addWidget(self.inputBtn)
        
        rootLayout = QBoxLayout(QBoxLayout.TopToBottom)
        rootLayout.addLayout(topLayout)
        rootLayout.addLayout(bottomLayout)
        rootLayout.addLayout(inputLayout)

        self.setLayout(rootLayout)
