import os
import pandas as pd

CATALOGO = os.path.join(os.path.dirname(__file__), "data", "catalogo_vulto_2026_REVISADO_final.xlsx")

# cada aba foi montada por uma pessoa diferente, entao cada uma tem um layout
# (header = linha do cabecalho, comecando do 0)
ABAS = {
    "VERAO 25": {"header": 0, "sku": "SKU", "nome": "Produto", "cat": "Categoria", "cor": "Cor", "tam": "Tam",
                 "preco": "Preço", "custo": "Custo", "ean": "EAN"},
    "inverno25": {"header": 2, "sku": "cod", "nome": "descricao", "cat": "cat", "cor": "cor", "tam": "tamanho",
                  "preco": "preco venda", "custo": "custo unit", "ean": "ean13"},
    "Verão 26": {"header": 0, "sku": "Código", "nome": "Nome", "cat": "Categoria", "cor": "Cor", "tam": "Tamanho",
                 "preco": "Preço (R$)", "custo": "Custo", "ean": "EAN"},
    "Atemporais": {"header": 0, "sku": "sku", "nome": "nome", "cat": "categoria", "cor": "cor", "tam": "tam",
                   "preco": "preco", "custo": "custo_medio", "ean": "ean"},
    # a antiga tem os skus de 2024 que ainda vendem, nao tirar
    "PLANILHA ANTIGA NAO USAR": {"header": 1, "sku": "SKU", "nome": "DESCRICAO", "cat": "GRUPO", "cor": "COR",
                                 "tam": "TAM", "preco": "PRECO", "custo": "CUSTO", "ean": "EAN"},
}

_cache = None


def parse_preco(p):
    try:
        if p is None or p == "":
            return None
        if isinstance(p, (int, float)):
            if p != p:  # nan
                return None
            return float(p)
        p = str(p).replace("R$", "").replace(" ", "").replace(",", ".")
        return float(p)
    except:
        print("preco invalido", p)
        return None


def ler_catalogo(force=False):
    global _cache
    if _cache is not None and not force:
        return _cache
    produtos = []
    for aba, cfg in ABAS.items():
        try:
            df = pd.read_excel(CATALOGO, sheet_name=aba, header=cfg["header"], dtype=object)
        except Exception as e:
            print("erro lendo aba", aba, e)
            continue
        df = df.fillna("")
        for i, row in df.iterrows():
            sku = str(row.get(cfg["sku"], "")).strip()
            if sku == "":
                continue
            produtos.append({
                "sku": sku,
                "nome": row.get(cfg["nome"], ""),
                "categoria": row.get(cfg["cat"], ""),
                "cor": row.get(cfg["cor"], ""),
                "tamanho": str(row.get(cfg["tam"], "")),
                "preco": parse_preco(row.get(cfg["preco"])),
                "custo": parse_preco(row.get(cfg["custo"])),
                "ean": str(row.get(cfg["ean"], "")),
                "colecao": aba,
            })
    _cache = produtos
    print("catalogo carregado:", len(produtos), "produtos")
    return produtos


def busca_produto(sku):
    achou = None
    for p in ler_catalogo():
        if p["sku"].upper() == sku.upper().strip():
            achou = p  # pega o mais novo
    return achou
