# Vulto — Sistema (Vulto+ / Lojas / Estoque) — API

API do programa de pontos Vulto+ e, desde 2025, também do módulo de lojas (produtos, estoque, vendas e relatório).

## Rodar

```bash
python -m venv venv
source venv/bin/activate   # windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Docs em http://localhost:8000/docs

## Dados

Tudo fica em `data/`:

- `vulto.db` — banco (SQLite). Tabelas: `lojas`, `compras`, `pontos_mov`, `config`, `vendas`, `itens_venda`, `estoque`, `entradas_estoque`
- `clientes_fidelidade_FINAL_v3 (1).xlsx` — cadastro dos clientes Vulto+ (NÃO renomear, o código procura esse nome)
- `catalogo_vulto_2026_REVISADO_final.xlsx` — catálogo de produtos do time de Compras (uma aba por coleção)
- `contagem_inventario_set26.xlsx` — contagem física de setembro/26
- `vendas_batel_MANUAL_marco.xlsx` — vendas da Batel em março (PDV ficou fora do ar)
- `atendimentos_export_whatsapp_insta.csv` — export da ferramenta de atendimento (WhatsApp / Insta / e-mail)
- `REGRAS_OPERACAO.txt` — regras da operação (Diego)

## Endpoints principais

Login das lojas (tela `?admin=1` do front): `POST /admin/login` com o código do crachá ou a senha. Usuário do TI pra teste: código `9999`, senha `teste`.

Fidelidade: `/login`, `/clientes`, `/cliente/{cpf}`, `/extrato/{cpf}`, `/resgate`, `/compra`, `/exportar`

Lojas:

- `GET /produtos` e `GET /produtos/{sku}` — lê direto da planilha de Compras
- `GET /estoque?loja=` e `POST /estoque/ajuste` — estoque em tempo real por loja
- `GET /vendas`, `GET /vendas/{id}`, `POST /venda`, `POST /venda/{id}/cancelar`
- `GET /relatorio/faturamento?inicio=&fim=` — relatório oficial de faturamento (usado pelo financeiro)
- `GET /atendimentos` — lê o export da ferramenta de atendimento

## Regras

1 real = 1 ponto, online vale dobro. 100 pontos = R$10.

Site e App têm "loja" própria no sistema (5 e 6). O CD é a loja 7.

Qualquer dúvida falar com o Diego.
