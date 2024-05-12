# Este módulo é responsável por importar todas as classes que representam as tabelas do banco de dados.
# Ele é utilizado no módulo con\db_session.py e no método createTables para criar as tabelas no banco de dados.
# Logo toda classe/tabela que for criada deve ser importada aqui.


from models.aditivo_nutritivo import AditivoNutritivo
from models.conservante import Conservante
from models.ingrediente import Ingrediente
from models.lote import Lote
from models.nota_fiscal import NotaFiscal
from models.picole import Picole
from models.revendedor import Revendedor
from models.sabor import Sabor
from models.tipo_embalagem import TipoEmbalagem
from models.tipo_picole import TipoPicole
from models.lote_nota_fiscal import LoteNotaFiscal
from models.aditivo_nutritivo_picole import AditivoNutritivoPicole
from models.conservante_picole import ConservantePicole
from models.ingrediente_picole import IngredientePicole
from models.lote_nota_fiscal import LoteNotaFiscal

