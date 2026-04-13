from token_type import RESERVED_WORDS, TokenType
from mineires_token import Token

class MineiresSyntaxError(Exception):
    def __init__(self, esperado, encontrado, linha, coluna):
        self.esperado = esperado
        self.encontrado = encontrado
        self.linha = linha
        self.coluna = coluna
        super().__init__(
            f"Erro sintático na linha {linha}, coluna {coluna}: esperado '{esperado}', mas encontrou '{encontrado}'"
        )

class AnalisadorSintatico:
    def __init__(self, lista_tokens):
        self.tokens = lista_tokens
        self.posicao = 0

    def token_atual(self) -> Token:
        if self.posicao < len(self.tokens):
            return self.tokens[self.posicao]
        return self.tokens[-1]
    
    def comparar_token(self, tipo_ou_chave):
        token = self.token_atual()
        
        if isinstance(tipo_ou_chave, str) and tipo_ou_chave in RESERVED_WORDS:
            return token.tipo == RESERVED_WORDS[tipo_ou_chave]
        
        if isinstance(tipo_ou_chave, TokenType):
            return token.tipo == tipo_ou_chave
        
        if isinstance(tipo_ou_chave, int):
            return token.tipo.value == tipo_ou_chave
        
        if tipo_ou_chave == 'IDENT':
            return token.tipo == TokenType.IDENTIFIER
        
        return token.lexema == tipo_ou_chave or token.tipo.value == tipo_ou_chave

    def verificar(self, tipo_ou_chave):
        if self.comparar_token(tipo_ou_chave):
            self.posicao += 1
            return True
        else:
            token = self.token_atual()
            esperado = tipo_ou_chave
            if isinstance(tipo_ou_chave, str) and tipo_ou_chave in RESERVED_WORDS:
                esperado = f"{tipo_ou_chave} ({RESERVED_WORDS[tipo_ou_chave].name})"
            elif isinstance(tipo_ou_chave, TokenType):
                esperado = tipo_ou_chave.name
            
            raise MineiresSyntaxError(esperado, token.lexema, token.linha, token.coluna)
        
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

    def function(self):
        self.verificar('bora_cumpade')
        self.verificar('main')
        self.verificar('(')
        self.verificar(')')
        self.bloco()
        print("Analisador sintático executado com sucesso!")

    def bloco(self):
        self.verificar('simbora')
        self.stmtList()
        self.verificar('cabo')
        
    def stmtList(self):
        while not self.comparar_token('cabo') and not self.comparar_token(TokenType.EOF):
            if not self.stmt():
                token = self.token_atual()
                raise MineiresSyntaxError("um comando (roda_esse_trem, xove, etc.) ou 'cabo'", token.lexema, token.linha, token.coluna)

    def stmt(self):
        if self.comparar_token('roda_esse_trem'):
            self.forStmt()
            return True
        
        elif self.comparar_token('xove') or self.comparar_token('oia_proce_ve'):
            self.ioStmt()
            return True
        
        elif self.comparar_token('enquanto_tiver_trem'): 
            self.whileStmt()
            return True
        
        elif self.comparar_token('uai_se'):
            self.ifStmt()
            return True
        
        elif self.comparar_token('dependenu'):
            self.caseStmt()
            return True

        elif self.comparar_token('simbora'):
            self.bloco()
            return True

        elif self.comparar_token('para_o_trem') or self.comparar_token('toca_o_trem'):
            self.verificar(self.token_atual().tipo)
            self.verificar('uai')
            return True
        
        elif self.type_check():
            self.declaration()
            self.verificar('uai')
            return True

        elif self.comparar_token(TokenType.IDENTIFIER) or self.comparar_token(TokenType.LPAREN):
            self.atrib()
            self.verificar('uai')
            return True

        elif self.comparar_token('uai'):
            self.verificar('uai')
            return True

        return False

    def type_check(self):
        """Apenas verifica se o próximo token é um tipo, sem consumir."""
        tipos = {
            RESERVED_WORDS['trem_di_numeru'],
            RESERVED_WORDS['trem_cum_virgula'],
            RESERVED_WORDS['trem_discrita'],
            RESERVED_WORDS['trem_discolhe'],
            RESERVED_WORDS['trosso'],
        }
        return self.token_atual().tipo in tipos

    def type(self):
        tipos = {
            RESERVED_WORDS['trem_di_numeru'],
            RESERVED_WORDS['trem_cum_virgula'],
            RESERVED_WORDS['trem_discrita'],
            RESERVED_WORDS['trem_discolhe'],
            RESERVED_WORDS['trosso'],
        }
        if self.token_atual().tipo in tipos:
            self.posicao += 1
            return True
        else:
            token = self.token_atual()
            raise MineiresSyntaxError("um tipo de dado (trem_...)", token.lexema, token.linha, token.coluna)

    def declaration(self):
        self.type()
        self.identList()

    def identList(self):
        self.verificar('IDENT')
        self.restoIdentList()

    def restoIdentList(self):
        if self.comparar_token(','):
            self.verificar(',')
            self.verificar('IDENT')
            self.restoIdentList()

    # Comando for:
    def forStmt(self):
        self.verificar('roda_esse_trem')
        self.verificar('(')
        self.optExpr()
        self.verificar(';')
        self.optExpr()
        self.verificar(';')
        self.optExpr()
        self.verificar(';') 
        self.verificar(')')
        self.stmt()
        
    def optExpr(self):
        if self.comparar_token(TokenType.IDENTIFIER):
            self.atrib()

    # Comandos de IO
    def ioStmt(self):
        if self.comparar_token('xove'):
            self.verificar('xove')
            self.verificar('(')
            self.type()
            self.verificar(',')
            self.verificar('IDENT')
            self.verificar(')')
            self.verificar('uai')

        elif self.comparar_token('oia_proce_ve'):
            self.verificar('oia_proce_ve')
            self.verificar('(')
            self.outList()
            self.verificar(')')
            self.verificar('uai')
    
    def outList(self):
        self.out()
        self.restoOutList()

    def out(self):
        self.fatorZin()

    def restoOutList(self):
        if self.comparar_token(','):
            self.verificar(',')
            self.out()
            self.restoOutList()

    # Comando while
    def whileStmt(self):
        self.verificar('enquanto_tiver_trem')
        self.verificar('(')
        self.expr()
        self.verificar(')')
        self.stmt()

    # Comando if
    def ifStmt(self):
        self.verificar('uai_se')
        self.verificar('(')
        self.expr()
        self.verificar(')')
        self.stmt()
        self.elsePart()

    def elsePart(self):
        if self.comparar_token('uai_senao'):
            self.verificar('uai_senao')
            self.stmt()

    # Comando case
    def caseStmt(self):
        self.verificar('dependenu')
        self.verificar('(')
        self.verificar('IDENT')
        self.verificar(')')
        self.verificar('simbora')
        self.dosCasos()
        self.verificar('cabo')

    def dosCasos(self):
        self.doCaso()
        self.restoDosCasos()

    def doCaso(self): 
        self.verificar('du_casu')
        self.fatorZin()
        self.verificar(':')
        self.stmt()
    
    def restoDosCasos(self): 
        if self.comparar_token('du_casu'):
            self.doCaso()
            self.restoDosCasos()
        elif self.comparar_token('cabo'):
            return
        # else:
        #    self.verificar('default')
        #    self.verificar(':')
        #    self.stmt()

    # Expressões:
    def expr(self):
        self.atrib()

    def atrib(self):
        self.Or()
        self.restoAtrib()

    def restoAtrib(self):
        if self.comparar_token('fica_assim_entao'):
            self.verificar('fica_assim_entao')
            self.atrib()

    def Or(self):
        self.xor()
        self.restoOr()

    def restoOr(self):
        if self.comparar_token('quarque_um'):
            self.verificar('quarque_um')
            self.xor()
            self.restoOr()

    def xor(self):
        self.And()
        self.restoXor()

    def restoXor(self):
        if self.comparar_token('um_o_oto'):
            self.verificar('um_o_oto')
            self.And()
            self.restoXor()

    def And(self):
        self.Not()
        self.restoAnd()

    def restoAnd(self):
        if self.comparar_token('tamem'):
            self.verificar('tamem')
            self.Not()
            self.restoAnd()

    def Not(self):
        if self.comparar_token('vam_marca'):
            self.verificar('vam_marca')
            self.Not()
        else:
            self.rel()

    def rel(self):
        self.add()
        self.restoRel()

    def restoRel(self):
        relacionais = {'mema_coisa', 'neh_nada', '<', '<=', '>', '>='}
        for rel in relacionais:
            if self.comparar_token(rel):
                self.verificar(rel)
                self.add()
                return

    def add(self):
        self.mult()
        self.restoAdd()

    def restoAdd(self):
        if self.comparar_token("+'") or self.comparar_token('-'):
            self.verificar(self.token_atual().tipo)
            self.mult()
            self.restoAdd()

    def mult(self):
        self.uno()
        self.restoMult()

    def restoMult(self):
        if (self.comparar_token('veiz') or
            self.comparar_token('sob') or
            self.comparar_token('/') or
            self.comparar_token('%')):
            self.verificar(self.token_atual().tipo)
            self.uno()
            self.restoMult()

    def uno(self):
        if(self.comparar_token("+'") or
           self.comparar_token('-')):
            self.verificar(self.token_atual().tipo)
            self.uno()
        else:
            self.fatorZao()

    def fatorZao(self):
        if self.comparar_token('('):
            self.verificar('(')
            self.atrib()
            self.verificar(')')
        else:
            self.fatorZin()

    def fatorZin(self):
        if self.comparar_token(TokenType.STRING_LITERAL):
            self.verificar(TokenType.STRING_LITERAL)

        elif self.comparar_token(TokenType.IDENTIFIER):
            self.verificar(TokenType.IDENTIFIER)
        
        elif self.comparar_token(TokenType.NUMBER_REAL):
            self.verificar(TokenType.NUMBER_REAL)
        
        elif self.comparar_token(TokenType.NUMBER_DECIMAL):
            self.verificar(TokenType.NUMBER_DECIMAL)
        
        elif self.comparar_token(TokenType.BOOLEAN):
            self.verificar(TokenType.BOOLEAN)
        
        elif self.comparar_token(TokenType.CHAR_LITERAL):
            self.verificar(TokenType.CHAR_LITERAL)
        else:
            token = self.token_atual()
            raise MineiresSyntaxError("um valor (literal ou identificador)", token.lexema, token.linha, token.coluna)

if __name__ == "__main__":
    tokens = [
        Token('bora_cumpade', TokenType.FUNCTION_DEF, 1, 1),
        Token('main', TokenType.MAIN, 1, 14),
        Token('(', TokenType.LPAREN, 1, 19),
        Token(')', TokenType.RPAREN, 1, 20),
        Token('simbora', TokenType.BEGIN_BLOCK, 2, 1),
        Token('cabo', TokenType.END_BLOCK, 3, 1),
        Token('EOF', TokenType.EOF, 4, 1)
    ]
    sint = AnalisadorSintatico(tokens)
    try:
        sint.function()
    except MineiresSyntaxError as e:
        print(e)