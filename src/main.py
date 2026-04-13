# executa a análise léxica e sintática do Mineires
import sys
from typing import Optional
from pathlib import Path
from automato import construir_automato
from lexer import Lexer, LexicalError
from token_type import TokenType
from analisador_sintatico import AnalisadorSintatico

# Define o diretório base do projeto
SCRIPT_DIR = Path(__file__).resolve().parent.parent
EXEMPLOS_DIR = SCRIPT_DIR / "exemplos"
SAIDA_DIR = EXEMPLOS_DIR


def _listar_arquivos_exemplo() -> list[Path]:
    if not EXEMPLOS_DIR.exists():
        return []
    return sorted(
        [
            arquivo
            for arquivo in EXEMPLOS_DIR.iterdir()
            if arquivo.is_file() and arquivo.name != "saida.txt"
        ]
    )


def _selecionar_arquivo_exemplo() -> Optional[str]:
    arquivos = _listar_arquivos_exemplo()
    if not arquivos:
        print(f"Nenhum arquivo de exemplo encontrado em: {EXEMPLOS_DIR}")
        return None
    print("\nArquivos disponíveis em exemplos:")
    for indice, arquivo in enumerate(arquivos, start=1):
        print(f"[{indice}] {arquivo.name}")
    while True:
        escolha = input("Selecione pelo número (ou 'q' para sair): ").strip().lower()
        if escolha == "q":
            return None
        if escolha.isdigit():
            indice = int(escolha)
            if 1 <= indice <= len(arquivos):
                return str(arquivos[indice - 1])
        print("Opção inválida. Tente novamente.")

def main() -> int:
    caminho_arquivo = None
    # Parse argumentos
    for arg in sys.argv[1:]:
        caminho_arquivo = arg
    # Define arquivo padrão se não fornecido
    if caminho_arquivo is None:
        caminho_arquivo = _selecionar_arquivo_exemplo()
        if caminho_arquivo is None:
            return 1
    caminho_path = Path(caminho_arquivo)
    if not caminho_path.exists():
        candidato = EXEMPLOS_DIR / caminho_arquivo
        if candidato.exists():
            caminho_path = candidato
        else:
            print(f"Arquivo não encontrado: {caminho_arquivo}")
            return 1
    automato = construir_automato()
    lexer = Lexer(automato, mostrar_erros=True)
    lexer.carregar_arquivo(str(caminho_path))
    try:
        tokens_identificados = lexer.analisar()
    except LexicalError as erro_lexico:
        print(str(erro_lexico))
        return 1
    print(f"\nArquivo lido: {caminho_path}")
    print(f"Tokens identificados: {len(tokens_identificados)}")
    print("\nTokens (tupla):")
    for token in tokens_identificados:
        print((token.lexema, token.tipo.value, token.linha, token.coluna)) # imprimindo valores do TokenType ao inves do nome associado
    print("\nResumo:")
    print(f"- Identificados: {len(tokens_identificados)}")
    print(f"- Não identificados: {sum(1 for token in lexer.tokens if token.tipo == TokenType.ERROR)}")
    # Salvando em um arquivo .txt separado:
    SAIDA_DIR.mkdir(parents=True, exist_ok=True)
    with open(SAIDA_DIR / "saida.txt", "w") as file:
        file.write(f"Tokens identificados: {len(tokens_identificados)}\n")
        file.write("\nTokens (tupla):\n")
        for token in tokens_identificados:
            file.write(str((token.lexema, token.tipo.name, token.linha, token.coluna)) + "\n")
        file.write("\nResumo:\n")
        file.write(f"- Identificados: {len(tokens_identificados)}\n")
        file.write(
        f"- Não identificados: {sum(1 for token in lexer.tokens if token.tipo == TokenType.ERROR)}\n"
        )
    ## ANÁLISE SINTÁTICA ##
    from analisador_sintatico import MineiresSyntaxError
    analisador_sintatico = AnalisadorSintatico(tokens_identificados) # Criando analisador com objetos Token
    erro_sintatico = None
    sucesso_sintatico = False
    try:
        sucesso_sintatico = analisador_sintatico.function()    # Chamando function para iniciar a recursão
    except MineiresSyntaxError as e:
        erro_sintatico = str(e)
        print(f"\n{e}")
    with open(SAIDA_DIR / "saida.txt", "a") as file:
        file.write("\nAnálise Sintática:\n")
        file.write(f"- Sucesso: {sucesso_sintatico}\n")
        if erro_sintatico is not None:
            file.write(f"- Erro: {erro_sintatico}\n")
        file.write("\nPassos do analisador sintático:\n")
        for passo in analisador_sintatico.get_trilha():
            file.write(passo + "\n")
    if erro_sintatico is not None:
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
