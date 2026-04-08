# le arquivo Mineires e imprime tokens no terminal
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
    profile = False
    caminho_arquivo = None
    
    # Parse argumentos
    for arg in sys.argv[1:]:
        if arg == "--profile":
            profile = True
        else:
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
    lexer = Lexer(automato, mostrar_erros=True, profile=profile)
    lexer.carregar_arquivo(str(caminho_path))
    try:
        tokens_identificados = lexer.analisar()
    except LexicalError as erro_lexico:
        print(str(erro_lexico))
        return 1
    
    # bom tratamento mas deixei pra ver TODOS os tokens por enquanto
    #tokens_identificados = [
    #    token
    #    for token in lexer.tokens
    #    if token.tipo not in {TokenType.ERROR, TokenType.EOF}
    #]
    
    print(f"\nArquivo lido: {caminho_path}")
    print(f"Tokens identificados: {len(tokens_identificados)}")
    print("\nTokens (tupla):")
    for token in tokens_identificados:
        print((token.lexema, token.tipo.value, token.linha, token.coluna)) # imprimindo valores do TokenType ao inves do nome associado
    print("\nResumo:")
    print(f"- Identificados: {len(tokens_identificados)}")
    print(f"- Não identificados: {sum(1 for token in lexer.tokens if token.tipo == TokenType.ERROR)}")
    
    if profile:
        lexer.relatorio_performance()
    
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
        
        # Sempre adiciona relatório de performance
        file.write("\n" + "=" * 70 + "\n")
        file.write("RELATÓRIO DE PERFORMANCE - ANÁLISE LÉXICA\n")
        file.write("=" * 70 + "\n")
        tempo_total = (lexer._tempo_fim - lexer._tempo_inicio) * 1000
        total_tokens = (lexer._contagem_tokens_afd + lexer._contagem_tokens_string + 
                        lexer._contagem_tokens_char + lexer._contagem_tokens_numero + 
                        lexer._contagem_tokens_identificador)
        file.write(f"Tempo total:            {tempo_total:.2f} ms\n")
        file.write(f"Caracteres processados: {lexer._contagem_caracteres_processados}\n")
        file.write(f"Tamanho do código:      {lexer._tamanho_codigo_bytes:,} bytes\n")
        file.write(f"Tamanho de tokens:      {lexer._tamanho_tokens_bytes:,} bytes\n")
        file.write("\nTOKENS POR TIPO:\n")
        file.write(f"  - AFD:              {lexer._contagem_tokens_afd}\n")
        file.write(f"  - STRING_LITERAL:   {lexer._contagem_tokens_string}\n")
        file.write(f"  - CHAR_LITERAL:     {lexer._contagem_tokens_char}\n")
        file.write(f"  - NUMBER_*:         {lexer._contagem_tokens_numero}\n")
        file.write(f"  - IDENTIFIER:       {lexer._contagem_tokens_identificador}\n")
        file.write(f"  - Total:            {total_tokens}\n")
        file.write(f"  - Erros:            {lexer._contagem_erros}\n")
        if total_tokens > 0 and tempo_total > 0:
            tokens_por_segundo = total_tokens / (tempo_total / 1000)
            chars_por_segundo = lexer._contagem_caracteres_processados / (tempo_total / 1000)
            file.write(f"\nTaxas:\n")
            file.write(f"  - Tokens/segundo:   {tokens_por_segundo:,.0f}\n")
            file.write(f"  - Chars/segundo:    {chars_por_segundo:,.0f}\n")
        file.write("=" * 70 + "\n")

    ## ANÁLISE SINTÁTICA ##
    lista_enums = []
    for token in tokens_identificados:
        lista_enums.append(token.tipo.value)

    analisador_sintatico = AnalisadorSintatico(lista_enums) # Criando analisador
    analisador_sintatico.function()                         # Chamando function para iniciar a recursão
    
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
