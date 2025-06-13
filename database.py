# database.py
import sqlite3

def conectar():
    return sqlite3.connect("oficina.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        veiculo TEXT,
        placa TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ordens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        data_entrada TEXT,
        data_saida TEXT,
        descricao TEXT,
        valor REAL,
        status TEXT,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    """)
    
    conn.commit()
    conn.close()
