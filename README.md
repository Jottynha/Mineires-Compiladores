# Mineires 
## Raiz do projeto
- `README.md`: documentação básica do projeto.
- `Elementos da Linguagem em Minerês.xlsx`: material de referência da linguagem.

## Pasta `src/`
- `automato.py`: definição do AFD (`Automato`) e funções para montar o autômato a partir de `grafos/automato_simples.txt`.
- `lexer.py`: analisador léxico que percorre o código fonte caractere a caractere usando o AFD.
- `main.py`: ponto de entrada para ler um arquivo `.mineires.txt`, executar o lexer e imprimir tokens/resumo.
- `token_type.py`: enum `TokenType` e mapeamento `RESERVED_WORDS` das palavras reservadas.
- `mineires_token.py`: classe `Token` (lexema, tipo, linha e coluna).

## Pasta `exemplos/`
- `programa_exemplo.mineires.txt`: exemplo simples de programa em Mineires para testar o lexer.

## Pasta `grafos/`
- `automato_simples.txt`: descrição textual do AFD (estados e transições) lida por `automato.py`.
