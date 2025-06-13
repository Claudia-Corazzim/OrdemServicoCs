# models.py
from database import conectar

def adicionar_cliente(nome, telefone, endereco, veiculo, placa):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (nome, telefone, endereco, veiculo, placa)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, telefone, endereco, veiculo, placa))
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
               ordens.descricao, ordens.valor, ordens.status, clientes.telefone,
               clientes.endereco, clientes.veiculo, clientes.placa
        FROM ordens
        JOIN clientes ON clientes.id = ordens.cliente_id
        ORDER BY ordens.id DESC
    """)
    ordens = cursor.fetchall()
    conn.close()
    return ordens

def excluir_cliente(cliente_id):
    conn = conectar()
    cursor = conn.cursor()
    try:
        # Primeiro excluir as ordens de serviço relacionadas
        cursor.execute("DELETE FROM ordens WHERE cliente_id = ?", (cliente_id,))
        
        # Depois excluir o cliente
        cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        
        conn.commit()
    except Exception as e:
        print(f"Erro ao excluir cliente: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()

def excluir_ordem(ordem_id):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM ordens WHERE id = ?", (ordem_id,))
        conn.commit()
    except Exception as e:
        print(f"Erro ao excluir ordem: {e}")
        conn.rollback()
        raise e
    finally:
        conn.close()
