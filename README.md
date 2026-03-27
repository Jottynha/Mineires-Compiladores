<h1 align="center">
Compilador de Mineires
</h1>

<h3 align="center">
Desenvolvimento de um compilador para a linguagem autoral denominada "Mineires".
</h3>

<div align="center">

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

</div>

---

<div align="justify">
<p><strong>Disciplina:</strong> Compiladores<br>
<strong>Instituição:</strong> Centro Federal de Educação Tecnológica de Minas Gerais (CEFET-MG) - Campus V Divinópolis<br>
<strong>Professor:</strong> Eduardo Miranda<br>
</div>

---

## Analisador Léxico
O analisador léxico da linguagem Mineires foi implementado com base em AFD, priorizando previsibilidade, facilidade de evolução e mensagens de erro claras.

### Estrutura do projeto
- `src/analisador_lexico/automato.py`: carrega e constrói o AFD definido em `grafos/automato_simples.txt`.
- `src/analisador_lexico/lexer.py`: executa a análise léxica e gera tokens com posição (linha/coluna).
- `src/analisador_lexico/token_type.py`: define `TokenType` e o mapeamento de palavras reservadas.
- `src/analisador_lexico/mineires_token.py`: estrutura do token (`lexema`, `tipo`, `linha`, `coluna`).
- `src/analisador_lexico/main.py`: ponto de entrada; lê arquivo, executa o lexer e grava saída.
- `exemplos/`: casos de teste válidos e com erros fatais.

## Análise léxica (resumo)
O `Lexer` percorre o código caractere a caractere e combina duas estratégias:
- **AFD para reconhecimento base:** palavras reservadas, identificadores, operadores e delimitadores são reconhecidos por estados/transições definidos em `grafos/automato_simples.txt`.
- **Rotinas dedicadas para casos sensíveis:** `STRING_LITERAL`, `CHAR_LITERAL`, validação de números e comentários multilinha são tratados por funções específicas no `lexer`, porque exigem regras contextuais e validação adicional.

### Decisões de implementação
Separou-se os dados da lógica, o AFD fica no arquivo de grafo, enquanto a lógica de execução fica em `src/analisador_lexico/lexer.py`, facilitando manutenção e ajustes da linguagem. Além dissohá o maior lexema válido (maximal munch), pois o lexer tenta consumir o maior trecho reconhecível antes de classificar o token. Ademais palavras reservadas só são classificadas como tal quando o lexema é exato; se estiverem concatenadas em um nome maior, o token vira `IDENTIFIER`. E ao detectar erro léxico, a análise é interrompida com `LexicalError` e posição precisa (linha/coluna), o que simplifica o diagnóstico.

### Erros fatais cobertos
- string não fechada;
- número malformado;
- símbolo desconhecido;
- comentário multilinha não fechado.

## Execução
Execute pela `main`:

```bash
python src/analisador_lexico/main.py
```

Sem argumento, a aplicação lista os arquivos de `exemplos/` e permite escolher um.
Também é possível informar o arquivo diretamente:

```bash
python src/analisador_lexico/main.py exemplos/programa_exemplo.mineires.txt
```
