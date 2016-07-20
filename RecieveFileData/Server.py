#encodig=utf-8
# _*_ coding:utf-8 _*_
# Writer : lgy
# dateTime : 2016-07-20

# import RecieveFile
# import sys
# import socket

# class listener():
# 	def __init__(self,Host='127.0.0.1',Port=5555):
# 		try:
# 			self.mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# 			self.mysocket.bind((Host,Port))
# 		except socket.error,msg:
# 			print 'Bind failed!\nError Code :'+str(msg[0])+ " Message" + msg[1]
# 			sys.exit()
# 		# finally:
# 			# print 'Socket Bind'

# 	def startServer(self):
# 		try:
# 			self.mysocket.listen(10)
# 			print 'Server start ... ...'
# 		except socket.error ,msg:
# 			print 'Server start Failed !Error Code : '+str(msg[0]) + 'Message' + msg[1]
# 			sys.exit()
# 		whileconn = self.mysocket.accept()
# 		print 'Connected with ' + addr[0] + ':' + str(addr)

# def main():
# 	listener_now = listener()
# 	listener_now.startServer()

# if __name__ == '__main__':
# 	main()
import sys
from RecieveFile import RecieveFile as rf
import SocketServer  
from SocketServer import StreamRequestHandler as SRH  
from time import ctime  

host = '127.0.0.1'  
port = 9998  
addr = (host,port)
user = 'mysql1'
passwd = 'mysql'  
      
class Servers(SRH):  
	def handle(self):  
		print 'got connection from ',self.client_address  
		self.wfile.write('connection %s:%s at %s succeed!' % (host,port,ctime()))  
		while True:  
			data = self.request.recv(1024)  
			if not data:   
				break 
			readFile = rf()
			readFile.login(Host=self.client_address[0])
			print self.client_address,user,passwd
			print data
			readFile.getFilestoLocal(data,'/home/mysql1/anqu/analysisResault/TestFile/')
			readFile.close()
			self.request.send(data)
			# break
print 'server is running....'
server = SocketServer.ThreadingTCPServer(addr,Servers)
server.serve_forever()


