import os
import json
import requests

from utils.common import *

class TelegramSender:
    """텔레그램 전송 클래스"""
    def __init__(self):
        self.config_path = get_config_path()
        self.config = load_config_json(self.config_path)
        bot_token, chat_id = get_token_and_id(self.config)
        
        self.bot_token = bot_token
        self.chat_id = chat_id

    def load_config(self):
        """설정 로드"""
        if not os.path.exists(self.config_path):
            return None
        
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except:
            return None
    
    def is_configured(self):
        """설정 여부 확인"""
        return (self.bot_token is not None) and (self.chat_id is not None)
    
    def send_file(self, file_path):
        """파일 전송"""
        if not self.is_configured():
            return False, "텔레그램 봇이 설정되지 않았습니다."
        
        url = f"https://api.telegram.org/bot{self.bot_token}/sendDocument"
        
        try:
            with open(file_path, 'rb') as f:
                files = {'document': f}
                data = {'chat_id': self.chat_id}
                response = requests.post(url, files=files, data=data, timeout=30)
                
                if response.status_code == 200:
                    return True, "전송 성공!"
                else:
                    return False, f"전송 실패: {response.text}"
        except Exception as e:
            return False, f"오류: {str(e)}"
    
    def send_photo(self, photo_path):
        """사진 전송"""
        if not self.is_configured():
            return False, "텔레그램 봇이 설정되지 않았습니다."
        
        url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
        
        try:
            with open(photo_path, 'rb') as f:
                files = {'photo': f}
                data = {'chat_id': self.chat_id}
                response = requests.post(url, files=files, data=data, timeout=30)
                
                if response.status_code == 200:
                    return True, "전송 성공!"
                else:
                    return False, f"전송 실패: {response.text}"
        except Exception as e:
            return False, f"오류: {str(e)}"
    
    def send_text(self, text):
        """텍스트 전송"""
        if not self.is_configured():
            return False, "텔레그램 봇이 설정되지 않았습니다."
        
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        
        try:
            data = {
                'chat_id': self.chat_id,
                'text': text
            }
            response = requests.post(url, data=data, timeout=30)
            
            if response.status_code == 200:
                return True, "전송 성공!"
            else:
                return False, f"전송 실패: {response.text}"
        except Exception as e:
            return False, f"오류: {str(e)}"
