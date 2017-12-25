from socketserver import (TCPServer as TCP, StreamRequestHandler as SRH)
from MagnetFinder import sel
import urllib.parse
class MyTCPHandler(SRH):
     
    def handle(self):

        while True:
            data=self.request.recv(1024)   #把接收的数据实例化
            if str(data).find('\\')>0: jg=sel(data.decode('gbk'))
            else : jg=sel(urllib.parse.unquote(data.decode('utf_8')))
            self.request.sendall(jg.encode('utf_8'))
            break
    
if __name__ == "__main__":
    HOST, PORT = "127.0.0.1",2333

    # 把刚才写的类当作一个参数传给ThreadingTCPServer这个类，下面的代码就创建了一个多线程socket server
    server = TCP((HOST, PORT), MyTCPHandler)

    # 启动这个server,这个server会一直运行，除非按ctrl-C停止
    server.serve_forever()


