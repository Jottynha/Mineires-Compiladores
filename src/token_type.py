# Enum com os tipos de tokens da linguagem Mineires.
# Cada token identificado pelo lexer terá um tipo definido aqui.
# Utiliza-se auto para atribuir valores automaticamente, mas o importante é a semântica do nome do token.
from enum import Enum, auto

class TokenType(Enum):
    # = Condicionais =
    IF = auto()                 # uai_se
    ELSE = auto()               # uai_senao
    SWITCH = auto()             # dependenu
    CASE = auto()               # du_casu

    # = Repetição =
    FOR = auto()                # roda_esse_trem
    WHILE = auto()              # enquanto_tiver_trem
    BREAK = auto()              # para_o_trem
    CONTINUE = auto()           # toca_o_trem

    # = Funções e Retorno =
    FUNCTION_DEF = auto()       # bora_cumpade
    MAIN = auto()               # main
    RETURN = auto()             # ta_bao

    # = Entrada e Saída =
    INPUT = auto()              # xove
    OUTPUT = auto()             # oia_proce_ve

    # = Comentários =
    COMMENT_LINE = auto()       # //
    COMMENT_START = auto()      # causo -> início de comentário multilinha
    COMMENT_END = auto()        # fim_do_causo -> fim de comentário multilinha

    # = Tipos de Dados =
    INT = auto()                # trem_di_numeru
    FLOAT = auto()              # trem_cum_virgula
    STRING = auto()             # trem_discrita
    BOOLEAN = auto()            # trem_discolhe
    CHAR = auto()               # trosso

    # = Blocos e Símbolos =
    BEGIN_BLOCK = auto()        # simbora
    END_BLOCK = auto()          # cabo
    LBRACE = auto()             # {
    RBRACE = auto()             # }
    LPAREN = auto()             # (
    RPAREN = auto()             # )
    QUOTE = auto()              # ""
    LSINGLE_QUOTE = auto()      # .'
    RSINGLE_QUOTE = auto()      # '.
    SEMICOLON = auto()          # uai (;)
    COLON = auto()              # :
    COMMA = auto()              # ,

    # = Operadores Relacionais =
    EQUAL = auto()              # mema_coisa (==)
    NOT_EQUAL = auto()          # neh_nada (!=)
    ASSIGN = auto()             # fica_assim_entao (=)
    LESS = auto()               # <
    GREATER = auto()            # >
    LESS_EQUAL = auto()         # <=
    GREATER_EQUAL = auto()      # >=
    
    # = Operadores Lógicos =
    OR = auto()                 # quarque_um 
    AND = auto()                # tamem
    NOT = auto()                # vam_marca 
    XOR = auto()                # um_o_oto 

    # = Booleanos =
    TRUE = auto()               # eh
    FALSE = auto()              # num_eh

    # = Operadores Aritméticos =
    PLUS = auto()               # +'
    MINUS = auto()              # -'
    MULTIPLY = auto()           # veiz (*)
    DIVIDE = auto()             # sob (/)
    MODULO = auto()             # %
    INT_DIVIDE = auto()         # / (divisão inteira)

    # = Bases Numéricas =
    NUMBER_REAL = auto()        # numeros reais (floats)
    NUMBER_DECIMAL = auto()     # numeros decimais (ints)
    NUMBER_OCTAL = auto()       # numeros octais
    NUMBER_HEX = auto()         # numeros hexadecimais

    # = Strings =
    STRING_LITERAL = auto()     # strings entre ""
    CHAR_LITERAL = auto()       # caractere entre .'. .'.
    ESCAPE_NEWLINE = auto()     # quebra de linha
    ESCAPE_TAB = auto()         # tab
    ESCAPE_QUOTE = auto()       # aspas escapadas
    
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
    "uai_se": TokenType.IF,
    "uai_senao": TokenType.ELSE,
    "dependenu": TokenType.SWITCH,
    "du_casu": TokenType.CASE,   
    
    # Repetição
    "roda_esse_trem": TokenType.FOR,
    "enquanto_tiver_trem": TokenType.WHILE,
    "para_o_trem": TokenType.BREAK,
    "toca_o_trem": TokenType.CONTINUE,

    # Funções e Retorno
    "bora_cumpade": TokenType.FUNCTION_DEF,
    "main": TokenType.MAIN,
    "ta_bao": TokenType.RETURN,

    # Entrada/Saída
    "xove": TokenType.INPUT,
    "oia_proce_ve": TokenType.OUTPUT,

    # Comentários
    "//": TokenType.COMMENT_LINE,
    "causo": TokenType.COMMENT_START,
    "fim_do_causo": TokenType.COMMENT_END,

    # Tipos de Dados
    "trem_di_numeru": TokenType.INT,
    "trem_cum_virgula": TokenType.FLOAT,
    "trem_discrita": TokenType.STRING,
    "trem_discolhe": TokenType.BOOLEAN,
    "trosso": TokenType.CHAR,

    # Blocos e Símbolos
    "simbora": TokenType.BEGIN_BLOCK,
    "cabo": TokenType.END_BLOCK,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    '"': TokenType.QUOTE,
    # descobrir como fazer aspas
    ".'": TokenType.LSINGLE_QUOTE,
    "'.": TokenType.RSINGLE_QUOTE,
    "uai": TokenType.SEMICOLON,
    ";": TokenType.SEMICOLON,
    ":": TokenType.COLON,
    ",": TokenType.COMMA,

    # Operadores Relacionais
    "mema_coisa": TokenType.EQUAL,
    "==": TokenType.EQUAL,
    "neh_nada": TokenType.NOT_EQUAL,
    "!=": TokenType.NOT_EQUAL,
    "fica_assim_entao": TokenType.ASSIGN,
    "=": TokenType.ASSIGN,
    "<": TokenType.LESS,
    ">": TokenType.GREATER,
    "<=": TokenType.LESS_EQUAL,
    ">=": TokenType.GREATER_EQUAL,

    # Operadoeres Lógicos
    "quarque_um": TokenType.OR,
    "tamem": TokenType.AND,
    "vam_marca": TokenType.NOT,
    "!": TokenType.NOT,
    "um_o_oto": TokenType.XOR,

    # Operadores Booleanos
    "eh": TokenType.TRUE,
    "num_eh": TokenType.FALSE,
    
    # Operadores Aritméticos
    "+'": TokenType.PLUS,
    "-'": TokenType.MINUS,
    "-": TokenType.MINUS,
    "veiz": TokenType.MULTIPLY,
    "*": TokenType.MULTIPLY,
    "sob": TokenType.DIVIDE,
    "%": TokenType.MODULO,
    "/": TokenType.INT_DIVIDE,

    # Bases Numéricas: (descobrir como fazer)

    # Strings: (descobrir como fazer o resto)
    "\\n": TokenType.ESCAPE_NEWLINE,
    "\\t": TokenType.ESCAPE_TAB,
    "\\\"": TokenType.ESCAPE_QUOTE
}
