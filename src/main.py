# le arquivo Mineires e imprime tokens no terminal
import sys
from pathlib import Path
from automato import construir_automato
from lexer import Lexer
from token_type import TokenType

def main() -> int:
    if len(sys.argv) > 1:
        caminho_arquivo = sys.argv[1]
    else:
        raiz_projeto = Path(__file__).resolve().parent.parent
        caminho_arquivo = str(raiz_projeto / "exemplos" / "programa_exemplo.mineires.txt")
    if not Path(caminho_arquivo).exists():
        print(f"Arquivo não encontrado: {caminho_arquivo}")
        return 1
    automato = construir_automato()
    lexer = Lexer(automato, mostrar_erros=True)
    lexer.carregar_arquivo(caminho_arquivo)
    tokens_identificados = lexer.analisar()
    
    # bom tratamento mas deixei pra ver TODOS os tokens por enquanto
    #tokens_identificados = [
    #    token
    #    for token in lexer.tokens
    #    if token.tipo not in {TokenType.ERROR, TokenType.EOF}
    #]
    
    print(f"\nArquivo lido: {caminho_arquivo}")
    print(f"Tokens identificados: {len(tokens_identificados)}")
    print("\nTokens (tupla):")
    for token in tokens_identificados:
        print((token.lexema, token.tipo.name, token.linha, token.coluna))
    print("\nResumo:")
    print(f"- Identificados: {len(tokens_identificados)}")
    print(f"- Não identificados: {sum(1 for token in lexer.tokens if token.tipo == TokenType.ERROR)}")
    
    # Salvando em um arquivo .txt separado:
    with open("exemplos/saida.txt", "w") as file:
        file.write(f"Tokens identificados: {len(tokens_identificados)}\n")

        file.write("\nTokens (tupla):\n")
        for token in tokens_identificados:
            file.write(str((token.lexema, token.tipo.name, token.linha, token.coluna)) + "\n")

        file.write("\nResumo:\n")
        file.write(f"- Identificados: {len(tokens_identificados)}\n")
        file.write(
        f"- Não identificados: {sum(1 for token in lexer.tokens if token.tipo == TokenType.ERROR)}\n"
        )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
