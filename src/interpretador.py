class ErroExecucao(Exception):
    pass

class Interpretador:
    def __init__(self, codigo_fonte):
        self.codigo_fonte = codigo_fonte
        self.labels = {}
        self.variaveis = {}
        self.saida = []
        self.erros = []
        self.pc = 0
    def mapear_labels(self):
        for idx, instrucao in enumerate(self.codigo_fonte):
            if instrucao[0] == "label":
                self.labels[instrucao[1]] = idx
    def iniciar_dicionario(self):
        for instrucao in self.codigo_fonte:
            if instrucao[0] == "att":
                destino = instrucao[1]
                # destino pode ser ('var', nome) ou nome cru
                if isinstance(destino, (tuple, list)) and len(destino) == 2 and destino[0] == 'var':
                    nome = destino[1]
                else:
                    nome = destino
                self.variaveis[nome] = 0
    def executar(self):
        self.mapear_labels()
        self.iniciar_dicionario()
        self.pc = 0
        while self.pc < len(self.codigo_fonte):
            instrucao = self.codigo_fonte[self.pc]
            try:
                self._executar_instrucao(instrucao)
                self.pc += 1
            except ErroExecucao as e:
                self.erros.append(str(e))
                return False
        return True
    def _executar_instrucao(self, instrucao):
        op = instrucao[0]
        if op == "label":
            return
        if op == "att":
            destino = instrucao[1]
            if isinstance(destino, (tuple, list)) and len(destino) == 2 and destino[0] == 'var':
                var_nome = destino[1]
            else:
                var_nome = destino
            valor = self._avaliar_expressao(instrucao[2])
            if var_nome not in self.variaveis:
                raise ErroExecucao(f"Variável não declarada: '{var_nome}'")
            self.variaveis[var_nome] = valor
            return
        if op == "jump":
            label = instrucao[1]
            if label not in self.labels:
                raise ErroExecucao(f"Label não encontrada: '{label}'")
            self.pc = self.labels[label] - 1
            return
        if op == "if":
            condicao = self._avaliar_expressao(instrucao[1])
            label_true = instrucao[2]
            label_false = instrucao[3]
            destino = label_true if condicao != 0 else label_false
            if destino not in self.labels:
                raise ErroExecucao(f"Label não encontrada: '{destino}'")
            self.pc = self.labels[destino] - 1
            return
        if op == "call":
            func = instrucao[1]
            if func != "print":
                raise ErroExecucao(f"Chamada não suportada: '{func}'")
            valor = instrucao[2] if instrucao[2] is not None else instrucao[3]
            valor_avaliado = self._avaliar_expressao(valor)
            self.saida.append(str(valor_avaliado))
            return
        if op in {"add", "sub", "mult", "div", "divI", "mod", "eq", "dif", "les", "leq", "grt", "geq", "and", "or", "xor", "not"}:
            destino = instrucao[1]
            resultado = self._avaliar_operacao(instrucao)
            if destino not in self.variaveis:
                self.variaveis[destino] = 0
            self.variaveis[destino] = resultado
            return
        raise ErroExecucao(f"Instrução desconhecida: '{op}'")
    def _avaliar_expressao(self, expr):
        if expr is None:
            return 0
        if isinstance(expr, (int, float)):
            return expr
        # Operando tipado: ('var','x'), ('str','...'), ('num','42'), ('bool','1')
        if isinstance(expr, (tuple, list)) and len(expr) == 2 and expr[0] in {'var', 'str', 'num', 'bool', 'char'}:
            tipo, val = expr[0], expr[1]
            if tipo == 'var':
                if val in self.variaveis:
                    return self.variaveis[val]
                raise ErroExecucao(f"Variável não declarada: '{val}'")
            if tipo == 'str' or tipo == 'char':
                # se for temporário/variável, busca o valor já calculado
                if isinstance(val, str) and val in self.variaveis:
                    return self.variaveis[val]
                return val
            if tipo == 'num':
                # aceita inteiros e floats na forma textual
                # se for temporário/variável nome, retorna seu valor se existir
                if isinstance(val, str) and val in self.variaveis:
                    return self.variaveis[val]
                if isinstance(val, (int, float)):
                    return val
                s = str(val)
                return float(s) if '.' in s else int(s)
            if tipo == 'bool':
                if isinstance(val, str) and val in self.variaveis:
                    return 1 if self.variaveis[val] != 0 else 0
                return 1 if str(val) == '1' else 0
        # Se for uma instrução/operacao representada por tupla maior
        if isinstance(expr, (tuple, list)):
            return self._avaliar_operacao(expr)
        if isinstance(expr, str):
            # string crua pode ser nome de variável, temporário ou literal com aspas
            if len(expr) >= 2 and ((expr[0] == '"' and expr[-1] == '"') or (expr[0] == "'" and expr[-1] == "'")):
                return expr[1:-1]
            if expr.isdigit() or (expr.startswith('-') and expr[1:].isdigit()):
                return int(expr)
            if expr in self.variaveis:
                return self.variaveis[expr]
            raise ErroExecucao(f"Variável não declarada: '{expr}'")
        raise ErroExecucao(f"Expressão inválida: {expr}")
    def _avaliar_operacao(self, instrucao):
        op = instrucao[0]
        if op == "not":
            valor = self._avaliar_expressao(instrucao[2])
            return 0 if valor != 0 else 1
        esq = self._avaliar_expressao(instrucao[2])
        dir = self._avaliar_expressao(instrucao[3])
        if op == "add":
            # Concatenação de strings ou adição numérica
            # Se ambos são strings, concatena; caso contrário, soma números
            if isinstance(esq, str) and isinstance(dir, str):
                return esq + dir
            return esq + dir
        if op == "sub":
            return esq - dir
        if op == "mult":
            return esq * dir
        if op in {"div", "divI", "mod"}:
            if dir == 0:
                raise ErroExecucao("Divisão por zero")
            if op == "div":
                return esq / dir
            if op == "divI":
                return esq // dir
            return esq % dir
        if op == "eq":
            return 1 if esq == dir else 0
        if op == "dif":
            return 1 if esq != dir else 0
        if op == "les":
            return 1 if esq < dir else 0
        if op == "leq":
            return 1 if esq <= dir else 0
        if op == "grt":
            return 1 if esq > dir else 0
        if op == "geq":
            return 1 if esq >= dir else 0
        if op == "and":
            return 1 if (esq != 0 and dir != 0) else 0
        if op == "or":
            return 1 if (esq != 0 or dir != 0) else 0
        if op == "xor":
            return 1 if ((esq != 0) ^ (dir != 0)) else 0
        raise ErroExecucao(f"Operação inválida: '{op}'")
    def get_saida(self):
        return "\n".join(self.saida)
    def get_erros(self):
        return "\n".join(self.erros) if self.erros else None
    def printar_info(self):
        print("\n== INTERPRETADOR ==")
        print("Código intermediário:")
        print(self.codigo_fonte)
        print("\nMapeamento de labels:")
        for label, idx in self.labels.items():
            print(f"{label} -> {idx}")
        print("\nDicionário de variáveis:")
        for var, valor in self.variaveis.items():
            print(f"{var} -> {valor}")
        if self.saida:
            print("\nSaída do programa:")
            print(self.get_saida())
        if self.erros:
            print("\nErros durante execução:")
            for erro in self.erros:
                print(f"! {erro}")

