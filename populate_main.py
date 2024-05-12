from time import sleep

from tqdm import tqdm  # pip install tqdm
from sqlalchemy.orm import Session

from conf.helpers import gerar_string, gerar_int, gerar_float, gerar_cor
from conf.db_session import createSession
from models.aditivo_nutritivo import AditivoNutritivo
from models.aditivo_nutritivo_picole import AditivoNutritivoPicole
from models.conservante_picole import ConservantePicole
from models.ingrediente_picole import IngredientePicole
from models.sabor import Sabor
from models.tipo_embalagem import TipoEmbalagem
from models.tipo_picole import TipoPicole
from models.ingrediente import Ingrediente
from models.conservante import Conservante
from models.revendedor import Revendedor
from models.lote import Lote
from models.nota_fiscal import NotaFiscal
from models.picole import Picole
from models.lote_nota_fiscal import LoteNotaFiscal


# 1) Aditivos Nutritivos
def populate_aditivo_nutritivo():
    print(f'Cadastrando Aditivo Nutritivo: ')

    # Estamos criando a sessão antes pois vamos inserir vários objetos
    session: Session = createSession()
    cor = gerar_cor()
    for n in tqdm(range(1, 101), desc='Cadastrando...', colour=cor):
        nome: str = gerar_string()
        formula_quimica: str = gerar_string(frase=True)

        aditivo_nutritivo: AditivoNutritivo = AditivoNutritivo(nome=nome, formula_quimica=formula_quimica)
        session.add(aditivo_nutritivo)
        sleep(0.05)

    # Perceba que estamos executando o commit somente no final. Desta forma os 100 dados serão enviados em um único batch para o banco
    session.commit()
    print('Aditivos Nutritivos cadastrados com sucesso')


# 2) Sabores
def populate_sabor():
    print(f'Cadastrando Sabores: ')

    # Estamos criando a sessão antes pois vamos inserir vários objetos
    session: Session = createSession()
    cor = gerar_cor()
    for n in tqdm(range(1, 101), desc='Cadastrando...', colour=cor):
        nome: str = gerar_string()

        sabor: Sabor = Sabor(nome=nome)
        session.add(sabor)
        sleep(0.05)

    # Perceba que estamos executando o commit somente no final. Desta forma os 100 dados serão enviados em um único batch para o banco
    session.commit()
    print('Sabores cadastrados com sucesso')


# 3) Tipos Embalagem
def populate_tipo_embalagem():
    print(f'Cadastrando Tipos Embalagem: ')

    # Estamos criando a sessão antes pois vamos inserir vários objetos
    session: Session = createSession()
    cor = gerar_cor()
    for n in tqdm(range(1, 101), desc='Cadastrando...', colour=cor):
        nome: str = gerar_string()

        tipo_embalagem: TipoEmbalagem = TipoEmbalagem(nome=nome)
        session.add(tipo_embalagem)
        sleep(0.05)

    # Perceba que estamos executando o commit somente no final. Desta forma os 100 dados serão enviados em um único batch para o banco
    session.commit()
    print('Tipos Embalagem cadastrados com sucesso')


# 4) Tipos Picole
def populate_tipo_picole():
    print(f'Cadastrando Tipos Picolé: ')

    # Estamos criando a sessão antes pois vamos inserir vários objetos
    session: Session = createSession()
    cor = gerar_cor()
    for n in tqdm(range(1, 101), desc='Cadastrando...', colour=cor):
        nome: str = gerar_string()

        tipo_picole: TipoPicole = TipoPicole(nome=nome)
        session.add(tipo_picole)
        sleep(0.05)

    # Perceba que estamos executando o commit somente no final. Desta forma os 100 dados serão enviados em um único batch para o banco
    session.commit()
    print('Tipos Picolé cadastrados com sucesso')


# 5) Ingredientes
def populate_ingrediente():
    print(f'Cadastrando Ingredientes: ')

    # Estamos criando a sessão antes pois vamos inserir vários objetos
    session: Session = createSession()
    cor = gerar_cor()
    for n in tqdm(range(1, 101), desc='Cadastrando...', colour=cor):
        nome: str = gerar_string()

        ingrediente: Ingrediente = Ingrediente(nome=nome)
        session.add(ingrediente)
        sleep(0.05)

    # Perceba que estamos executando o commit somente no final. Desta forma os 100 dados serão enviados em um único batch para o banco
    session.commit()
    print('Ingredientes cadastrados com sucesso')


# 6) Conservantes
def populate_conservante():
    print(f'Cadastrando Conservantes: ')

    # Estamos criando a sessão antes pois vamos inserir vários objetos
    session: Session = createSession()
    cor = gerar_cor()
    for n in tqdm(range(1, 101), desc='Cadastrando...', colour=cor):
        nome: str = gerar_string()
        descricao: str = gerar_string(frase=True)

        conservante: Conservante = Conservante(nome=nome, descricao=descricao)
        session.add(conservante)
        sleep(0.05)

        # Perceba que estamos executando o commit somente no final. Desta forma os 100 dados serão enviados em um único batch para o banco
        session.commit()
    print('Conservantes cadastrados com sucesso')


# 7) Revendedor
def populate_revendedor():
    print(f'Cadastrando Revendedores: ')

    # Estamos criando a sessão antes pois vamos inserir vários objetos
    session: Session = createSession()
    cor = gerar_cor()
    for n in tqdm(range(1, 101), desc='Cadastrando...', colour=cor):
        nome: str = gerar_string()
        cnpj: str = gerar_string()
        razao_social: str = gerar_string()
        contato: str = gerar_string()

        revendedor: Revendedor = Revendedor(nome=nome, cnpj=cnpj, razao_social=razao_social, contato=contato)
        session.add(revendedor)
        sleep(0.05)

    # Perceba que estamos executando o commit somente no final. Desta forma os 100 dados serão enviados em um único batch para o banco
    session.commit()
    print('Revendedores cadastrados com sucesso')


# 8) Lote
def populate_lote():
    print(f'Cadastrando Lotes: ')

    # Estamos criando a sessão antes pois vamos inserir vários objetos
    session: Session = createSession()
    cor = gerar_cor()
    for n in tqdm(range(1, 101), desc='Cadastrando...', colour=cor):
        picole_fk: int = gerar_int()
        quantidade: int = gerar_int()

        lote: Lote = Lote(picole_fk=picole_fk, quantidade=quantidade)
        session.add(lote)
        sleep(0.05)

    # Perceba que estamos executando o commit somente no final. Desta forma os 100 dados serão enviados em um único batch para o banco
    session.commit()
    print('Lotes cadastrados com sucesso')


# 9) Nota Fiscal
def populate_nota_fiscal():
    print(f'Cadastrando Notas Fiscais: ')

    # Estamos criando a sessão antes pois vamos inserir vários objetos
    session: Session = createSession()
    cor = gerar_cor()
    for n in tqdm(range(1, 101), desc='Cadastrando...', colour=cor):
        valor: float = gerar_float(digitos=3)
        numero_serie: str = gerar_string()
        descricao: str = gerar_string(frase=True)
        revendedor_fk: int = gerar_int()

        nota_fiscal: NotaFiscal = NotaFiscal(valor=valor, numero_serie=numero_serie, descricao=descricao,
                                             revendedor_fk=revendedor_fk)
        session.add(nota_fiscal)
        sleep(0.05)

    # Perceba que estamos executando o commit somente no final. Desta forma os 100 dados serão enviados em um único batch para o banco
    session.commit()
    print('Notas Fiscais cadastradas com sucesso')


# 10) Piole
def populate_picole():
    print(f'Cadastrando Picolés: ')

    # Estamos criando a sessão antes pois vamos inserir vários objetos
    session: Session = createSession()
    cor = gerar_cor()
    for n in tqdm(range(1, 101), desc='Cadastrando...', colour=cor):
        preco: float = gerar_float()
        sabor_fk: int = gerar_int()
        tipo_embalagem_fk: int = gerar_int()
        tipo_picole_fk: int = gerar_int()

        sabor_tipoPicole_tipoEmbalagem = f'{sabor_fk}_{tipo_picole_fk}_{tipo_embalagem_fk}'
        picole: Picole = Picole(preco=preco,
                                sabor_fk=sabor_fk,
                                tipo_embalagem_fk=tipo_embalagem_fk,
                                tipo_picole_fk=tipo_picole_fk,
                                sabor_tipoPicole_tipoEmbalagem=sabor_tipoPicole_tipoEmbalagem)

        # # Ingredientes
        # for n in range(5):
        #     nome: str = gerar_string()
        #     ingrediente: Ingrediente = Ingrediente(nome=nome)
        #     picole.ingredientes.append(ingrediente)
        #
        # op = gerar_float()
        # if op > 5:
        #     for _ in range(3):
        #         # Aditivos Nutritivos
        #         nome: str = gerar_string()
        #         formula_quimica: str = gerar_string(frase=True)
        #         aditivo_nutritivo: AditivoNutritivo = AditivoNutritivo(nome=nome, formula_quimica=formula_quimica)
        #         picole.aditivos_nutritivos.append(aditivo_nutritivo)
        # else:
        #     for _ in range(3):
        #         # Conservantes
        #         nome: str = gerar_string()
        #         descricao: str = gerar_string(frase=True)
        #         conservante: Conservante = Conservante(nome=nome, descricao=descricao)
        #         picole.conservantes.append(conservante)

        session.add(picole)
        sleep(0.05)

    # Perceba que estamos executando o commit somente no final. Desta forma os 100 dados serão enviados em um único batch para o banco
    session.commit()
    print('Picolés cadastrados com sucesso')


def populate_ingrediente_picole():
    print(f'Cadastrando Ingredientes Picolé: ')

    # Estamos criando a sessão antes pois vamos inserir vários objetos
    session: Session = createSession()
    cor = gerar_cor()
    chave = []
    for n in tqdm(range(1, 101), desc='Cadastrando...', colour=cor):
        picole_fk: int = gerar_int()
        ingrediente_fk: int = gerar_int()
        ingrediente_picole2 = f'{ingrediente_fk}-{picole_fk}'
        if ingrediente_picole2 in chave:
            continue
        chave.append(ingrediente_picole2)
        ingrediente_picole: IngredientePicole = IngredientePicole(picole_fk=picole_fk,
                                                                  ingrediente_fk=ingrediente_fk,
                                                                  ingrediente_picole=ingrediente_picole2)
        session.add(ingrediente_picole)
        sleep(0.05)

    # Perceba que estamos executando o commit somente no final. Desta forma os 100 dados serão enviados em um único batch para o banco
    session.commit()
    print('Ingredientes Picolé cadastrados com sucesso')


def populate_conservante_picole():
    print(f'Cadastrando Conservantes Picolé: ')

    # Estamos criando a sessão antes pois vamos inserir vários objetos
    session: Session = createSession()
    cor = gerar_cor()
    chaves = []
    for n in tqdm(range(1, 101), desc='Cadastrando...', colour=cor):
        picole_fk: int = gerar_int()
        conservante_fk: int = gerar_int()
        conservante_picole1 = f'{conservante_fk}-{picole_fk}'
        if conservante_picole1 in chaves:
            continue
        chaves.append(conservante_picole1)
        conservante_picole: ConservantePicole = ConservantePicole(picole_fk=picole_fk,
                                                                  conservante_fk=conservante_fk,
                                                                  conservante_picole=conservante_picole1)
        session.add(conservante_picole)
        sleep(0.05)

    # Perceba que estamos executando o commit somente no final. Desta forma os 100 dados serão enviados em um único batch para o banco
    session.commit()
    print('Conservantes Picolé cadastrados com sucesso')


def populate_aditivo_nutritivo_picole():
    print(f'Cadastrando Aditivos Nutritivos Picolé: ')

    # Estamos criando a sessão antes pois vamos inserir vários objetos
    session: Session = createSession()
    cor = gerar_cor()
    chave = []
    for n in tqdm(range(1, 101), desc='Cadastrando...', colour=cor):
        picole_fk: int = gerar_int()
        aditivo_nutritivo_fk: int = gerar_int()
        picole_aditivo_nutritivo = f'{picole_fk}-{aditivo_nutritivo_fk}'
        if picole_aditivo_nutritivo in chave:
            continue
        chave.append(picole_aditivo_nutritivo)
        aditivo_nutritivo_picole: AditivoNutritivoPicole = AditivoNutritivoPicole(picole_fk=picole_fk,
                                                                                  aditivo_nutritivo_fk=aditivo_nutritivo_fk,
                                                                                  picole_aditivo_nutritivo=picole_aditivo_nutritivo)
        session.add(aditivo_nutritivo_picole)
        sleep(0.05)

    # Perceba que estamos executando o commit somente no final. Desta forma os 100 dados serão enviados em um único batch para o banco
    session.commit()
    print('Aditivos Nutritivos Picolé cadastrados com sucesso')


def lote_notas_fiscal():
    print(f'Cadastrando Lote Nota Fiscal: ')

    # Estamos criando a sessão antes pois vamos inserir vários objetos
    session: Session = createSession()
    cor = gerar_cor()
    chave = []
    chave_lote = []
    for n in tqdm(range(1, 101), desc='Cadastrando...', colour=cor):
        lote_fk: int = gerar_int()
        nota_fiscal_fk: int = gerar_int()
        lote_nota_fiscal1 = f'{lote_fk}-{nota_fiscal_fk}'
        if lote_fk in chave_lote:
            continue
        chave_lote.append(lote_fk)
        if lote_nota_fiscal1 in chave:
            continue
        chave.append(lote_nota_fiscal1)
        lote_nota_fiscal: LoteNotaFiscal = LoteNotaFiscal(nota_fiscal_fk=nota_fiscal_fk,
                                                          lote_fk=lote_fk,
                                                          lote_nota_fiscal=lote_nota_fiscal1
                                                          )
        session.add(lote_nota_fiscal)
        sleep(0.05)


    # Perceba que estamos executando o commit somente no final. Desta forma os 100 dados serão enviados em um único batch para o banco
    session.commit()


    print('Lote Nota Fiscal cadastrados com sucesso')


def popular():
    # 1) Aditivos Nutritivos
    populate_aditivo_nutritivo()

    # 2) Sabores
    populate_sabor()

    # 3) Tipos Embalagem
    populate_tipo_embalagem()

    # 4) Tipos Picole
    populate_tipo_picole()

    # 5) Ingredientes
    populate_ingrediente()

    # 6) Conservantes (Deixando vazio para poder verificar resultados em tabelas vazias)
    populate_conservante()

    # 7) Revendedores
    populate_revendedor()

    # 8) Notas Fiscais
    populate_nota_fiscal()

    # 9) Picole
    populate_picole()

    # 10) Lotes
    populate_lote()

    # 11) Ingredientes Picolé
    populate_ingrediente_picole()

    # 12) Conservantes Picolé
    populate_conservante_picole()

    # 13) Aditivos Nutritivos Picolé
    populate_aditivo_nutritivo_picole()

    # 14) Lote Nota Fiscal
    lote_notas_fiscal()


if __name__ == '__main__':
    popular()
