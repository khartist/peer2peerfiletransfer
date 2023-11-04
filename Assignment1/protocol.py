import json
import datetime
FORMAT = "utf-8"
class Encode:
    def __init__(self,ip,port) -> None:
        self.ip = ip
        self.port = port
    def requestChat(self):
        return json.dumps({
            'type':"Request",
            'flag':'S',
            'content': "{} {}".format(self.ip, self.port)
        }).encode(FORMAT)

    def closeChat(self):
        return json.dumps({
            'type':"Request",
            'flag': 'E',
        }).encode(FORMAT)

    def acceptChat(self):
        return json.dumps({
            'type':"Response",
            'code':1,
        }).encode(FORMAT)
    def declineChat(self):
        return json.dumps({
            'type':"Response",
            'code':13,
        }).encode(FORMAT)

    # Chat encode protocol
    # flag = 0, no action
    # flag = 1, send file request
    # flag = 
    def sendMessage(self,msg):
        return json.dumps({
            'type':"M",
            'flag':0,
            'time':datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            'msg':msg
        }).encode(FORMAT)

    def sendFileRequest(self, filename, filesize):
        return json.dumps({
            'type':"F",
            'flag':1,
            'time':datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            'fname': filename,
            'fsize': filesize
        }).encode(FORMAT)
    




if __name__== "__main__":
    e = Encode(1,1,2)
    print(e.requestChat('Hello'))