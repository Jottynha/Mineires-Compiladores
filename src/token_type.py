# Enum com os tipos de tokens da linguagem Mineires.
# Cada token identificado pelo lexer terá um tipo definido aqui.
# Utiliza-se auto para atribuir valores automaticamente, mas o importante é a semântica do nome do token.
from enum import Enum, auto

class TokenType(Enum):
    # = Condicionais =
    IF = auto()                 
    ELSE = auto()               
    ELIF = auto()               
    # = Laços =
    FOR = auto()                
    WHILE = auto()              
    # = Switch/Case =
    SWITCH = auto()             
    CASE = auto()               
    # = Fluxo =
    RETURN = auto()             
    BREAK = auto()              
    CONTINUE = auto()           
    # = Main =
    MAIN = auto()               
    # = Tipos de Dados =
    INT = auto()                
    FLOAT = auto()              
    STRING = auto()             
    BOOLEAN = auto()            
    CHAR = auto()               
    # = Booleanos =
    TRUE = auto()               
    FALSE = auto()              
    # = Sintaxe =
    BEGIN_BLOCK = auto()        
    END_BLOCK = auto()          
    # = Delimitadores =
    LBRACE = auto()             # {
    RBRACE = auto()             # }
    LPAREN = auto()             # (
    RPAREN = auto()             # )
    SEMICOLON = auto()          # uai -> ;
    COMMA = auto()              # ,
    QUOTE = auto()              # "
    SINGLE_QUOTE = auto()       # .'. -> '
    # = Operadores Relacionais =
    LESS = auto()               # <
    GREATER = auto()            # >
    LESS_EQUAL = auto()         # <=
    GREATER_EQUAL = auto()      # >=
    ASSIGN = auto()             # fica_assim_entao -> =
    NOT_EQUAL = auto()          # neh_nada -> !=
    EQUAL = auto()              # mema_coisa -> ==
    # = Operadores Lógicos =
    OR = auto()                 # quarque_um -> or
    NOT = auto()                # vam_marca -> not
    AND = auto()                # tamem -> and
    XOR = auto()                # um_o_oto -> xor
    # = Operadores Aritméticos =
    PLUS = auto()               # +'
    MINUS = auto()              # -'
    MULTIPLY = auto()           # veiz -> *
    DIVIDE = auto()             # sob -> /
    MODULO = auto()             # %
    INT_DIVIDE = auto()         # / (divisão inteira)    
    # = Entrada e Saída =
    INPUT = auto()              
    OUTPUT = auto()             
    # = Comentários =
    COMMENT_LINE = auto()       # //
    COMMENT_START = auto()      # causo -> início de comentário multilinha
    COMMENT_END = auto()        # fim_do_causo -> fim de comentário multilinha
    # = Literais =
    NUMBER_INT = auto()         # números inteiros: 0, 10, 32
    NUMBER_FLOAT = auto()       # números reais: 3.14, .92, 0.33
    NUMBER_OCTAL = auto()       # números octais: 01, 07, 017
    NUMBER_HEX = auto()         # números hexadecimais: 0x10F
    STRING_LITERAL = auto()     # strings entre ""
    CHAR_LITERAL = auto()       # caractere entre .'. .'.
    # = Identificadores =
    IDENTIFIER = auto()         
    # = Especiais =
    EOF = auto()                # fim do arquivo
    ERROR = auto()              # token de erro
    WHITESPACE = auto()         # espaços em branco (geralmente ignorado)
    NEWLINE = auto()            # nova linha

# Mapeamento de palavras reservadas para os tokens
RESERVED_WORDS = {
    # Condicionais
    "c_to_pensanu": TokenType.IF,
    "c_nao": TokenType.ELSE,
    "c_nao_c_to_pensanu": TokenType.ELIF,   
    # Laços
    "roda_esse_trem": TokenType.FOR,
    "enquanto_tiver_trem": TokenType.WHILE,
    # Switch/Case
    "dependenu": TokenType.SWITCH,
    "du_casu": TokenType.CASE,
    # Controle de Fluxo
    "ta_bao": TokenType.RETURN,
    "para_o_trem": TokenType.BREAK,
    "toca_o_trem": TokenType.CONTINUE,
    # Função Principal
    "bora_cumpade": TokenType.MAIN,
    # Tipos de Dados
    "trem_di_numeru": TokenType.INT,
    "trem_cum_virgula": TokenType.FLOAT,
    "trem_discrita": TokenType.STRING,
    "trem_discolhe": TokenType.BOOLEAN,
    "trosso": TokenType.CHAR,
    # Valores Booleanos
    "certin": TokenType.TRUE,
    "eradin": TokenType.FALSE,
    # Escopo
    "simbora": TokenType.BEGIN_BLOCK,
    "cabo": TokenType.END_BLOCK,  # cabô sem acento para facilitar
    # Operadores
    "fica_assim_entao": TokenType.ASSIGN,
    "neh_nada": TokenType.NOT_EQUAL,
    "mema_coisa": TokenType.EQUAL,
    "quarque_um": TokenType.OR,
    "vam_marca": TokenType.NOT,
    "tamem": TokenType.AND,
    "um_o_oto": TokenType.XOR,
    "veiz": TokenType.MULTIPLY,
    "sob": TokenType.DIVIDE,
    # Entrada/Saída
    "xove": TokenType.INPUT,
    "oia_proce_ve": TokenType.OUTPUT,
    # Comentários
    "causo": TokenType.COMMENT_START,
    "fim_do_causo": TokenType.COMMENT_END,
    # Delimitadores
    "uai": TokenType.SEMICOLON,
}
