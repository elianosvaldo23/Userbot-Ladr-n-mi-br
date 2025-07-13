import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    @classmethod
    def get_api_id(cls):
        return os.getenv('API_ID')
    
    @classmethod
    def get_api_hash(cls):
        return os.getenv('API_HASH')
    
    @classmethod
    def get_phone_number(cls):
        return os.getenv('PHONE_NUMBER')
    
    @classmethod
    def get_session_name(cls):
        return os.getenv('SESSION_NAME', 'userbot_session')
    
    # Properties for backward compatibility
    @property
    def API_ID(self):
        return self.get_api_id()
    
    @property
    def API_HASH(self):
        return self.get_api_hash()
    
    @property
    def PHONE_NUMBER(self):
        return self.get_phone_number()
    
    @property
    def SESSION_NAME(self):
        return self.get_session_name()
    
    @classmethod
    def validate(cls):
        api_id = cls.get_api_id()
        api_hash = cls.get_api_hash()
        phone_number = cls.get_phone_number()
        
        if not api_id:
            raise ValueError("API_ID is required")
        if not api_hash:
            raise ValueError("API_HASH is required")
        if not phone_number:
            raise ValueError("PHONE_NUMBER is required")
        
        return True
