import re

class checks:

    def __init__(self) -> None:
        pass
      
    def check_password(self,c_pass):
        c_pass = str(c_pass)
        message = ''
        if len(c_pass) <8:
            message = 'short'
        elif not (c_pass.isalnum):
            message= 'incorrect'
        return message
        