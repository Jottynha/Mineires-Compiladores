# executa a análise léxica e sintática do Mineires
import sys
from typing import Optional
from pathlib import Path
from automato import construir_automato
from lexer import Lexer, LexicalError
from token_type import TokenType
from analisador_sintatico import AnalisadorSintatico
from analisador_sintatico import MineiresSyntaxError

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
    # == SETUP DE ARQUIVOS == #
    caminho_arquivo = sys.argv[1] if len(sys.argv) > 1 else _selecionar_arquivo_exemplo()

    if caminho_arquivo is None:
        return 1

    caminho_path = Path(caminho_arquivo)

    if not caminho_path.exists():
        caminho_path = EXEMPLOS_DIR / caminho_arquivo

    if not caminho_path.exists():
        print(f"Arquivo não encontrado: {caminho_arquivo}")
        return 1
    

    # == CONSTRUÇÃO DO AUTÔMATO == #
    automato = construir_automato()
    

    # == ANÁLISE LÉXICA == #
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
    
    
    # == ANÁLISE SINTÁTICA == #
    analisador_sintatico = AnalisadorSintatico(tokens_identificados) # Criando analisador com objetos Token
    erro_sintatico = None
    sucesso_sintatico = False
    try:
        sucesso_sintatico = analisador_sintatico.function()    # Chamando function para iniciar a recursão
    except MineiresSyntaxError as e:
        erro_sintatico = str(e)
        print(f"\n{e}")
    if erro_sintatico is not None:
        return 1
    

    # == SALVANDO RESULTADOS == #
    SAIDA_DIR.mkdir(parents=True, exist_ok=True)
    with open(SAIDA_DIR / "saida.txt", "w") as file:
        file.write("== ANÁLISE LÉXICA ==\n")
        file.write(f"Tokens identificados: {len(tokens_identificados)}\n")
        file.write("\nTokens (tupla):\n")
        for token in tokens_identificados:
            file.write(str((token.lexema, token.tipo.name, token.linha, token.coluna)) + "\n")
        file.write("\nResumo:\n")
        file.write(f"- Identificados: {len(tokens_identificados)}\n")
        file.write(
        f"- Não identificados: {sum(1 for token in lexer.tokens if token.tipo == TokenType.ERROR)}\n"
        )

        file.write("\n\n== ANÁLISE SINTÁTICA ==\n")
        file.write(f"- Sucesso: {sucesso_sintatico}\n")
        if erro_sintatico is not None:
            file.write(f"- Erro: {erro_sintatico}\n")
        file.write("\nPassos do analisador sintático:\n")
        for passo in analisador_sintatico.get_trilha():
            file.write(passo + "\n")
        
    return 0

if __name__ == "__main__":
    raise SystemExit(main())