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
        self.codigo = []  # Lista de tuplas de código intermediário
        self.temp_count = 0  # Contador para gerar nomes de temporários
        self.label_count = 0  # Contador para gerar labels
        self.vars_table = {}  # Tabela de símbolos simples (nome -> tipo)

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
    
    def _emit(self, op: str, arg1: str, arg2: str | None, arg3: str | None):
        #Emite uma tupla de código intermediário
        self.codigo.append((op, arg1, arg2, arg3))
    
    def _temp_var(self) -> str:
        #Gera variavel temporaria
        self.temp_count += 1
        return f"_t{self.temp_count}"
    
    def _new_label(self) -> str:
        # Gera novo label único
        self.label_count += 1
        return f"L{self.label_count}"
    
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
            tipo, valor = self.atrib()
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
            return token.lexema
        else:
            token = self.token_atual()
            raise MineiresSyntaxError("um tipo de dado (trem_...)", token.lexema, token.linha, token.coluna)

    def declaration(self):
        self._entrar('declaration')
        tipo_var = self.type()
        identificadores = self.identList()
        for ident in identificadores:
            self.vars_table[ident] = tipo_var
        self.exigir_terminador()

    def identList(self):
        self._entrar('identList')
        identificadores = [self.token_atual().lexema]
        self.verificar('IDENT')
        identificadores.extend(self.restoIdentList())
        return identificadores

    def restoIdentList(self):
        identificadores = []
        if self.comparar_token(','):
            self.verificar(',')
            identificadores.append(self.token_atual().lexema)
            self.verificar('IDENT')
            identificadores.extend(self.restoIdentList())
        return identificadores

    # Comando for:
    def forStmt(self):
        self._entrar('forStmt')
        self.verificar('roda_esse_trem')
        self.verificar('(')
        # Inicialização - consome a expressão e emite código
        self._inicio_expr_for = False
        tipo_init, valor_init = self.optExpr()
        self.verificar(';')
        # Gera labels para o for
        L_test = self._new_label()
        L_body = self._new_label()
        L_incr = self._new_label()
        L_exit = self._new_label()
        # Label de teste da condição
        self._emit('label', L_test, None, None)
        # Condição - consome e emite código
        tipo_cond, valor_cond = self.optExpr()
        self.verificar(';')
        # Se condição falsa, sai do loop
        if valor_cond:
            self._emit('if', valor_cond, L_body, L_exit)
        else:
            # Se não há condição, sempre executa o corpo
            self._emit('jump', L_body, None, None)
        # Lê o incremento (sem emitir ainda)
        self.posicao_incr_start = self.posicao
        self._skip_expr()
        self.posicao_incr_end = self.posicao
        self.verificar(')')
        # Label do corpo
        self._emit('label', L_body, None, None)
        # Corpo do for
        self.stmt()
        # Label do incremento
        self._emit('label', L_incr, None, None)
        # Executa incremento: re-processa os tokens do incremento
        if self.posicao_incr_end > self.posicao_incr_start:
            posicao_temp = self.posicao
            self.posicao = self.posicao_incr_start
            self.optExpr()
            self.posicao = posicao_temp
        # Volta para testar condição
        self._emit('jump', L_test, None, None)
        # Label de saída
        self._emit('label', L_exit, None, None)
    
    def _skip_expr(self):
        # Pula uma expressão sem processá-la
        if self._inicio_expr():
            # Pula identificador/valor inicial
            self.posicao += 1
            # Pula operadores e operandos
            while self.posicao < len(self.tokens) and not self.comparar_token(';') and not self.comparar_token(')'):
                self.posicao += 1
        
    def optExpr(self):
        self._entrar('optExpr')
        if self._inicio_expr():
            tipo, valor = self.atrib()
            return tipo, valor
        return None, None

    # Comandos de IO
    def ioStmt(self):
        self._entrar('ioStmt')
        if self.comparar_token('xove'):
            self.verificar('xove')
            self.verificar('(')
            tipo_var = self.type()
            self.verificar(',')
            var_name = self.token_atual().lexema
            self.verificar('IDENT')
            self.verificar(')')
            self._emit('call', 'read', var_name, None)
            self.vars_table[var_name] = tipo_var
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
        tipo, valor = self.fatorZin()
        self._emit('call', 'print', valor if tipo == 'var' else None, valor if tipo != 'var' else None)

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
        tipo, valor = self.expr()
        self.verificar(')')
        # Geração de labels para o while
        L_loop = self._new_label()
        L_body = self._new_label()
        L_exit = self._new_label()
        # Emite label de volta (início do loop)
        self._emit('label', L_loop, None, None)
        # Emite condição: se verdadeira vai para corpo, senão sai
        self._emit('if', valor, L_body, L_exit)
        # Label do corpo
        self._emit('label', L_body, None, None)
        # Bloco do while
        self.stmt()
        # Salta de volta para o teste da condição
        self._emit('jump', L_loop, None, None)
        # Label de saída
        self._emit('label', L_exit, None, None)

    # Comando if
    def ifStmt(self):
        self._entrar('ifStmt')
        self.verificar('uai_se')
        self.verificar('(')
        tipo, valor = self.expr()
        self.verificar(')')
        # Geração de labels para o if/else
        L_true = self._new_label()
        L_false = self._new_label()
        L_after = self._new_label()
        # Emite instrução condicional: se cond for verdadeira vai para L_true senão L_false
        self._emit('if', valor, L_true, L_false)
        # Bloco then
        self._emit('label', L_true, None, None)
        self.stmt()
        # após then, pula para o fim
        self._emit('jump', L_after, None, None)
        # Bloco else (se houver)
        self._emit('label', L_false, None, None)
        self.elsePart()
        # Label final
        self._emit('label', L_after, None, None)

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
        switch_var = self.token_atual().lexema
        self.verificar('IDENT')
        self.verificar(')')
        self.verificar('simbora')
        end_label = self._new_label()
        self.dosCasos(switch_var, end_label)
        self.verificar('cabo')
        self._emit('label', end_label, None, None)

    def dosCasos(self, switch_var, end_label):
        self._entrar('dosCasos')
        self.restoDosCasos(switch_var, end_label)

    def doCaso(self, switch_var, end_label): 
        self._entrar('doCaso')
        self.verificar('du_casu')
        tipo, valor = self.miniFator()
        self.verificar(':')
        caso_label = self._new_label()
        proximo_label = self._new_label()
        temp = self._temp_var()
        self._emit('eq', temp, switch_var, valor)
        self._emit('if', temp, caso_label, proximo_label)
        self._emit('label', caso_label, None, None)
        self.stmt()
        self._emit('jump', end_label, None, None)
        self._emit('label', proximo_label, None, None)
    
    def restoDosCasos(self, switch_var, end_label): 
        if self.comparar_token('du_casu'):
            self.doCaso(switch_var, end_label)
            self.restoDosCasos(switch_var, end_label)
        elif self.comparar_token('uai_so'):
            self.verificar('uai_so')
            self.verificar(':')
            self.stmt()
            self._emit('jump', end_label, None, None)
        elif self.comparar_token('cabo'):
            return

    def miniFator(self):
        self._entrar('miniFator')
        if self.comparar_token(TokenType.STRING_LITERAL):
            val = self.token_atual().lexema
            self.verificar(TokenType.STRING_LITERAL)
            return ('str', val)

        elif self.comparar_token(TokenType.CHAR_LITERAL):
            val = self.token_atual().lexema
            self.verificar(TokenType.CHAR_LITERAL)
            return ('char', val)

        elif self.comparar_token(TokenType.NUMBER_REAL):
            val = self.token_atual().lexema
            self.verificar(TokenType.NUMBER_REAL)
            return ('num', val)

        elif self.comparar_token(TokenType.NUMBER_DECIMAL):
            val = self.token_atual().lexema
            self.verificar(TokenType.NUMBER_DECIMAL)
            return ('num', val)

        elif self.comparar_token(TokenType.TRUE):
            self.verificar(TokenType.TRUE)
            return ('bool', '1')

        elif self.comparar_token(TokenType.FALSE):
            self.verificar(TokenType.FALSE)
            return ('bool', '0')

        else:
            token = self.token_atual()
            raise MineiresSyntaxError("um valor literal para case", token.lexema, token.linha, token.coluna)

    # Expressões:
    def expr(self):
        self._entrar('expr')
        return self.atrib()
    def atrib(self):
        # Trata atribuição e expressões. Retorna (tipo, valor) para código intermediário."""
        self._entrar('atrib')
        tipo, valor = self.Or()
        return self.restoAtrib(tipo, valor)

    def restoAtrib(self, tipo, valor):
        if self.comparar_token('fica_assim_entao'):
            if tipo != 'var':
                token = self.token_atual()
                raise MineiresSyntaxError("uma variável à esquerda de 'fica_assim_entao'", valor, token.linha, token.coluna)
            self.verificar('fica_assim_entao')
            rhs_tipo, rhs_valor = self.atrib()
            self._emit('att', valor, rhs_valor, None)
            if valor not in self.vars_table:
                if rhs_tipo == 'var':
                    self.vars_table[valor] = self.vars_table.get(rhs_valor, 'desconhecido')
                else:
                    self.vars_table[valor] = rhs_tipo
            return ('var', valor)
        return (tipo, valor)

    def Or(self):
        self._entrar('Or')
        tipo, valor = self.xor()
        return self.restoOr(tipo, valor)

    def restoOr(self, tipo, valor):
        if self.comparar_token('quarque_um'):
            self.verificar('quarque_um')
            tipo2, valor2 = self.xor()
            temp = self._temp_var()
            self._emit('or', temp, valor, valor2)
            return self.restoOr('bool', temp)
        return (tipo, valor)

    def xor(self):
        self._entrar('xor')
        tipo, valor = self.And()
        return self.restoXor(tipo, valor)

    def restoXor(self, tipo, valor):
        if self.comparar_token('um_o_oto'):
            self.verificar('um_o_oto')
            tipo2, valor2 = self.And()
            temp = self._temp_var()
            self._emit('xor', temp, valor, valor2)
            return self.restoXor('bool', temp)
        return (tipo, valor)

    def And(self):
        self._entrar('And')
        tipo, valor = self.Not()
        return self.restoAnd(tipo, valor)

    def restoAnd(self, tipo, valor):
        if self.comparar_token('tamem'):
            self.verificar('tamem')
            tipo2, valor2 = self.Not()
            temp = self._temp_var()
            self._emit('and', temp, valor, valor2)
            return self.restoAnd('bool', temp)
        return (tipo, valor)

    def Not(self):
        self._entrar('Not')
        if self.comparar_token('vam_marca'):
            self.verificar('vam_marca')
            tipo, valor = self.Not()
            temp = self._temp_var()
            self._emit('not', temp, valor, None)
            return ('bool', temp)
        else:
            return self.rel()

    def rel(self):
        self._entrar('rel')
        tipo, valor = self.add()
        return self.restoRel(tipo, valor)

    def restoRel(self, tipo, valor):
        relacionais = {'mema_coisa', 'neh_nada', '<', '<=', '>', '>='}
        for rel in relacionais:
            if self.comparar_token(rel):
                self.verificar(rel)
                tipo2, valor2 = self.add()
                temp = self._temp_var()
                op_map = {
                    'mema_coisa': 'eq', 'neh_nada': 'dif',
                    '<': 'les', '<=': 'leq', '>': 'grt', '>=': 'geq'
                }
                self._emit(op_map.get(rel, rel), temp, valor, valor2)
                return ('bool', temp)
        return (tipo, valor)

    def add(self):
        self._entrar('add')
        tipo, valor = self.mult()
        return self.restoAdd(tipo, valor)

    def restoAdd(self, tipo, valor):
        if self.comparar_token("+") or self.comparar_token('-'):
            op = self.token_atual().lexema
            self.verificar(self.token_atual().tipo)
            tipo2, valor2 = self.mult()
            temp = self._temp_var()
            op_code = 'add' if op == '+' else 'sub'
            self._emit(op_code, temp, valor, valor2)
            return self.restoAdd('num', temp)
        return (tipo, valor)

    def mult(self):
        self._entrar('mult')
        tipo, valor = self.uno()
        return self.restoMult(tipo, valor)

    def restoMult(self, tipo, valor):
        if (self.comparar_token('veiz') or
            self.comparar_token('sob') or
            self.comparar_token('/') or
            self.comparar_token('%')):
            op = self.token_atual().lexema
            self.verificar(self.token_atual().tipo)
            tipo2, valor2 = self.uno()
            temp = self._temp_var()
            op_map = {'veiz': 'mult', 'sob': 'divI', '/': 'div', '%': 'mod'}
            self._emit(op_map.get(op, op), temp, valor, valor2)
            return self.restoMult('num', temp)
        return (tipo, valor)

    def uno(self):
        self._entrar('uno')
        if(self.comparar_token("+") or
           self.comparar_token('-')):
            op = self.token_atual().lexema
            self.verificar(self.token_atual().tipo)
            tipo, valor = self.uno()
            # Unário + ou - não precisa emitir código especial (- pode ser negação)
            if op == '-':
                temp = self._temp_var()
                self._emit('sub', temp, '0', valor)
                return ('num', temp)
            return (tipo, valor)
        else:
            return self.fatorZao()

    def fatorZao(self):
        self._entrar('fatorZao')
        if self.comparar_token('('):
            self.verificar('(')
            tipo, valor = self.atrib()
            self.verificar(')')
            return (tipo, valor)
        else:
            return self.fatorZin()

    def fatorZin(self):
        self._entrar('fatorZin')
        if self.comparar_token(TokenType.STRING_LITERAL):
            val = self.token_atual().lexema
            self.verificar(TokenType.STRING_LITERAL)
            return ('str', val)

        elif self.comparar_token(TokenType.IDENTIFIER):
            val = self.token_atual().lexema
            self.verificar(TokenType.IDENTIFIER)
            return ('var', val)
        
        elif self.comparar_token(TokenType.NUMBER_REAL):
            val = self.token_atual().lexema
            self.verificar(TokenType.NUMBER_REAL)
            return ('num', val)
        
        elif self.comparar_token(TokenType.NUMBER_DECIMAL):
            val = self.token_atual().lexema
            self.verificar(TokenType.NUMBER_DECIMAL)
            return ('num', val)
        
        elif self.comparar_token(TokenType.TRUE):
            self.verificar(TokenType.TRUE)
            return ('bool', '1')

        elif self.comparar_token(TokenType.FALSE):
            self.verificar(TokenType.FALSE)
            return ('bool', '0')
        
        elif self.comparar_token(TokenType.CHAR_LITERAL):
            val = self.token_atual().lexema
            self.verificar(TokenType.CHAR_LITERAL)
            return ('char', val)
        else:
            token = self.token_atual()
            raise MineiresSyntaxError("um valor (literal ou identificador)", token.lexema, token.linha, token.coluna)
