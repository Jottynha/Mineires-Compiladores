<h1 align="center">
Trabalho de Compiladores

para a linguagem _Minerês_
</h1>

<div align="center">

![Python](https://img.shields.io/badge/python-blue?style=for-the-badge&logo=python&logoColor=white)
![VS Code](https://img.shields.io/badge/visual%20studio%20code-blue?style=for-the-badge)
![Ubuntu](https://img.shields.io/badge/ubuntu-orange?style=for-the-badge&logo=ubuntu&logoColor=white)

</div>

---

<div align="justify">
<p><strong>Disciplina:</strong> Compiladores<br>
<strong>Instituição:</strong> CEFET-MG Campus V<br>
<strong>Professor:</strong> Eduardo Gabriel Reis Miranda<br>
</div>

---

## 📖: Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Partes do projeto](#partes-do-projeto)
    - [Analisador Léxico](#parte-1-analisador-léxico)
    - [Analisador Sintático](#parte-2-analisador-sintático)
- [Como executar](#como-executar)
- [Colaboradores](#colaboradores)
- [Referências](#referências)

---
## Sobre o projeto:

<div align = "justify">
<p>Esse é o repositório de um projeto executado para a disciplina de Compiladores, voltado para a implementação em partes de um compilador/interpretador de uma linguagem esotérica chamada Minerês [1], criada pela turma da disciplina para a implementação do trabalho. A implementação é acompanhada em sala e dividida em partes para entrega e apresentação.</p>

<p>O Python foi escolhido como linguagem a ser utilizada pelos integrantes do grupo devido a familiaridade com seu uso. Até então, nenhuma biblioteca externa é utilizada no trabalho.</p>
</div>

---
#### ℹ️: Arquivos do repositório
---

```
├── exemplos
│   ├── 01_uai_mundo.txt
│   ├── 02_par_ou_impar.txt
│   ├── 03_switch_case.txt
│   ├── 04_controles.txt
│   ├── 05_teste_completo.txt
│   ├── 06_fibonacci.txt
│   ├── 07_codigo_errado.txt
│   ├── 08_par_impar_errado.txt
│   └── saida.txt
├── grafos
│   └── automato_simples.txt
├── mineres.gmr
├── README.md
└── src
    ├── analisador_sintatico.py
    ├── automato.py
    ├── lexer.py
    ├── main.py
    ├── mineires_token.py
    └── token_type.py
```
---

- `exemplos/`: casos de teste válidos e com erros.
    - `01_uai_mundo.txt`: O "Hello World" do Minerês;
    - `02_par_ou_impar.txt`: Verifica se um número é par ou ímpar;
    - `03_switch_case.txt`: Testa um switch case simples;
    - `04_controles.txt`: Testa desvios e laços de repetição;
    - `05_teste_completo.txt`: Teste mais abrangente da gramática;
    - `06_fibonacci.txt`: Implementação de Fibonacci não-recursivo em Minerês;
    - `07_codigo_errado.txt`: Testa um Uai Mundo com erro sintático;
    - `08_par_impar_errado.txt`: Testa um par ou ímpar com erro sintático;

- `grafos/`: pasta que armazena o conteúdo de AFDs analisados pelo script.
    - `automato_simples.txt`: Arquivo de texto qua armazena textualmente os estados e transições do AFD que descreve a linguagem Minerês.

- `mineres.gmr`: arquivo original da gramática do Minerês.

- `README.MD`: este arquivo.

- `src/`: pasta que armazena os principais scripts do projeto.
    - `src/analisador_sintatico.py`: arquivo de implementação da parte de análise sintática do projeto como através da classe `AnalisadorSintatico`;
    - `src/automato.py`: carrega e constrói o AFD definido em `grafos/automato_simples.txt`.
    - `src/lexer.py`: executa a análise léxica e gera tokens com posição (linha/coluna).
    - `src/token_type.py`: define `TokenType` e o mapeamento de palavras reservadas.
    - `src/mineires_token.py`: estrutura do token (`lexema`, `tipo`, `linha`, `coluna`).
    - `src/main.py`: ponto de entrada; lê arquivo, executa o lexer e grava saída.

---

## Partes do projeto:

O projeto foi, até então, dividido entre as seguintes partes:

---
### PARTE 1: Analisador Léxico
---
O analisador léxico da linguagem Mineires foi implementado com base em um AFD, priorizando previsibilidade, facilidade de evolução e mensagens de erro claras.

### Análise léxica (resumo)
O `Lexer` percorre o código caractere a caractere e combina duas estratégias:
- **AFD para reconhecimento base:** palavras reservadas, identificadores, operadores e delimitadores são reconhecidos por estados/transições definidos em `grafos/automato_simples.txt`.
- **Rotinas dedicadas para casos sensíveis:** `STRING_LITERAL`, `CHAR_LITERAL`, validação de números e comentários multilinha são tratados por funções específicas no `lexer`, porque exigem regras contextuais e validação adicional.

### Decisões de implementação
Separou-se os dados da lógica, o AFD fica no arquivo de grafo, enquanto a lógica de execução fica em `src/analisador_lexico/lexer.py`, facilitando manutenção e ajustes da linguagem. Além disso há o maior lexema válido (maximal munch), pois o lexer tenta consumir o maior trecho reconhecível antes de classificar o token. Ademais palavras reservadas só são classificadas como tal quando o lexema é exato; se estiverem concatenadas em um nome maior, o token vira `IDENTIFIER`. E, ao detectar erro léxico, a análise é interrompida com `LexicalError` e posição precisa (linha/coluna), o que simplifica o diagnóstico.

---
### PARTE 2: Analisador Sintático
---
<div align="justify">
<p>A implementação do analisador sintático se deu através do arquivo <i>analisador_sinatico.py</i>, onde a classe AnalisadorSintatico foi devidamente implementada para uso na main.</p> 
</div>

### Análise Sintática (resumo)
- O analisador sintático recebe uma lista de Tokens gerada pelo analisador léxico;
- Mantém um ponteiro para a posição atual na lista de Tokens;
- Percorre os tokens através de um algoritmo descendente recursivo [2] chamando métodos que correspondem às regras da gramática do Minerês;
    - Em casos válidos, incrementa o ponteiro (consumindo o token válido) e continua a execução dos métodos; 
    - Em casos de erro, chama lança o erro `MineresSyntaxError`;
- Para iniciar a recursão, chama o método `function()`, que inicia a verificação da gramática pelo topo e "desce" recursivamente para validar o restante.

### Decisões de implementação:
- Durante a verificação de tokens, a comparação é feita com valores inteiros (embora a classe armazene e use tokens para outras funções);
- O log das verificações é disponibilizado no arquivo `saida.txt` para verificação posterior, embora o terminal notifique o primeiro erro encontrado ou se a análise foi bem-sucedida;



## Como executar:

#### Execução direta pelo _main.py_ 
Execute pelo arquivo `main.py`. Isso pode ser feito via terminal da seguinte forma:

```bash
python src/main.py
```
#### Execução por exemplos:

Sem argumento, a aplicação lista os arquivos de `exemplos/` e permite escolher um.
Também é possível informar o arquivo diretamente:

```bash
python src/main.py exemplos/01_valido_basico.mineires.txt
```

## Colaboradores:
| Colaborador | Perfil |
|-------------|--------|
| Frank Leite Lemos Costa | [@frankleitelemoscosta](https://github.com/frankleitelemoscosta)
| João Pedro Rodrigues Silva | [@jottynha](https://github.com/jottynha)
| Samuel Silva Gomes | [@samuelsilvg](https://github.com/samuelsilvg)

---

### 📚: Referências
[1]: [Referência de linguagem do Minerês](https://mineres-language.github.io/)

[2]: [Referência para implementação do analisador sintático recursivo](https://www.geeksforgeeks.org/compiler-design/recursive-descent-parser/)

---

<div align ="center">
made with ❤️ | 2026
</div>