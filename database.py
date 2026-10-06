
import sqlite3
import pandas as pd
from datetime import datetime

def init_db():
    conn = sqlite3.connect('sasoa_triagens.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS triagens (
            protocolo TEXT PRIMARY KEY,
            data_hora TEXT,
            admissibilidade TEXT,
            trl_stange TEXT,
            estrategia_pi TEXT,
            exclusividade TEXT,
            status_final TEXT
        )
    ''')
    conn.commit()
    conn.close()

def salvar_triagem(protocolo, admissibilidade, trl, pi, exclusividade, status_final):
    conn = sqlite3.connect('sasoa_triagens.db')
    c = conn.cursor()
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    c.execute("INSERT INTO triagens VALUES (?, ?, ?, ?, ?, ?, ?)",
              (protocolo, data_hora, admissibilidade, trl, pi, exclusividade, status_final))
    conn.commit()
    conn.close()

def carregar_dados():
    conn = sqlite3.connect('sasoa_triagens.db')
    df = pd.read_sql_query("SELECT * FROM triagens ORDER BY data_hora DESC", conn)
    conn.close()
    return df
