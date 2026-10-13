class Trie:
    def __init__(self):
        self.raiz = {}

    def inserir(self, palavra):
        no = self.raiz

        for caractere in palavra:
            no = no.setdefault(caractere, {})

        no["*"] = palavra

    def buscar_prefixo(self, prefixo):
        no = self.raiz

        for caractere in prefixo:
            if caractere not in no:
                return []
            no = no[caractere]

        return self._coletar(no)

    def _coletar(self, no):
        encontradas = []

        for chave, valor in no.items():
            if chave == "*":
                encontradas.append(valor)
            else:
                encontradas.extend(self._coletar(valor))

        return encontradas


def construir_trie(df, coluna):
    trie = Trie()

    for valor in df[coluna].unique():
        trie.inserir(valor)

    return trie