def conect_mysql(user, password):
    import mysql.connector

    connection = mysql.connector.connect(
        host="sistema88.ddns.net",
        port=50505,
        database="DB88",
        user=user,
        password=password
    )

    return connection


def registrar_cliente(cursor, nome, bairro, sexo, telefone, captacao, return_id=False):
    id_cliente = cursor.execute("SELECT MAX(id_cliente) FROM clientes").fetchone()[0] + 1

    cursor.execute(
        "INSERT INTO clientes (nome, bairro, sexo, telefone, captacao) VALUES (%s, %s, %s, %s, %s)",
        (nome, bairro, sexo, telefone, captacao)
    )

    cursor.connection.commit()

    if return_id:
        return id_cliente


def registrar_venda(cursor, id_cliente, data, hora, canal_aquisicao, forma_recebimento, valor_faturado, taxa_entrega, itens_venda, return_id=False):
    id_venda = cursor.execute("SELECT MAX(id_venda) FROM vendas").fetchone()[0] + 1

    cursor.execute(
        "INSERT INTO vendas (id_cliente, data, hora, canal_aquisicao, forma_recebimento, valor_faturado, taxa_entrega) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (id_cliente, data, hora, canal_aquisicao, forma_recebimento, valor_faturado, taxa_entrega)
    )

    for item in itens_venda:
        sku, qtd, preco_und, cmmv = item if type(item) == tuple else itens_venda
        cursor.execute(
            "INSERT INTO itens_venda (id_venda, sku, qtd, preco_und, cmmv) VALUES (%s, %s, %s, %s, %s)" ,
            (id_venda, sku, qtd, preco_und, cmmv)
        )

    cursor.connection.commit()

    if return_id:
        return id_venda


def registrar_produto(cursor, marca, modelo, categoria, variacao, return_sku=False):
    sku = cursor.execute("SELECT MAX(sku) FROM produtos").fetchone()[0] + 1

    cursor.execute(
        "INSERT INTO produtos (marca, modelo, categoria, variacao) VALUES (%s, %s, %s, %s)",
        (marca, modelo, categoria, variacao)
    )

    cursor.connection.commit()

    if return_sku:
        return sku


def registrar_compra(cursor, app, conta, forma_pagamento, qtd_itens, data_compra, custo_base, frete, custo_final, itens_compra, return_id=False):
    id_compra = cursor.execute("SELECT MAX(id_compra) FROM compras").fetchone()[0] + 1

    impostos = int(custo_final) - (int(custo_base) + int(frete))

    cursor.execute(
        "INSERT INTO compras (app, conta, forma_pagamento, data_compra, custo_base, frete, impostos, custo_final) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (app, conta, forma_pagamento, qtd_itens, data_compra, custo_base, frete, impostos, custo_final)
    )

    for item in itens_compra:
        sku, fornecedor, status, qtd, custo_unt_base = item if type(item) == tuple else itens_compra
        cursor.execute(
            "INSERT INTO itens_compra (id_compra, sku, fornecedor, status, qtd, custo_unt_base) VALUES (%s, %s, %s, %s, %s)",
            (id_compra, sku, fornecedor, "não confirmado", qtd, custo_unt_base)
        )

    cursor.connection.commit()

    if return_id:
        return id_compra

