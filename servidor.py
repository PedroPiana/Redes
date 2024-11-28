import random
import socket
import sys
from barbaro import Barbaro
from mago import Mago
from ladino import Ladino
from clerigo import Clerigo

# comentario teste versionamento
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

    def ataqueRecebido(self, msg):

        if msg[:2] == "AD" and int(msg[2:4]) > self.getTeste(msg[4:7]):
            dano = int(msg[7:9])
        elif msg[:2] == "AM" and int(msg[2:4]) > self.classe.CA:
            dano = int(msg[4:6])
        else:
            print("Seu inimigo errou o ATAQUE, seu D20 foi: ", msg[2:4])
            dano = 0
        print("DANO RECEBIDO : ", dano)
        nova_vida = self.getVida() - dano
        self.setVida(nova_vida)
        return nova_vida

    def getVida(self):
        return self.classe.HP

    def setVida(self, novaVida):
        self.classe.HP = novaVida


def main():

    socketConexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    endereco = ("127.0.0.1", 50000)
    socketConexao.bind(endereco)
    socketConexao.listen(1)

    [jogador, _] = socketConexao.accept()

    personagem1 = Personagem(
        input("Digite o nome do Personagem 1: "),
        input("Digite a classe do Personagem 1: "),
    )

    encerrado = False

    while not encerrado:
        print("Sua vez")

        msg = personagem1.classe.ataqueAcerto()  # Atacando o Inimigo,

        jogador.send(
            msg.encode()
        )  # enviar teste ou D20 e o dano, msg = 'AD' + '18' + '30'

        retorno = jogador.recv(1)  # mensagem

        if not retorno:
            sys.exit(-1)
        retorno = retorno.decode()

        if retorno == "D":
            acaoInimigo = jogador.recv(9)  # teste ou D20 e o Dano
            acaoInimigo = acaoInimigo.decode()

            hpRestante = personagem1.ataqueRecebido(acaoInimigo)
            print("Seu HP restante: ", hpRestante)
            if hpRestante <= 0:
                jogador.send("V".encode())
                encerrado = True
                break
            # msg = 'AD' + '18' + '30'
        elif retorno == "V":
            print(f"{personagem1.nome} venceu!")
            encerrado = True
            break


if __name__ == "__main__":
    main()
