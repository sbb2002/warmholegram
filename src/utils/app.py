import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QSystemTrayIcon, QMenu, QAction)
from PyQt5.QtGui import (QPainter, QColor, QPen, QRadialGradient, QIcon, QPixmap)

from utils.config import ConfigDialog
from utils.ui import WormholeWidget
from utils.api import TelegramSender


class WormholeApp:
    """메인 애플리케이션"""
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # 웜홀 위젯
        self.wormhole = WormholeWidget()
        self.wormhole.file_dropped.connect(self.handle_drop)
        
        # 텔레그램 전송기
        self.sender = TelegramSender()
        self.wormhole.add_url(self.sender.bot_token)

        # 시스템 트레이
        self.setup_tray()
        
        # 설정 확인
        if not self.sender.is_configured():
            self.show_config_dialog()
    
    def setup_tray(self):
        """시스템 트레이 설정"""
        # 아이콘 생성
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        gradient = QRadialGradient(32, 32, 30)
        gradient.setColorAt(0, QColor(200, 150, 255))
        gradient.setColorAt(1, QColor(100, 50, 200))
        painter.setBrush(gradient)
        painter.setPen(QPen(QColor(150, 100, 255), 2))
        painter.drawEllipse(2, 2, 60, 60)
        painter.end()
        
        icon = QIcon(pixmap)
        
        self.tray = QSystemTrayIcon(icon, self.app)
        
        # 트레이 메뉴
        menu = QMenu()
        
        show_action = QAction("웜홀 보이기", self.app)
        show_action.triggered.connect(self.wormhole.show)
        menu.addAction(show_action)
        
        hide_action = QAction("웜홀 숨기기", self.app)
        hide_action.triggered.connect(self.wormhole.hide)
        menu.addAction(hide_action)
        
        menu.addSeparator()
        
        config_action = QAction("설정", self.app)
        config_action.triggered.connect(self.show_config_dialog)
        menu.addAction(config_action)
        
        menu.addSeparator()
        
        quit_action = QAction("종료", self.app)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)
        
        self.tray.setContextMenu(menu)
        self.tray.show()
        
        self.tray.showMessage(
            "웜홀 전송기",
            "웜홀이 활성화되었습니다!\n파일을 드래그해서 전송하세요.",
            QSystemTrayIcon.Information,
            2000
        )
    
    def show_config_dialog(self):
        """설정 다이얼로그 표시"""
        dialog = ConfigDialog(
            current_opacity=self.wormhole.image_opacity,
            current_speed=self.wormhole.rotation_speed # 현재 속도 전달
        )
        
        # 실시간 변경 연결
        dialog.opacity_changed.connect(self.wormhole.set_opacity)
        dialog.speed_changed.connect(self.wormhole.set_rotation_speed) # 속도 연결 추가
        
        if dialog.exec_():
            self.sender = TelegramSender()
            self.wormhole.load_ui_settings_from_config()
    
    def handle_drop(self, items):
        """드롭된 항목 처리"""
        if not self.sender.is_configured():
            self.tray.showMessage(
                "설정 필요",
                "먼저 텔레그램 봇을 설정해주세요!",
                QSystemTrayIcon.Warning,
                3000
            )
            self.show_config_dialog()
            return
        
        for item in items:
            if os.path.isfile(item):
                # 파일인 경우
                ext = os.path.splitext(item)[1].lower()
                
                if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
                    success, message = self.sender.send_photo(item)
                else:
                    success, message = self.sender.send_file(item)
                
                if success:
                    self.tray.showMessage(
                        "전송 완료",
                        f"'{os.path.basename(item)}'이(가) 전송되었습니다!",
                        QSystemTrayIcon.Information,
                        2000
                    )
                else:
                    self.tray.showMessage(
                        "전송 실패",
                        message,
                        QSystemTrayIcon.Critical,
                        3000
                    )
            else:
                # 텍스트인 경우
                success, message = self.sender.send_text(item)
                
                if success:
                    self.tray.showMessage(
                        "전송 완료",
                        "텍스트가 전송되었습니다!",
                        QSystemTrayIcon.Information,
                        2000
                    )
                else:
                    self.tray.showMessage(
                        "전송 실패",
                        message,
                        QSystemTrayIcon.Critical,
                        3000
                    )
    
    def quit_app(self):
        """앱 종료"""
        self.tray.hide()
        self.app.quit()
    
    def run(self):
        """앱 실행"""
        self.wormhole.show()
        sys.exit(self.app.exec_())
