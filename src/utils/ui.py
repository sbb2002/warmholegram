import json
import requests
import webbrowser

from PyQt5.QtWidgets import (QApplication, QWidget)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import (QPainter, QColor, QPen, QRadialGradient, QPixmap)

from utils.common import *

class EventHandler:
    def paintEvent(self, event):
        """웜홀 그리기"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        center_x = self.width() // 2
        center_y = self.height() // 2
        
        # 안드로메다 이미지가 있으면 회전하며 그리기
        if self.andromeda_image:
            # 첫 프레임에만 디버그 출력
            if not hasattr(self, '_debug_printed'):
                print(f"✓ 안드로메다 이미지 그리기 시작! (투명도: {self.image_opacity})")
                self._debug_printed = True
            
            # 빨려들어가는 애니메이션 중이면 스케일 적용
            if self.is_animating:
                scale = 1.0 - self.animation_progress * 0.4
                opacity_mult = 1.0 - self.animation_progress
            else:
                scale = 1.0
                opacity_mult = 1.0
            
            painter.save()
            painter.translate(center_x, center_y)
            painter.rotate(self.rotation_angle)
            painter.scale(scale, scale)
            painter.translate(-center_x, -center_y)
            
            # 설정된 투명도 사용 (드래그 오버 시 더 밝게)
            if self.is_drag_over:
                painter.setOpacity(min(1.0, self.image_opacity + 0.05) * opacity_mult)
            else:
                painter.setOpacity(self.image_opacity * opacity_mult)
            
            painter.drawPixmap(0, 0, self.andromeda_image)
            painter.restore()
            
            # 빨려들어가는 효과 - 회전하는 빛
            if self.is_animating:
                for i in range(3):
                    angle_offset = self.animation_progress * 720 + i * 120
                    painter.save()
                    painter.translate(center_x, center_y)
                    painter.rotate(angle_offset)
                    
                    glow_radius = (self.wormhole_size // 2) * (1.0 - self.animation_progress)
                    glow = QRadialGradient(0, 0, glow_radius)
                    glow.setColorAt(0, QColor(100, 200, 255, int(100 * opacity_mult)))
                    glow.setColorAt(0.5, QColor(150, 100, 255, int(50 * opacity_mult)))
                    glow.setColorAt(1, QColor(200, 50, 255, 0))
                    
                    painter.setBrush(glow)
                    painter.setPen(Qt.NoPen)
                    painter.drawEllipse(int(-glow_radius), int(-glow_radius),
                                       int(glow_radius * 2), int(glow_radius * 2))
                    painter.restore()
            
            # 이미지가 있을 때는 가벼운 테두리만
            if not self.is_animating:
                painter.setPen(QPen(QColor(150, 100, 255, 150), 2))
                painter.setBrush(Qt.NoBrush)
                painter.drawEllipse(5, 5, self.wormhole_size - 10, self.wormhole_size - 10)
                
                # 드래그 오버 시 빛나는 효과
                if self.is_drag_over:
                    glow_gradient = QRadialGradient(center_x, center_y, self.wormhole_size / 2)
                    glow_gradient.setColorAt(0, QColor(100, 200, 255, 0))
                    glow_gradient.setColorAt(0.7, QColor(100, 150, 255, 30))
                    glow_gradient.setColorAt(1, QColor(150, 100, 255, 80))
                    painter.setBrush(glow_gradient)
                    painter.setPen(Qt.NoPen)
                    painter.drawEllipse(0, 0, self.wormhole_size, self.wormhole_size)
        else:
            # 이미지가 없을 때는 기존 웜홀 효과
            self.paint_default_wormhole(painter, center_x, center_y)
    
    def mousePressEvent(self, event):
        """마우스 드래그로 이동 (좌클릭), 우클릭으로 메뉴"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            self.click_time = QTimer()  # 더블클릭 감지용
    
    def mouseDoubleClickEvent(self, event):
        """더블클릭으로 텔레그램 채팅 열기"""
        if event.button() == Qt.LeftButton:
            # 드래그 위치 초기화 (이동 방지)
            self.drag_position = None
            # 텔레그램 웹 앱에서 saved messages 열기
            if self.url is not None:
                webbrowser.open(self.url)
            else:
                print("텔레그램 URL이 설정되지 않았습니다.")

    def mouseMoveEvent(self, event):
        """드래그 중 - 웜홀 위치 이동"""
        if event.buttons() == Qt.LeftButton and self.drag_position:
            self.move(event.globalPos() - self.drag_position)
    
    def mouseReleaseEvent(self, event):
        """마우스 릴리즈"""
        if event.button() == Qt.LeftButton:
            self.drag_position = None
    
    def dragEnterEvent(self, event):
        """드래그 진입"""
        if event.mimeData().hasUrls() or event.mimeData().hasText():
            self.is_drag_over = True
            event.acceptProposedAction()
    
    def dragLeaveEvent(self, event):
        """드래그 벗어남"""
        self.is_drag_over = False
    
    def dropEvent(self, event):
        """파일/텍스트 드롭"""
        self.is_drag_over = False  # 드롭 시 드래그 오버 상태 해제
        
        files = []
        text = None
        
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                files.append(url.toLocalFile())
        elif event.mimeData().hasText():
            text = event.mimeData().text()
        
        # 빨려들어가는 애니메이션 시작
        self.start_suck_animation()
        
        # 파일 전송 신호
        if files:
            self.file_dropped.emit(files)
        elif text:
            self.file_dropped.emit([text])
        
        event.acceptProposedAction()

class WormholeWidget(QWidget, EventHandler):
    """웜홀 UI 위젯"""
    file_dropped = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()

        # Config loading
        self.config_path = get_config_path()
        self.config = load_config_json(self.config_path)
        opacity, rotation_speed = get_settings(self.config)
        self.opacity = opacity
        self.rotation_speed = rotation_speed

        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAcceptDrops(True)
        
        # 웜홀 크기 및 위치
        self.wormhole_size = 150
        self.setFixedSize(self.wormhole_size, self.wormhole_size)
        
        # 화면 우측 하단에 배치
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - self.wormhole_size - 50, 
                  screen.height() - self.wormhole_size - 100)
        
        # 드래그 이동을 위한 변수
        self.drag_position = None
        
        # 애니메이션 상태
        self.is_animating = False
        self.animation_progress = 0.0
        self.pulse_value = 0.0
        self.rotation_angle = 0.0  # 회전 각도
        self.rotation_speed = 0.05  # 기본 회전 속도
        self.is_drag_over = False  # 드래그 오버 상태
        
        # 이미지 투명도 및 속도 세팅 불러오기
        # self.image_opacity = 0.95
        self.load_ui_settings_from_config()
        
        # 펄스 애니메이션 타이머
        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self.update_pulse)
        self.pulse_timer.start(30)  # 30ms마다 업데이트
        
        # 빨려들어가는 애니메이션 타이머
        self.suck_timer = QTimer()
        self.suck_timer.timeout.connect(self.update_suck_animation)
        
        # 안드로메다 이미지 로드 및 처리
        self.andromeda_image = self.load_andromeda_image()
    
        # URL
        self.url = None

    def load_ui_settings_from_config(self):
        """설정에서 투명도 및 속도 불러오기"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    settings = config['settings']
                    self.image_opacity = settings.get('image_opacity', 0.95)
                    self.rotation_speed = settings.get('rotation_speed', 0.05) # 추가
            except:
                self.image_opacity = 0.95
                self.rotation_speed = 0.05 # 기본값
    
    def set_rotation_speed(self, speed):
        """회전 속도 실시간 변경"""
        self.rotation_speed = speed
        # print(speed, self.rotation_speed)

    def update_pulse(self):
        """펄스 효과 및 회전 업데이트"""
        self.pulse_value += 0.05
        if self.pulse_value > 6.28:
            self.pulse_value = 0
        
        # 드래그 오버 상태에 따라 배수 적용
        multiplier = 3.0 if self.is_drag_over else 1.0
        
        # [수정] rotation_speed를 직접 더해줍니다. 
        # 슬라이더 값이 10이면 한 프레임에 10도씩 회전하게 됩니다.
        self.rotation_angle += (self.rotation_speed * multiplier)
        
        if self.rotation_angle >= 360:
            self.rotation_angle -= 360
        
        self.update()

    def set_opacity(self, opacity):
        """투명도 설정"""
        self.image_opacity = opacity
        self.update()
        
    def load_andromeda_image(self):
        """안드로메다 이미지 로드 및 원형 마스크 처리"""
        import os
        
        # 현재 스크립트 위치 기준으로 이미지 찾기
        asset_dir = get_asset_path()
        
        # 이미지 파일 찾기
        image_path = None
        for filename in ['andromeda.jpg', 'andromeda.png', 'galaxy.jpg', 'galaxy.png']:
            full_path = os.path.join(asset_dir, filename)
            if os.path.exists(full_path):
                image_path = full_path
                print(f"✓ 이미지 발견: {image_path}")
                break
        
        if not image_path:
            print("✗ 안드로메다 이미지를 찾을 수 없습니다.")
            print(f"  다음 위치를 확인하세요: {asset_dir}")
            print(f"  파일명: andromeda.jpg 또는 andromeda.png")
            return None
        
        # 이미지 로드
        from PyQt5.QtGui import QImage, QBrush, QRegion
        original = QPixmap(image_path)
        if original.isNull():
            print(f"✗ 이미지 로드 실패: {image_path}")
            return None
        
        print(f"✓ 이미지 로드 성공! ({original.width()}x{original.height()})")
        
        # 정사각형으로 크롭
        size = min(original.width(), original.height())
        original = original.copy(
            (original.width() - size) // 2,
            (original.height() - size) // 2,
            size, size
        )
        
        # 웜홀 크기에 맞게 조정
        original = original.scaled(
            self.wormhole_size, 
            self.wormhole_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        
        # 원형 마스크와 페이드아웃 효과 적용
        result = QPixmap(self.wormhole_size, self.wormhole_size)
        result.fill(Qt.transparent)
        
        painter = QPainter(result)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # 원형 클리핑
        from PyQt5.QtGui import QPainterPath
        path = QPainterPath()
        path.addEllipse(0, 0, self.wormhole_size, self.wormhole_size)
        painter.setClipPath(path)
        
        # 이미지 그리기
        painter.drawPixmap(0, 0, original)
        
        painter.end()
        
        print(f"✓ 안드로메다 이미지 처리 완료! (최종 크기: {result.width()}x{result.height()})")
        
        return result
    
    def update_suck_animation(self):
        """빨려들어가는 애니메이션 업데이트"""
        self.animation_progress += 0.08
        if self.animation_progress >= 1.0:
            self.animation_progress = 0.0
            self.is_animating = False
            self.suck_timer.stop()
        self.update()
    
    def start_suck_animation(self):
        """빨려들어가는 애니메이션 시작"""
        self.is_animating = True
        self.animation_progress = 0.0
        self.suck_timer.start(16)  # ~60 FPS
    
    def paint_default_wormhole(self, painter, center_x, center_y):
        """기본 웜홀 효과 (이미지 없을 때)"""
        # 펄스 효과 계산
        pulse = abs(0.8 + 0.2 * (1 + pow(abs(1 - abs((self.pulse_value % 3.14) / 3.14 - 0.5) * 2), 2)))
        
        if self.is_animating:
            # 빨려들어가는 효과
            scale = 1.0 - self.animation_progress * 0.3
            opacity = int(255 * (1.0 - self.animation_progress))
            
            # 회전하는 나선 효과
            for i in range(5):
                angle_offset = self.animation_progress * 360 * 2 + i * 72
                radius = (self.wormhole_size // 2 - 10) * scale * (1 - i * 0.1)
                
                gradient = QRadialGradient(center_x, center_y, radius)
                gradient.setColorAt(0, QColor(100, 200, 255, opacity // (i + 1)))
                gradient.setColorAt(0.5, QColor(150, 100, 255, opacity // (i + 2)))
                gradient.setColorAt(1, QColor(200, 50, 255, 0))
                
                painter.setBrush(gradient)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(int(center_x - radius), int(center_y - radius), 
                                   int(radius * 2), int(radius * 2))
        else:
            # 일반 웜홀 효과
            # 외부 링
            for i in range(3):
                radius = (self.wormhole_size // 2 - 10 - i * 8) * pulse
                
                gradient = QRadialGradient(center_x, center_y, radius)
                gradient.setColorAt(0, QColor(50, 150, 255, 30))
                gradient.setColorAt(0.7, QColor(100, 100, 255, 80))
                gradient.setColorAt(1, QColor(150, 50, 255, 0))
                
                painter.setBrush(gradient)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(int(center_x - radius), int(center_y - radius), 
                                   int(radius * 2), int(radius * 2))
            
            # 중앙 코어
            core_radius = 30 * pulse
            core_gradient = QRadialGradient(center_x, center_y, core_radius)
            core_gradient.setColorAt(0, QColor(200, 150, 255, 200))
            core_gradient.setColorAt(0.5, QColor(100, 100, 255, 150))
            core_gradient.setColorAt(1, QColor(50, 50, 200, 0))
            
            painter.setBrush(core_gradient)
            painter.drawEllipse(int(center_x - core_radius), int(center_y - core_radius),
                               int(core_radius * 2), int(core_radius * 2))
            
            # 외곽 링
            painter.setPen(QPen(QColor(150, 100, 255, 100), 3))
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(10, 10, self.wormhole_size - 20, self.wormhole_size - 20)

    def add_url(self, bot_token: str):
        
        # token을 통해 getMe로 접근하여 username을 파악
        url = f'https://api.telegram.org/bot{bot_token}/getMe'
        rsp = requests.get(url).json()

        if rsp.get("ok"):
            username = rsp["result"]["username"]
        else:
            print(f"ERR: {rsp['error_code']}")
            return None
        
        url = f"https://web.telegram.org/k/#@{username}"
        self.url = url

        print("✓ URL 설정 완료:", self.url)



