import os


class Auxiliar:

    @staticmethod
    def getProjectRootDir():
        # Obtém o diretório do script atual
        diretorio_atual = os.path.abspath(os.path.dirname(__file__))

        # Define o nome da pasta que você sabe que está presente no diretório raiz do projeto
        pasta_referencia = '.root'

        # Itera sobre os diretórios pais até encontrar a pasta de referência
        while not os.path.exists(os.path.join(diretorio_atual, pasta_referencia)):
            diretorio_atual = os.path.dirname(diretorio_atual)
            if diretorio_atual == os.path.dirname(diretorio_atual):
                # Chegou ao diretório raiz do sistema de arquivos
                raise FileNotFoundError(f'Pasta de referência "{pasta_referencia}" não encontrada.')

        # Retorna o diretório onde a pasta de referência foi encontrada
        return diretorio_atual

if __name__ == '__main__':
    print(Auxiliar.getProjectRootDir())
