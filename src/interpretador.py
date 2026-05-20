class Interpretador:
    def __init__(self, codigo_fonte):
        self.codigo_fonte = codigo_fonte
        self.labels = {}
        self.variaveis = {}
    def mapear_labels(self):
        for idx, instrucao in enumerate(self.codigo_fonte):
            print(f"Analisando instrução: {instrucao[0]}")
            if instrucao[0] == "label":
                self.labels[instrucao[1]] = idx+1
    def iniciar_dicionario(self, codigo_fonte):
        for instrucao in codigo_fonte:
            if instrucao[0] == "att":
                self.variaveis[instrucao[1]] = instrucao[2]
    def printar_codigo(self):
        print(self.codigo_fonte)
        print("\nMapeamento de labels:")
        for label, idx in self.labels.items():
            print(f"{label} -> {idx}")
        print("\nDicionário de variáveis:")
        for var, valor in self.variaveis.items():
            print(f"{var} -> {valor}")

