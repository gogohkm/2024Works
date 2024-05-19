import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QVBoxLayout,
                             QMessageBox, QPlainTextEdit) # 어플리케이션 핸들러와 빈 GUI 위젯
from PyQt5.QtGui import QIcon    # 아이콘 사용을 위한 모듈


class Calculator(QWidget):  # QWidget을 상속받아 Calculator 클래스를 정의

    def __init__(self):
        super().__init__()  # 부모 클래스 초기화
        self.initUI()       # 나머지 초가화는 initUI() 메서드에서 처리

    def initUI(self):

        self.te1 = QPlainTextEdit()  # 텍스트 편집기 생성
        self.te1.setReadOnly(True)  # 편집 불가능하게 설정

        self.btn1 = QPushButton('Message', self)             # 버튼 추가
        self.btn1.clicked.connect(self.activateMessage)     # 버튼 클릭 시 핸들러 함수 연결

        vbox= QVBoxLayout()         # 수직 박스 레이아웃 생성
        vbox.addWidget(self.te1)    # 텍스트 편집기를 레이아웃에 추가
        vbox.addStretch(1)          # 레이아웃을 위젯에 추가, 빈공간
        vbox.addWidget(self.btn1)   # 버튼을 레이아웃에 추가
        vbox.addStretch(1)          # 레이아웃을 위젯에 추가, 빈공간

        self.setLayout(vbox)        # 레이아웃을 위젯에 설정. 빈공간->버튼->빈공간 순으로 수직배치된 레이아웃 설정

        self.setWindowTitle('Calculator')       # 타이틀바에 'Calculator' 표시
        self.setWindowIcon(QIcon('icon.png'))   # 아이콘 설정
        self.resize(256, 256)                   # 위젯의 크기를 300x200으로 조절
        self.show()                             # 위젯을 화면에 표시

    def activateMessage(self):                      # 버튼 클릭 시 호출되는 메서드
        self.te1.appendPlainText('Button Clicked')  # 메세지가 텍스트 에디트에 출력되도록 수정
        # QMessageBox.information(self, 'information', 'Button Clicked')


if __name__ == '__main__':              # pyqt는 애플리케이션당 하나의 QApplication 객체만을 생성할 수 있음
    app = QApplication(sys.argv)        # QApplication 객체 생성
    view = Calculator()                 # Calculator 윈도우 객체 생성
    sys.exit(app.exec_())               # 이벤트 루프 실행
