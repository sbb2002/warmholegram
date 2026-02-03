import os
import json
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, 
                             QMessageBox, QSlider)

from utils.common import *


class ConfigDialog(QDialog):
    """텔레그램 봇 설정 다이얼로그"""
    opacity_changed = pyqtSignal(float)
    speed_changed = pyqtSignal(float)  # 회전 속도 신호 추가
    
    def __init__(self, parent=None, current_opacity=0.95, current_speed=0.05):
        super().__init__(parent)
        
        # Config loading
        self.config_path = get_config_path()
        self.config = load_config_json(self.config_path)
        opacity, rotation_speed = get_settings(self.config)
        self.opacity = opacity
        self.rotation_speed = rotation_speed
        
        # Layout
        self.setWindowTitle("웜홀 설정")
        self.setFixedSize(400, 280)
        
        layout = QVBoxLayout()
        
        # Bot Token 입력 요구
        layout.addWidget(QLabel("텔레그램 봇 토큰:"))
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
        layout.addWidget(self.token_input)
        
        # Chat ID 입력 요구
        layout.addWidget(QLabel("내 Chat ID:"))
        self.chat_id_input = QLineEdit()
        self.chat_id_input.setPlaceholderText("123456789")
        layout.addWidget(self.chat_id_input)
        
        # 회전 속도 조절
        layout.addWidget(QLabel("회전 속도:"))
        speed_layout = QHBoxLayout()
        
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(0)   # 정지
        self.speed_slider.setMaximum(20)  # 최대 속도
        self.speed_slider.setValue(int(current_speed)) # 0.05 -> 5
        self.speed_slider.valueChanged.connect(self.on_speed_changed)
        
        self.speed_label = QLabel(f"{current_speed:.2f}")
        speed_layout.addWidget(self.speed_slider)
        speed_layout.addWidget(self.speed_label)
        layout.addLayout(speed_layout)

        # 투명도 조절
        layout.addWidget(QLabel("웜홀 이미지 투명도:"))
        opacity_layout = QHBoxLayout()
        
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setMinimum(10)  # 10%
        self.opacity_slider.setMaximum(100)  # 100%
        self.opacity_slider.setValue(int(current_opacity * 100))
        self.opacity_slider.setTickPosition(QSlider.TicksBelow)
        self.opacity_slider.setTickInterval(10)
        self.opacity_slider.valueChanged.connect(self.on_opacity_changed)
        
        self.opacity_label = QLabel(f"{int(current_opacity * 100)}%")
        self.opacity_label.setMinimumWidth(40)
        
        opacity_layout.addWidget(self.opacity_slider)
        opacity_layout.addWidget(self.opacity_label)
        layout.addLayout(opacity_layout)

        # 저장 버튼
        save_btn = QPushButton("저장")
        save_btn.clicked.connect(self.save_config)
        layout.addWidget(save_btn)
        
        self.setLayout(layout)
        
        # 기존 설정 로드
        self.load_existing_config()

    def on_speed_changed(self, value):
        # 0~100 정수를 0.0~1.0 실수로 변환
        speed = value
        # print("Speed", value)
        self.speed_label.setText(f"{speed}")
        self.speed_changed.emit(speed)

    def on_opacity_changed(self, value):
        """투명도 변경 시 실시간 업데이트"""
        self.opacity_label.setText(f"{value}%")
        self.opacity_changed.emit(value / 100.0)
    
    def load_existing_config(self):
        if os.path.exists(self.config_path):
            try:
                self.config = load_config_json(self.config_path)
                userinfo = get_token_and_id(self.config)
                settings = get_settings(self.config)
                
                bot_token, chat_id = userinfo
                opacity, speed = settings
                
                self.token_input.setText(bot_token)
                self.chat_id_input.setText(chat_id)
                
                # 투명도 로드
                self.opacity_slider.setValue(int(opacity * 100))
                
                # 속도 로드 (0.0~1.0 범위를 다시 0~100으로 변환)
                self.speed_slider.setValue(int(speed))
                self.speed_label.setText(f"{int(speed)}")

            except:
                pass

    def save_config(self):
        """설정 저장"""
        bot_token = self.token_input.text().strip()
        chat_id = self.chat_id_input.text().strip()
        
        if not bot_token or not chat_id:
            QMessageBox.warning(self, "오류", "모든 항목을 입력해주세요!")
            return
        
        config = {
            "userinfo": {
                "bot_token": bot_token,
                "chat_id": chat_id
            },
            "settings": {
                "image_opacity": self.opacity_slider.value() / 100.0,
                "rotation_speed": self.speed_slider.value()
            }
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=4)
        
        QMessageBox.information(self, "완료", "설정이 저장되었습니다!")
        self.accept()
