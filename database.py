#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os

def conectar():
    return sqlite3.connect("oficina.db")

def criar_tabelas():
    # Exclui o banco se existir para recriar do zero
    if os.path.exists("oficina.db"):
        os.remove("oficina.db")
    
    conn = conectar()
    cursor = conn.cursor()
    
    # Criar tabela de clientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        endereco TEXT
    )
    """)
      # Criar tabela de ordens
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ordens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente_id INTEGER,
        data_entrada TEXT,
        data_saida TEXT,
        descricao TEXT,
        valor REAL,
        status TEXT,
        veiculo TEXT,
        placa TEXT,
        observacoes TEXT,
        FOREIGN KEY(cliente_id) REFERENCES clientes(id)
    )
    """)
    
    conn.commit()
    conn.close()