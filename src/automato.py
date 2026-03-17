# afd para analise léxica do Mineires, construído a partir de arquivo txt
from enum import Enum, auto
from pathlib import Path
from typing import Any, Optional


class EstadoTipo(Enum):
    INICIAL = auto()
    INTERMEDIARIO = auto()
    FINAL = auto()
class Automato:
    def __init__(self, nome: str = "Automato"):
        self.nome = nome
        self.estado_inicial: Optional[str] = None # string || None
        self.estados: dict[str, EstadoTipo] = {} 
        self.token_por_estado: dict[str, Any] = {} # tokens a estados relevantes
        self.transicoes_char: dict[str, dict[str, str]] = {} # origem -> (caractere -> destino)
    def adicionar_estado(
        self,
        nome: str,
        tipo: EstadoTipo = EstadoTipo.INTERMEDIARIO,
        token_type: Optional[Any] = None,
    ) -> "Automato":
        self.estados[nome] = tipo
        if token_type is not None:
            self.token_por_estado[nome] = token_type
        if tipo == EstadoTipo.INICIAL:
            self.estado_inicial = nome
        self.transicoes_char.setdefault(nome, {}) #declaração em caso de não existir, para evitar erros depois
        return self
    def adicionar_transicao(
        self,
        origem: str,
        destino: str,
        caractere: Optional[str] = None,
    ) -> "Automato":
        if origem not in self.estados or destino not in self.estados:
            raise ValueError("Origem/destino não existem")
        if caractere is None:
            raise ValueError("Transições só podem ser por caractere")
        self.transicoes_char[origem][caractere] = destino
        return self
    def proximo_estado(self, estado_atual: str, caractere: str) -> Optional[str]:
        return self.transicoes_char.get(estado_atual, {}).get(caractere)
    def eh_estado_final(self, estado: str) -> bool:
        return self.estados.get(estado) == EstadoTipo.FINAL
    def get_token_type(self, estado: str) -> Optional[Any]:
        return self.token_por_estado.get(estado)

def _decodificar_caractere_txt(valor: str) -> str:
    if valor == r"\n":
        return "\n"
    if valor == r"\t":
        return "\t"
    if valor == r"\r":
        return "\r"
    if valor == r"\s":
        return " "
    return valor

def construir_automato_por_txt(caminho_txt: str, token_type_cls) -> Automato:
    """
    Constrói um AFD lendo estados e transições de um arquivo .txt.
    Formato esperado:
    [ESTADOS]
    q0 INICIAL
    q1 FINAL IDENTIFIER
    [TRANSICOES]
    q0 q1 a
    q1 q1 b
    """
    automato = Automato(Path(caminho_txt).stem)
    with open(caminho_txt, "r", encoding="utf-8") as arquivo:
        linhas = arquivo.readlines()
    secao = None
    for numero_linha, linha_bruta in enumerate(linhas, start=1):
        linha = linha_bruta.strip()
        if not linha or linha.startswith("#"):
            continue
        if linha == "[ESTADOS]":
            secao = "ESTADOS"
            continue
        if linha == "[TRANSICOES]":
            secao = "TRANSICOES"
            continue
        if secao == "ESTADOS":
            partes = linha.split()
            if len(partes) < 2:
                raise ValueError(f"Linha {numero_linha}: estado inválido '{linha}'")
            nome_estado = partes[0]
            tipo_estado_nome = partes[1]
            if tipo_estado_nome not in EstadoTipo.__members__:
                raise ValueError(
                    f"Linha {numero_linha}: tipo de estado inválido '{tipo_estado_nome}'"
                )
            tipo_estado = EstadoTipo[tipo_estado_nome]
            token_type = None
            if len(partes) >= 3:
                nome_token = partes[2]
                if not hasattr(token_type_cls, nome_token):
                    raise ValueError(
                        f"Linha {numero_linha}: token inválido '{nome_token}'"
                    )
                token_type = getattr(token_type_cls, nome_token)
            automato.adicionar_estado(nome_estado, tipo_estado, token_type)
            continue
        if secao == "TRANSICOES":
            partes = linha.split(maxsplit=2)
            if len(partes) != 3:
                raise ValueError(f"Linha {numero_linha}: transição inválida '{linha}'")
            origem, destino, caractere_txt = partes
            caractere = _decodificar_caractere_txt(caractere_txt)
            if len(caractere) != 1:
                raise ValueError(
                    f"Linha {numero_linha}: caractere de transição inválido '{caractere_txt}'"
                )
            automato.adicionar_transicao(origem, destino, caractere=caractere)
            continue
        raise ValueError(
            f"Linha {numero_linha}: conteúdo fora de [ESTADOS]/[TRANSICOES]"
        )
    if automato.estado_inicial is None:
        raise ValueError("AFD inválido: nenhum estado inicial definido")
    return automato

def _caminho_automato_padrao() -> str:
    raiz_projeto = Path(__file__).resolve().parent.parent
    return str(raiz_projeto / "grafos" / "automato_simples.txt")

def construir_automato() -> Automato:
    from token_type import TokenType
    return construir_automato_por_txt(_caminho_automato_padrao(), TokenType)
