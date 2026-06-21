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
## Arquitetura Geral do Sistema

O sistema foi desenvolvido seguindo a arquitetura clássica de compiladores, composta pelas etapas de análise léxica, análise sintática, análise semântica, geração de código intermediário e interpretação.

O fluxo de execução do compilador é representado na Figura abaixo.

```text
Código Fonte
     │
     ▼
Análise Léxica
     │
     ▼
Lista de Tokens
     │
     ▼
Análise Sintática
     │
     ▼
Análise Semântica
     │
     ▼
Código Intermediário
     │
     ▼
Interpretador
     │
     ▼
Saída do Programa
```
---
#### ℹ️: Arquivos do repositório
---

```
├── exemplos
│   ├── 01_teste_completo.txt
│   ├── 02_loop_while.txt
│   ├── 03_loop_for.txt
│   ├── 04_switch_case.txt
│   ├── 05_fibonacci.txt
│   ├── 06_codigo_errado.txt
│   ├── 07_erro_atrib.txt
│   ├── 08_concatenar.txt
│   ├── 09_invalido_char_op.txt
│   ├── 10_xove(read).txt
│   ├── 11_eq_str.txt
│   ├── 12_conversao_numeral.txt
│   ├── 13_dif_types.txt
│   ├── 14_div_zero.txt
│   ├── 15_redeclaracao.txt
│   ├── 16_declaracao_previa.txt
│   ├── 17_OR_op.txt
│   ├── 18_str_op_error.txt
│   ├── 19_condicao_nao_booleana_if.txt
│   ├── 20_caso_duplicado_switch.txt
│   └── saida.txt
├── grafos
│   └── automato_simples.txt
├── mineres.gmr
├── README.md
└── src
    ├── analisador_sintatico.py
    ├── automato.py
    ├── interpretador.py
    ├── lexer.py
    ├── main.py
    ├── mineires_token.py
    └── token_type.py
```

---

- `exemplos/`: Esta pasta contém casos de teste válidos e com erros para testar a funcionalidade do Minerês. Alguns exemplos incluem:
  - `01_teste_completo.txt`: Um exemplo completo de diversas funções do Minerês.
  - `02_loop_while.txt`: Um exemplo que imprime valores usando um loop while.
  - `03_loop_for.txt`: Um exemplo que usa um loop for com teste de break e continue.
  - `04_switch_case.txt`: Um exemplo que testa um switch case simples.
  - `05_fibonacci.txt`: Um exemplo que implementa a sequência de Fibonacci não-recursiva em Minerês.
  - `06_codigo_errado.txt`: Um exemplo com erro sintático.
  - `07_erro_atrib.txt`: Um exemplo com erro de atribuição.
  - `08_concatenar.txt`: Um exemplo que concatena strings.
  - `09_invalido_char_op.txt`: Um exemplo com operação inválida com caracteres (atribuir dois char dentro de um).
  - `10_xove(read).txt`: Um exemplo que usa a função `read` para ler uma variável.
  - `11_eq_str.txt`: Um exemplo que compara uma string com outra.
  - `12_conversao_numeral.txt`: Um exemplo que converte número octal para um número decimal.
  - `13_dif_types.txt`: Um exemplo de erro que compara tipos de dados diferentes.
  - `14_div_zero.txt`: Um exemplo de erro que divide por zero.
  - `15_redeclaracao.txt`: Um exemplo de erro que redeclara uma variável.
  - `16_declaracao_previa.txt`: Um exemplo de erro que declara uma variável previamente.
  - `17_OR_op.txt`: Um exemplo que usa operador OR.
  - `18_str_op_error.txt`: Um exemplo com operação inválida com strings.
  - `19_condicao_nao_booleana_if.txt`: Um exemplo com condição não booleana em um if.
  - `20_caso_duplicado_switch.txt`: Um exemplo com caso duplicado em um switch.

- `grafos/`: Esta pasta contém o conteúdo de AFDs analisados pelo script. Atualmente, o arquivo `automato_simples.txt` é usado para construir o AFD que descreve a linguagem Minerês.

- `mineres.gmr`: Este arquivo contém a gramática original do Minerês.

- `README.MD`: Este arquivo descreve o projeto e seus arquivos principais.

- `src/`: Esta pasta contém os principais scripts do projeto.
  - `src/analisador_sintatico.py`: Este arquivo contém a implementação da parte de análise sintática do projeto, representada pela classe `AnalisadorSintatico`.
  - `src/automato.py`: Este arquivo carrega e constrói o AFD definido em `grafos/automato_simples.txt`.
  - `src/interpretador.py`: Este arquivo é responsável por interpretar o código do Minerês, executando as ações correspondentes aos tokens e estruturas sintáticas reconhecidas.
  - `src/lexer.py`: Este arquivo executa a análise léxica e gera tokens com posição (linha/coluna).
  - `src/token_type.py`: Este arquivo define `TokenType` e o mapeamento de palavras reservadas.
  - `src/mineires_token.py`: Este arquivo define a estrutura do token (`lexema`, `tipo`, `linha`, `coluna`).
  - `src/main.py`: Este arquivo é o ponto de entrada do projeto. Ele lê um arquivo, executa o lexer e grava a saída.

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

---
### PARTE 3: Analisador Semântica
---

A análise semântica foi incorporada ao analisador sintático por meio de verificações executadas durante o percurso da árvore sintática implícita.

O principal objetivo dessa etapa é garantir que programas sintaticamente válidos também sejam semanticamente consistentes.

As verificações implementadas incluem:

- Declaração prévia de variáveis antes de sua utilização;
- Detecção de redeclaração de identificadores;
- Verificação de compatibilidade entre tipos;
- Validação de expressões lógicas em estruturas condicionais e de repetição;
- Verificação de atribuições incompatíveis;
- Detecção de valores duplicados em estruturas `dependenu`;
- Verificação de operações aritméticas aplicadas apenas a tipos numéricos.

Para auxiliar essas verificações, o compilador mantém uma tabela de símbolos simplificada contendo os identificadores declarados e seus respectivos tipos.

#### Geração de Código Intermediário

Após a validação sintática e semântica, o compilador gera uma representação intermediária do programa baseada em instruções de três endereços.

Essa representação abstrai os detalhes da linguagem fonte e facilita a execução posterior pelo interpretador.

As instruções geradas incluem:

- Atribuições (`att`);
- Operações aritméticas (`add`, `sub`, `mult`, `div`, `divI`, `mod`);
- Operações relacionais (`eq`, `dif`, `les`, `leq`, `grt`, `geq`);
- Operações lógicas (`and`, `or`, `xor`, `not`);
- Saltos incondicionais (`jump`);
- Saltos condicionais (`if`);
- Definição de rótulos (`label`);
- Chamadas de funções internas (`call`).

O uso de código intermediário permite desacoplar a etapa de análise da etapa de execução, aproximando a implementação da estrutura encontrada em compiladores reais.

---
### PARTE 4: Interpretador
---

O interpretador é responsável por executar o código intermediário gerado pelo compilador.

Durante a execução, são mantidas estruturas responsáveis por:

- Controle do fluxo de execução;
- Armazenamento de variáveis;
- Avaliação de expressões;
- Resolução de rótulos;
- Tratamento de operações aritméticas e lógicas;
- Entrada e saída de dados.

Além disso, o interpretador realiza verificações em tempo de execução, como divisão por zero e acesso a variáveis inexistentes.

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
