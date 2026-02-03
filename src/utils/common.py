import os
import json

def get_config_path():
    root_path = os.path.abspath(os.getcwd())      # Running at main.py
    config_path = os.path.join(root_path, 'src', 'config', 'config.json')
    return config_path

def load_config_json(config_path):
    
    if not os.path.exists(config_path):
        return None
    
    try:
        with open(config_path, 'r') as jsfile:
            return json.load(jsfile)
        
    except Exception as e:
        print(e)
        return None

def get_token_and_id(config):
    userinfo = config['userinfo']
    bot_token = userinfo['bot_token']
    chat_id = userinfo['chat_id']
    return bot_token, chat_id

def get_settings(config):
    settings = config['settings']
    opacity = settings['image_opacity']
    rot_speed = settings['rotation_speed']
    return opacity, rot_speed

def get_asset_path():
    """애셋 디렉토리 경로 반환"""
    root_path = os.path.abspath(os.getcwd())      # Running at main.py
    asset_path = os.path.join(root_path, 'src', 'assets')
    return asset_path

def init_config():
    """기본 설정 파일 초기화"""
    config_path = get_config_path()
    
    default_config = {
        "userinfo": {
            "bot_token": "",
            "chat_id": ""
        },
        "settings": {
            "image_opacity": 0.95,
            "rotation_speed": 0.05
        }
    }
    
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=4)