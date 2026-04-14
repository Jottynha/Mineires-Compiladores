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
        self.trilha = []
        self.erro = None

    def token_atual(self) -> Token:
        if self.posicao < len(self.tokens):
            return self.tokens[self.posicao]
        if self.tokens:
            return self.tokens[-1]
        return Token('EOF', TokenType.EOF, 0, 0)

    def _trace(self, mensagem):
        self.trilha.append(mensagem)

    def _entrar(self, regra):
        token = self.token_atual()
        self._trace(f"ENTRAR {regra} | pos={self.posicao} | atual={token.lexema} ({token.tipo.name})")

    def _aceitar_terminador(self):
        if self.comparar_token('uai'):
            self.verificar('uai')
            return True
        if self.comparar_token(';'):
            self.verificar(';')
            return True
        return False
    
    def exigir_terminador(self):
        if not self._aceitar_terminador():
            token = self.token_atual()
            raise MineiresSyntaxError("terminador ('uai' ou ';')", token.lexema, token.linha, token.coluna)

    def _inicio_tipo(self):
        return self.token_atual().tipo in {
            RESERVED_WORDS['trem_di_numeru'],
            RESERVED_WORDS['trem_cum_virgula'],
            RESERVED_WORDS['trem_discrita'],
            RESERVED_WORDS['trem_discolhe'],
            RESERVED_WORDS['trosso'],
        }

    def _inicio_expr(self):
        return self.token_atual().tipo in {
            TokenType.IDENTIFIER,
            TokenType.STRING_LITERAL,
            TokenType.CHAR_LITERAL,
            TokenType.NUMBER_REAL,
            TokenType.NUMBER_DECIMAL,
            TokenType.TRUE,
            TokenType.FALSE,
            TokenType.LPAREN,
            TokenType.NOT,
            TokenType.PLUS,
            TokenType.MINUS,
        }

    def get_trilha(self):
        return self.trilha
    
    def comparar_token(self, tipo_ou_chave):
        token = self.token_atual()
        
        if isinstance(tipo_ou_chave, str) and tipo_ou_chave in RESERVED_WORDS:
            return token.tipo.value == RESERVED_WORDS[tipo_ou_chave].value
        
        if isinstance(tipo_ou_chave, TokenType):
            return token.tipo.value == tipo_ou_chave.value
        
        if isinstance(tipo_ou_chave, int):
            return token.tipo.value == tipo_ou_chave
        
        if tipo_ou_chave == 'IDENT':
            return token.tipo.value == TokenType.IDENTIFIER.value
        
        #return token.lexema == tipo_ou_chave or token.tipo.value == tipo_ou_chave
        
        return False
        
        
    def verificar(self, tipo_ou_chave):
        if self.comparar_token(tipo_ou_chave):
            token = self.token_atual()
            self._trace(f"CONSUMIR OK | pos={self.posicao} | esperado={tipo_ou_chave} | encontrado={token.lexema} ({token.tipo.name})")
            self.posicao += 1
            return True
        else:
            token = self.token_atual()
            esperado = tipo_ou_chave
            if isinstance(tipo_ou_chave, str) and tipo_ou_chave in RESERVED_WORDS:
                esperado = f"{tipo_ou_chave} ({RESERVED_WORDS[tipo_ou_chave].name})"
            elif isinstance(tipo_ou_chave, TokenType):
                esperado = tipo_ou_chave.name
            
            self._trace(f"CONSUMIR FALHOU | pos={self.posicao} | esperado={esperado} | encontrado={token.lexema} ({token.tipo.name})")
            raise MineiresSyntaxError(esperado, token.lexema, token.linha, token.coluna)
        
    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=- #

    def function(self):
        self._entrar('function')
        self.erro = None
        self.verificar('bora_cumpade')
        self.verificar('main')
        self.verificar('(')
        self.verificar(')')
        self.bloco()
        self.verificar(TokenType.EOF)
        self._trace('SUCESSO análise sintática finalizada')
        print("Analisador sintático executado com sucesso!")
        return True

    def bloco(self):
        self._entrar('bloco')
        self.verificar('simbora')
        self.stmtList()
        self.verificar('cabo')
        
    def stmtList(self):
        self._entrar('stmtList')
        while not self.comparar_token('cabo') and not self.comparar_token(TokenType.EOF):
            if not self.stmt():
                token = self.token_atual()
                raise MineiresSyntaxError("um comando (roda_esse_trem, xove, etc.) ou 'cabo'", token.lexema, token.linha, token.coluna)

    def stmt(self):
        self._entrar('stmt')
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
            self.exigir_terminador()
            return True
        
        elif self._inicio_tipo():
            self.declaration()
            return True

        elif self.comparar_token('fica_assim_entao'):
            self.atrib()
            self.exigir_terminador()
            return True

        elif self._inicio_expr():
            self.atrib()
            self.exigir_terminador()
            return True

        elif self.comparar_token('uai') or self.comparar_token(';'):
            self._aceitar_terminador()
            return True

        return False

    def type_check(self):
        """Apenas verifica se o próximo token é um tipo, sem consumir."""
        return self._inicio_tipo()

    def type(self):
        self._entrar('type')
        tipos = {
            RESERVED_WORDS['trem_di_numeru'],
            RESERVED_WORDS['trem_cum_virgula'],
            RESERVED_WORDS['trem_discrita'],
            RESERVED_WORDS['trem_discolhe'],
            RESERVED_WORDS['trosso'],
        }
        if self.token_atual().tipo in tipos:
            token = self.token_atual()
            self._trace(f"CONSUMIR OK | pos={self.posicao} | esperado=TYPE | encontrado={token.lexema} ({token.tipo.name})")
            self.posicao += 1
            return True
        else:
            token = self.token_atual()
            raise MineiresSyntaxError("um tipo de dado (trem_...)", token.lexema, token.linha, token.coluna)

    def declaration(self):
        self._entrar('declaration')
        self.type()
        self.identList()
        self.exigir_terminador()

    def identList(self):
        self._entrar('identList')
        self.verificar('IDENT')
        self.restoIdentList()

    def restoIdentList(self):
        if self.comparar_token(','):
            self.verificar(',')
            self.verificar('IDENT')
            self.restoIdentList()

    # Comando for:
    def forStmt(self):
        self._entrar('forStmt')
        self.verificar('roda_esse_trem')
        self.verificar('(')
        self.optExpr()
        self.verificar(';')
        self.optExpr()
        self.verificar(';')
        self.optExpr()
        self.verificar(')')
        self.stmt()
        
    def optExpr(self):
        self._entrar('optExpr')
        if self._inicio_expr():
            self.atrib()

    # Comandos de IO
    def ioStmt(self):
        self._entrar('ioStmt')
        if self.comparar_token('xove'):
            self.verificar('xove')
            self.verificar('(')
            self.type()
            self.verificar(',')
            self.verificar('IDENT')
            self.verificar(')')
            self.exigir_terminador()

        elif self.comparar_token('oia_proce_ve'):
            self.verificar('oia_proce_ve')
            self.verificar('(')
            self.outList()
            self.verificar(')')
            self.exigir_terminador()
    
    def outList(self):
        self._entrar('outList')
        self.out()
        self.restoOutList()

    def out(self):
        self._entrar('out')
        self.fatorZin()

    def restoOutList(self):
        if self.comparar_token(','):
            self.verificar(',')
            self.out()
            self.restoOutList()

    # Comando while
    def whileStmt(self):
        self._entrar('whileStmt')
        self.verificar('enquanto_tiver_trem')
        self.verificar('(')
        self.expr()
        self.verificar(')')
        self.stmt()

    # Comando if
    def ifStmt(self):
        self._entrar('ifStmt')
        self.verificar('uai_se')
        self.verificar('(')
        self.expr()
        self.verificar(')')
        self.stmt()
        self.elsePart()

    def elsePart(self):
        self._entrar('elsePart')
        if self.comparar_token('uai_senao'):
            self.verificar('uai_senao')
            self.stmt()

    # Comando case
    def caseStmt(self):
        self._entrar('caseStmt')
        self.verificar('dependenu')
        self.verificar('(')
        self.verificar('IDENT')
        self.verificar(')')
        self.verificar('simbora')
        self.dosCasos()
        self.verificar('cabo')

    def dosCasos(self):
        self._entrar('dosCasos')
        self.doCaso()
        self.restoDosCasos()

    def doCaso(self): 
        self._entrar('doCaso')
        self.verificar('du_casu')
        self.fatorZin()
        self.verificar(':')
        self.stmt()
    
    def restoDosCasos(self): 
        if self.comparar_token('du_casu'):
            self.doCaso()
            self.restoDosCasos()
        elif self.comparar_token('default'):
            self.verificar('default')
            self.verificar(':')
            self.stmt()
        elif self.comparar_token('cabo'):
            return

    # Expressões:
    def expr(self):
        self._entrar('expr')
        self.atrib()

    def atrib(self):
        self._entrar('atrib')
        if self.comparar_token('fica_assim_entao'):
            self.verificar('fica_assim_entao')
            self.atrib()
            return
        self.Or()
        self.restoAtrib()

    def restoAtrib(self):
        if self.comparar_token('fica_assim_entao'):
            self.verificar('fica_assim_entao')
            self.atrib()

    def Or(self):
        self._entrar('Or')
        self.xor()
        self.restoOr()

    def restoOr(self):
        if self.comparar_token('quarque_um'):
            self.verificar('quarque_um')
            self.xor()
            self.restoOr()

    def xor(self):
        self._entrar('xor')
        self.And()
        self.restoXor()

    def restoXor(self):
        if self.comparar_token('um_o_oto'):
            self.verificar('um_o_oto')
            self.And()
            self.restoXor()

    def And(self):
        self._entrar('And')
        self.Not()
        self.restoAnd()

    def restoAnd(self):
        if self.comparar_token('tamem'):
            self.verificar('tamem')
            self.Not()
            self.restoAnd()

    def Not(self):
        self._entrar('Not')
        if self.comparar_token('vam_marca'):
            self.verificar('vam_marca')
            self.Not()
        else:
            self.rel()

    def rel(self):
        self._entrar('rel')
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
        self._entrar('add')
        self.mult()
        self.restoAdd()

    def restoAdd(self):
        if self.comparar_token("+") or self.comparar_token('-'):
            self.verificar(self.token_atual().tipo)
            self.mult()
            self.restoAdd()

    def mult(self):
        self._entrar('mult')
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
        self._entrar('uno')
        if(self.comparar_token("+") or
           self.comparar_token('-')):
            self.verificar(self.token_atual().tipo)
            self.uno()
        else:
            self.fatorZao()

    def fatorZao(self):
        self._entrar('fatorZao')
        if self.comparar_token('('):
            self.verificar('(')
            self.atrib()
            self.verificar(')')
        else:
            self.fatorZin()

    def fatorZin(self):
        self._entrar('fatorZin')
        if self.comparar_token(TokenType.STRING_LITERAL):
            self.verificar(TokenType.STRING_LITERAL)

        elif self.comparar_token(TokenType.IDENTIFIER):
            self.verificar(TokenType.IDENTIFIER)
        
        elif self.comparar_token(TokenType.NUMBER_REAL):
            self.verificar(TokenType.NUMBER_REAL)
        
        elif self.comparar_token(TokenType.NUMBER_DECIMAL):
            self.verificar(TokenType.NUMBER_DECIMAL)
        
        elif self.comparar_token(TokenType.TRUE):
            self.verificar(TokenType.TRUE)

        elif self.comparar_token(TokenType.FALSE):
            self.verificar(TokenType.FALSE)
        
        elif self.comparar_token(TokenType.CHAR_LITERAL):
            self.verificar(TokenType.CHAR_LITERAL)
        else:
            token = self.token_atual()
            raise MineiresSyntaxError("um valor (literal ou identificador)", token.lexema, token.linha, token.coluna)

# Main para testes rápidos no arquivo:
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