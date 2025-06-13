# models.py
from database import conectar

def adicionar_cliente(nome, telefone, veiculo, placa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (nome, telefone, veiculo, placa)
        VALUES (?, ?, ?, ?)
    """, (nome, telefone, veiculo, placa))
    conn.commit()
    conn.close()

def buscar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes

def adicionar_ordem(cliente_id, data_entrada, data_saida, descricao, valor, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ordens (cliente_id, data_entrada, data_saida, descricao, valor, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (cliente_id, data_entrada, data_saida, descricao, valor, status))
    conn.commit()
    conn.close()

def listar_ordens():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ordens.id, clientes.nome, ordens.data_entrada, ordens.data_saida,
               ordens.descricao, ordens.valor, ordens.status
        FROM ordens
        JOIN clientes ON clientes.id = ordens.cliente_id
        ORDER BY ordens.id DESC
    """)
    ordens = cursor.fetchall()
    conn.close()
    return ordens
