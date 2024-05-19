import sys
from PyQt5.QtWidgets import QApplication, QWidget  # 어플리케이션 핸들러와 빈 GUI 위젯


class Calculator(QWidget): # QWidget을 상속받아 Calculator 클래스를 정의

    def __init__(self):
        super().__init__()  # 부모 클래스 초기화
        self.initUI()       # 나머지 초가화는 initUI() 메서드에서 처리
    def initUI(self):
        self.setWindowTitle('Calculator')     # 타이틀바에 'Calculator' 표시
        self.setGeometry(100, 100, 300, 400)  # 위치와 크기 설정
        self.show()                           # 위젯을 화면에 표시


if __name__ == '__main__':            # pyqt는 애플리케이션당 하나의 QApplication 객체만을 생성할 수 있음
    app = QApplication(sys.argv)      # QApplication 객체 생성
    calculator = Calculator()         # Calculator 윈도우 객체 생성
    sys.exit(app.exec_())             # 이벤트 루프 실행
    