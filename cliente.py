import random
import socket
import sys
from barbaro import Barbaro
from mago import Mago
from ladino import Ladino
from clerigo import Clerigo

bonusProeficiencia = 3

class Personagem:
    def __init__(self, nome, classe):
        self.nome = nome
        self.classe = None
        
        # Definindo a classe com base no parâmetro recebido
        if classe == "Barbaro":
            self.classe = Barbaro()
        elif classe == "Mago":
            self.classe = Mago()
        elif classe == "Ladino":
            self.classe = Ladino()
        elif classe == "Clerigo":
            self.classe = Clerigo()

    def ataqueRecebido(self , msg):
       
        if msg[:2] == "AD" and int(msg[2:4]) > self.getTeste(msg[4:7]):
            dano = int(msg[7:9])
        elif msg[:2] == "AM" and int(msg[2:4]) > self.classe.CA:  
            dano = int(msg[4:6])
        else:
            print("Seu inimigo errou o ATAQUE, seu D20 foi: ",msg[2:4])
            dano = 0
        nova_vida = self.getVida() - dano
        self.setVida(nova_vida)
        return nova_vida

        
    def getVida(self):
        return self.classe.HP
    
    def setVida(self, novaVida):
        self.classe.HP = novaVida

def main():
    jogador = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    endereco = ('127.0.0.1', 50000)
  
    jogador.connect(endereco)

    personagem2 = Personagem(input('Digite o nome do seu Personagem : '), input('Digite a classe do seu Personagem : '))

    encerrado = False
    
    while not encerrado:
        codigo = jogador.recv(1)  # Receber se ganhou ou não o Jogador 1
        if not codigo:
            sys.exit(-1)
        
        codigo = codigo.decode()
        if codigo == 'D':
            acaoInimigo = jogador.recv(9)  # Receber Ataque inimigo
            acaoInimigo = acaoInimigo.decode()

            hpRestante = personagem2.ataqueRecebido(acaoInimigo)
            print("Seu HP eh: ", hpRestante)
            if hpRestante <= 0:
                jogador.send('V'.encode())  # Envia "V" para indicar vitória
                encerrado = True
                break

            print('Sua vez')
            msg = personagem2.classe.ataqueAcerto()  # Atacar inimigo
            jogador.send(msg.encode())  # Envia a mensagem de ataque

        elif(codigo == 'V'):
            print('Cliente Ganhou/n')
            sys.exit(-2)

if __name__ == '__main__':
    main()
