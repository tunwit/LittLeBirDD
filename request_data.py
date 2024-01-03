import json
import portalocker
import io

class request():
    def __init__(self,fp) -> None:
        self.fp = fp
        self.f = None

    def request_access(self) -> dict:
        self.f = open(self.fp, "r+", encoding="utf-8")
        portalocker.lock(self.f, portalocker.LOCK_EX)
        data = json.load(self.f)
        self.f.seek(0)
        return data
    
    def update_access(self,data):
        self.f.seek(0)
        json.dump(data, self.f,ensure_ascii=False,indent=4) 
        portalocker.unlock(self.f)

