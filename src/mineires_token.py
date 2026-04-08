# Representa um token identificado pelo lexer.
from dataclasses import dataclass # Para facilitar a criação de classes simples como Token
from token_type import TokenType 

@dataclass
class Token:
    """
    Representa um token identificado pelo analisador léxico.
    Atributos da tupla/classe:
        lexema: O texto exato encontrado no código fonte
        tipo: O tipo do token (TokenType)
        linha: Número da linha onde o token foi encontrado (1-indexed)
        coluna: Número da coluna onde o token começa (1-indexed)
    """
    lexema: str
    tipo: TokenType
    linha: int
    coluna: int
    def __repr__(self) -> str:
        return f"({self.lexema!r}, {self.tipo.name}, {self.linha}, {self.coluna})"
    def to_tuple(self) -> tuple:
        # Retorna o token como uma tupla.
        return (self.lexema, self.tipo, self.linha, self.coluna)
