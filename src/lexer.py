# analisador léxico para mineires.
from typing import List, Optional, Generator
from automato import Automato
from token_type import TokenType, RESERVED_WORDS
from mineires_token import Token


class LexicalError(Exception):
    def __init__(self, lexema: str, linha: int, coluna: int, mensagem_especifica: Optional[str] = None):
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna
        if mensagem_especifica:
            mensagem = f"Erro léxico na linha {linha}, coluna {coluna}: {mensagem_especifica}"
        else:
            mensagem = f"Erro léxico: string '{lexema}' não reconhecida na linha {linha}, coluna {coluna}"
        super().__init__(mensagem)

class Lexer:
    def __init__(self, automato: Automato, mostrar_erros: bool = True):
        # inicializa o Lexer com um autômato.
        # args: automato: Autômato configurado para reconhecer tokens
        #       mostrar_erros: Se True, imprime erros léxicos no terminal
        self.automato = automato
        self.mostrar_erros = mostrar_erros
        self.codigo: str = ""
        self.posicao: int = 0
        self.linha: int = 1
        self.coluna: int = 1
        self.tokens: List[Token] = []
        self._delimitadores_numero = set(' \t\r\n,;(){}[]<>!=+-*/%"\'')

    def carregar_arquivo(self, caminho: str) -> None:
        with open(caminho, 'r', encoding='utf-8') as f:
            self.codigo = f.read()
        self.posicao = 0
        self.linha = 1
        self.coluna = 1
        self.tokens = []

    def carregar_string(self, codigo: str) -> None:
        self.codigo = codigo
        self.posicao = 0
        self.linha = 1
        self.coluna = 1
        self.tokens = []

    def _char_atual(self) -> Optional[str]:
        # retorna o caractere atual ou None se fim do arquivo.
        if self.posicao < len(self.codigo):
            return self.codigo[self.posicao]
        return None
    def _avancar(self) -> Optional[str]:
        if self.posicao >= len(self.codigo):
            return None
        char = self.codigo[self.posicao]
        self.posicao += 1
        if char == '\n':
            self.linha += 1
            self.coluna = 1
        else:
            self.coluna += 1
        return char
    def _peek(self, offset: int = 1) -> Optional[str]:
        # olha caracteres à frente sem consumir
        # args: offset: Quantos caracteres à frente (1 = próximo)
        # retorna: o caractere na posição ou None se fim do arquivo
        pos = self.posicao + offset
        if pos < len(self.codigo):
            return self.codigo[pos]
        return None
    def _pular_espacos(self) -> None:
        while self._char_atual() is not None and self._char_atual() in ' \t\r\n':
            self._avancar()

    def _eh_char_identificador(self, char: Optional[str]) -> bool:
        return char is not None and (char.isalnum() or char == '_')
    def _eh_lexema_identificador(self, lexema: str) -> bool:
        if not lexema:
            return False
        if not (lexema[0].isalpha() or lexema[0] == '_'):
            return False
        return all(ch.isalnum() or ch == '_' for ch in lexema)

    def _reconhecer_string(self) -> Optional[Token]:
        # reconhece string entre aspas duplas com suporte a escapes
        if self._char_atual() != '"':
            return None
        linha_inicio = self.linha
        coluna_inicio = self.coluna
        self._avancar()  # consome a aspas inicial
        lexema = '"'
        while self._char_atual() is not None:
            char = self._char_atual()
            if char == '\\':
                # Escape sequence
                lexema += self._avancar() or ""
                proximo = self._char_atual()
                if proximo in 'ntr"\\':
                    lexema += self._avancar() or ""
                else:
                    raise LexicalError(lexema, linha_inicio, coluna_inicio, f"sequência de escape inválida '\\{proximo}' em string")
            elif char == '"':
                # Fim da string
                lexema += self._avancar() or ""
                return Token(lexema, TokenType.STRING_LITERAL, linha_inicio, coluna_inicio)
            elif char == '\n':
                # Quebra de linha dentro de string é erro
                raise LexicalError(lexema, linha_inicio, coluna_inicio, "quebra de linha dentro de string literal")
            else:
                lexema += self._avancar() or ""
        # String não fechada
        raise LexicalError(lexema, linha_inicio, coluna_inicio, "string literal não fechada (esperado '\"')")
    def _reconhecer_char(self) -> Optional[Token]:
        # reconhece char único entre aspas simples
        if self._char_atual() != "'":
            return None
        linha_inicio = self.linha
        coluna_inicio = self.coluna
        # Peek ahead para ver se é um char válido
        if self._peek(1) is None:
            return None
        proximo_char = self._peek(1)
        # Se for .' ou '. sozinhos, deixa o AFD tratar
        if proximo_char == '.' or (proximo_char == "'" and self._peek(2) != '.'):
            return None
        
        self._avancar()  # consome a aspas inicial
        lexema = "'"
        # Primeiro caractere (pode ser escape)
        char = self._char_atual()
        if char is None:
            raise LexicalError(lexema, linha_inicio, coluna_inicio, "char literal incompleto (esperado caractere ou escape)")
        if char == '\\':
            # Escape sequence
            lexema += self._avancar() or ""
            proximo = self._char_atual()
            if proximo not in 'ntr"\\':
                raise LexicalError(lexema, linha_inicio, coluna_inicio, f"sequência de escape inválida '\\{proximo}' em char")
            lexema += self._avancar() or ""
        elif char == "'":
            # Char vazio
            raise LexicalError(lexema, linha_inicio, coluna_inicio, "char literal vazio (esperado um caractere entre aspas simples)")
        elif char == '\n':
            # Quebra de linha dentro de char é erro
            raise LexicalError(lexema, linha_inicio, coluna_inicio, "quebra de linha dentro de char literal")
        else:
            lexema += self._avancar() or ""
        # Deve ter aspas simples de fechamento
        if self._char_atual() != "'":
            raise LexicalError(lexema, linha_inicio, coluna_inicio, "char literal não fechado (esperado ')")
        lexema += self._avancar() or ""
        return Token(lexema, TokenType.CHAR_LITERAL, linha_inicio, coluna_inicio)
    def _consumir_lexema_invalido(self) -> str:
        # consome um trecho inválido contínuo até espaço em branco ou fim
        lexema_invalido = ""
        while self._char_atual() is not None and self._char_atual() not in ' \t\r\n':
            lexema_invalido += self._avancar() or ""
        return lexema_invalido
    def _consumir_numero_malformado(self) -> str:
        lexema = ""
        while self._char_atual() is not None and self._char_atual() not in self._delimitadores_numero:
            lexema += self._avancar() or ""
        return lexema
    def _validar_numero_malformado(self, token: Token) -> None:
        if token.tipo not in {
            TokenType.NUMBER_DECIMAL,
            TokenType.NUMBER_REAL,
            TokenType.NUMBER_OCTAL,
            TokenType.NUMBER_HEX,
        }:
            return
        proximo = self._char_atual()
        if proximo is None:
            return
        if token.tipo == TokenType.NUMBER_OCTAL and proximo.isdigit():
            resto = self._consumir_numero_malformado()
            raise LexicalError(f"{token.lexema}{resto}", token.linha, token.coluna, "número octal inválido (contém dígito fora do intervalo 0-7)")
        if proximo.isalpha() or proximo == '_' or proximo == '.':
            resto = self._consumir_numero_malformado()
            raise LexicalError(f"{token.lexema}{resto}", token.linha, token.coluna, "número malformado (contém caracteres inválidos após número)")
    def _consumir_comentario_multilinha(self, linha_inicio: int, coluna_inicio: int) -> Token:
        while self._char_atual() is not None:
            self._pular_espacos()
            if self._char_atual() is None:
                break
            token = self._reconhecer_com_automato()
            if token is None:
                self._avancar()
                continue
            if token.tipo == TokenType.COMMENT_END:
                return token
        raise LexicalError("causo", linha_inicio, coluna_inicio, "comentário multilinha não fechado (esperado '*/u')")
    def _reconhecer_com_automato(self) -> Optional[Token]:
        if self.automato.estado_inicial is None:
            return None
        estado_atual = self.automato.estado_inicial
        lexema = ""
        linha_inicio = self.linha
        coluna_inicio = self.coluna
        posicao_inicio = self.posicao
        linha_posicao_inicio = self.linha
        coluna_posicao_inicio = self.coluna
        ultimo_estado_final = None
        ultimo_lexema = ""
        ultima_posicao = self.posicao
        ultima_linha = self.linha
        ultima_coluna = self.coluna
        while self._char_atual() is not None:
            char = self._char_atual()
            proximo = self.automato.proximo_estado(estado_atual, char)
            if proximo is None:
                # Sem transição, para aqui
                break
            lexema += char
            self._avancar()
            estado_atual = proximo
            # Se chegou em estado final, guarda como candidato
            if self.automato.eh_estado_final(estado_atual):
                ultimo_estado_final = estado_atual
                ultimo_lexema = lexema
                ultima_posicao = self.posicao
                ultima_linha = self.linha
                ultima_coluna = self.coluna
        # Se encontrou estado final, retorna o token
        if ultimo_estado_final is not None:
            # Restaura posição para depois do último token válido
            self.posicao = ultima_posicao
            self.linha = ultima_linha
            self.coluna = ultima_coluna
            token_type = self.automato.get_token_type(ultimo_estado_final)
            # Verifica se é palavra reservada (para identificadores)
            if token_type == TokenType.IDENTIFIER:
                if ultimo_lexema in RESERVED_WORDS:
                    token_type = RESERVED_WORDS[ultimo_lexema]
            if (
                token_type in RESERVED_WORDS.values()
                and ultimo_lexema in RESERVED_WORDS
                and self._eh_lexema_identificador(ultimo_lexema)
                and self._eh_char_identificador(self._char_atual())
            ):
                while self._eh_char_identificador(self._char_atual()):
                    ultimo_lexema += self._avancar() or ""
                token_type = TokenType.IDENTIFIER
            return Token(ultimo_lexema, token_type, linha_inicio, coluna_inicio)

        # Não encontrou estado final: restaura e tenta reconhecer identificador genérico
        self.posicao = posicao_inicio
        self.linha = linha_posicao_inicio
        self.coluna = coluna_posicao_inicio
        char_atual = self._char_atual()
        if char_atual is not None and (char_atual.isalpha() or char_atual == '_'):
            lexema_identificador = self._avancar() or ""
            while self._eh_char_identificador(self._char_atual()):
                lexema_identificador += self._avancar() or ""
            token_type = RESERVED_WORDS.get(lexema_identificador, TokenType.IDENTIFIER)
            return Token(lexema_identificador, token_type, linha_inicio, coluna_inicio)

        return None
    
    def analisar(self) -> List[Token]:
        self.tokens = []
        while self._char_atual() is not None:
            # Pula espaços em branco
            self._pular_espacos()
            if self._char_atual() is None:
                break
            # Tenta reconhecer string
            token_string = self._reconhecer_string()
            if token_string is not None:
                self.tokens.append(token_string)
                continue
            # Tenta reconhecer char
            token_char = self._reconhecer_char()
            if token_char is not None:
                self.tokens.append(token_char)
                continue
            linha_inicio = self.linha
            coluna_inicio = self.coluna
            # Tenta reconhecer com o autômato
            token = self._reconhecer_com_automato()
            if token is not None:
                if token.tipo == TokenType.COMMENT_START:
                    self._consumir_comentario_multilinha(token.linha, token.coluna)
                    continue
                if token.tipo == TokenType.COMMENT_LINE:
                    while self._char_atual() is not None and self._char_atual() != '\n':
                        self._avancar()
                    continue
                self._validar_numero_malformado(token)
                # Ignora tokens de whitespace se necessário
                if token.tipo != TokenType.WHITESPACE:
                    self.tokens.append(token)
            else:
                char_atual = self._char_atual()
                if char_atual is not None and (char_atual.isdigit() or (char_atual == '.' and (self._peek() or '').isdigit())):
                    numero_invalido = self._consumir_numero_malformado()
                    if not numero_invalido and self._char_atual() is not None:
                        numero_invalido = self._avancar() or ""
                    erro = Token(numero_invalido, TokenType.ERROR, linha_inicio, coluna_inicio)
                    self.tokens.append(erro)
                    raise LexicalError(erro.lexema, erro.linha, erro.coluna, "número malformado (sintaxe inválida)")
                # Lexema não reconhecido - erro léxico
                lexema_invalido = self._consumir_lexema_invalido()
                if not lexema_invalido and self._char_atual() is not None:
                    lexema_invalido = self._avancar() or ""
                erro = Token(lexema_invalido, TokenType.ERROR, linha_inicio, coluna_inicio)
                self.tokens.append(erro)
                raise LexicalError(erro.lexema, erro.linha, erro.coluna, "token não reconhecido")
        # Adiciona token de fim de arquivo
        token_eof = Token("EOF", TokenType.EOF, self.linha, self.coluna)
        self.tokens.append(token_eof)
        return self.tokens
    def tokens_generator(self) -> Generator[Token, None, None]:
        while self._char_atual() is not None:
            self._pular_espacos()
            if self._char_atual() is None:
                break
            # Tenta reconhecer string
            token_string = self._reconhecer_string()
            if token_string is not None:
                yield token_string
                continue
            # Tenta reconhecer char
            token_char = self._reconhecer_char()
            if token_char is not None:
                yield token_char
                continue
            linha_inicio = self.linha
            coluna_inicio = self.coluna
            token = self._reconhecer_com_automato()
            if token is not None:
                if token.tipo == TokenType.COMMENT_START:
                    yield token
                    token_fim = self._consumir_comentario_multilinha(token.linha, token.coluna)
                    yield token_fim
                    continue
                self._validar_numero_malformado(token)
                if token.tipo != TokenType.WHITESPACE:
                    yield token
            else:
                char_atual = self._char_atual()
                if char_atual is not None and (char_atual.isdigit() or (char_atual == '.' and (self._peek() or '').isdigit())):
                    numero_invalido = self._consumir_numero_malformado()
                    if not numero_invalido and self._char_atual() is not None:
                        numero_invalido = self._avancar() or ""
                    erro = Token(numero_invalido, TokenType.ERROR, linha_inicio, coluna_inicio)
                    yield erro
                    raise LexicalError(erro.lexema, erro.linha, erro.coluna, "número malformado (sintaxe inválida)")
                lexema_invalido = self._consumir_lexema_invalido()
                if not lexema_invalido and self._char_atual() is not None:
                    lexema_invalido = self._avancar() or ""
                erro = Token(lexema_invalido, TokenType.ERROR, linha_inicio, coluna_inicio)
                yield erro
                raise LexicalError(erro.lexema, erro.linha, erro.coluna, "token não reconhecido")
        yield Token("EOF", TokenType.EOF, self.linha, self.coluna)    
    def imprimir_tokens(self) -> None:
        print("\n" + "=" * 70)
        print(f"{'LEXEMA':<30} {'TIPO':<25} {'LINHA':<7} {'COLUNA':<7}")
        print("=" * 70)
        for token in self.tokens:
            lexema_display = repr(token.lexema) if len(token.lexema) <= 28 else repr(token.lexema[:25] + "...")
            print(f"{lexema_display:<30} {token.tipo.name:<25} {token.linha:<7} {token.coluna:<7}")
        print("=" * 70)
        print(f"Total de tokens: {len(self.tokens)}")
