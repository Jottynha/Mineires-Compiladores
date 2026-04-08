from token_type import RESERVED_WORDS
from token_type import TokenType

class AnalisadorSintatico:
    def __init__(self, lista_tokens):
        self.tokens = lista_tokens
        self.posicao = 0

    def token_atual(self):
        return self.tokens[self.posicao]
    
    def comparar_token(self, tipo):
        if (self.token_atual() == RESERVED_WORDS[tipo].value):
            return True
        else:
            return False
        
    def comparar_token_literal(self, tipo):
        if (self.token_atual() == tipo):
            return True
        else:
            return False

    def verificar(self, tipo):
        if self.comparar_token(tipo) or self.comparar_token_literal(tipo):
            self.posicao += 1
        else:
            print(f"{self.token_atual()} =\= {RESERVED_WORDS[tipo]}")
        
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
        if (self.stmt()):
            self.stmtList()

    def stmt(self):
        if self.comparar_token('roda_esse_trem'):
            self.forStmt()
        
        elif self.comparar_token('xove') or self.comparar_token('oia_proce_ve'):
            self.ioStmt()
        
        elif self.comparar_token('enquanto_tiver_trem'): 
            self.whileStmt()
        
        elif self.atrib():
            self.verificar('uai')
        
        elif self.verificar('uai_se'):
            self.ifStmt()
        
        elif self.verificar('dependenu'):
            self.caseStmt()

        elif self.verificar('simbora'):
            self.bloco()

        elif self.verificar('para_o_trem') or self.verificar('toca_o_trem'):
            self.verificar('uai')
        
        elif self.type():
            self.declaration()

        else:
            self.verificar('uai') 

    def type(self):
        if self.token_atual() in {
            RESERVED_WORDS['trem_di_numeru'].value,
            RESERVED_WORDS['trem_cum_virgula'].value,
            RESERVED_WORDS['trem_discrita'].value,
            RESERVED_WORDS['trem_discolhe'].value,
            RESERVED_WORDS['trosso'].value,
        }:
            self.posicao += 1
        else:
            return False



    # Declarações:
    def declaration(self):
        self.type()
        self.identList()

    def identList(self):
        self.verificar('IDENT')
        self.restoIdentList()

    def restoIdentList(self):
        if self.verificar(','):
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
            self.verificar(';')

        elif self.comparar_token('oia_proce_ve'):
            self.verificar('oia_proce_ve')
            self.verificar('(')
            self.outList()
            self.verificar(')')
            self.verificar(';')
    
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
        self.verificar('du_caso')
        self.fatorZin()
        self.verificar(':')
        self.stmt()
    
    def restoDosCasos(self): 
        if self.comparar_token('du_caso'):
            self.doCaso()
            self.restoDosCasos()
        else:
            self.verificar('default')
            self.verificar(':')
            self.stmt()

    

    # Expressões:
    def expr(self):
        self.atrib()

    def atrib(self):
        self.Or()
        self.restoAtrib()

    def restoAtrib(self):
        if self.comparar_token('fica_assim_entao'):
            self.atrib()

    def Or(self):
        self.xor()
        self.restoOr()

    def restoOr(self):
        if self.comparar_token('quarque_um'):
            self.xor()
            self.restoOr()

    def xor(self):
        self.And()
        self.restoXor()

    def restoXor(self):
        if self.comparar_token('um_o_oto'):
            self.And()
            self.restoXor()

    def And(self):
        self.Not()
        self.restoAnd()

    def restoAnd(self):
        if self.comparar_token('tamem'):
            self.Not()
            self.restoAnd()

    def Not(self):
        if self.verificar('vam_marca'):
            self.Not()
        else:
            self.rel()

    def rel(self):
        self.add()
        self.restoRel()

    def restoRel(self):
        if (self.verificar('mema_coisa') or 
            self.verificar('neh_nada') or
            self.verificar('<') or
            self.verificar('<=') or
            self.verificar('>') or
            self.verificar('>=')):
            self.add()

    def add(self):
        self.mult()
        self.restoAdd()

    def restoAdd(self):
        if (self.verificar("+'") or
            self.verificar('-')):
            self.mult()
            self.restoAdd()

    def mult(self):
        self.uno()
        self.restoMult()

    def restoMult(self):
        if (self.verificar('veiz') or
            self.verificar('sob') or
            self.verificar('/') or
            self.verificar('%')):
            self.uno()
            self.restoMult()

    def uno(self):
        if(self.verificar("+'") or
           self.verificar('-')):
            self.uno()
        else:
            self.fatorZao()

    def fatorZao(self):
        if self.verificar('('):
            self.atrib()
            self.verificar(')')
        else:
            self.fatorZin()

    def fatorZin(self):
        if self.comparar_token_literal(TokenType.STRING_LITERAL.value):
            self.verificar(TokenType.STRING_LITERAL.value)

        elif self.comparar_token_literal(TokenType.IDENTIFIER.value):
            self.verificar(TokenType.IDENTIFIER.value)
        
        elif self.comparar_token_literal(TokenType.NUMBER_REAL.value):
            self.verificar(TokenType.NUMBER_REAL.value)
        
        elif self.comparar_token_literal(TokenType.NUMBER_DECIMAL.value):
            self.verificar(TokenType.NUMBER_DECIMAL.value)
        
        # atenção aqui pq chama trem_discolhe e talvez nn seja isso
        elif self.comparar_token_literal(TokenType.BOOLEAN.value):
            self.verificar(TokenType.BOOLEAN.value)
        
        elif self.comparar_token_literal(TokenType.CHAR_LITERAL.value):
            self.verificar(TokenType.CHAR_LITERAL.value)

if __name__ == "__main__":
    # Testando o uai mundo com os values gerados: 
    lista_enums = [9, 10, 26, 27, 22, 32, 19, 62, 31, 21, 62, 31, 36, 58, 31, 36, 57, 31, 13, 26, 62, 27, 31, 11, 54, 31, 17, 53, 23, 63]
    sint = AnalisadorSintatico(lista_enums)
    sint.function()