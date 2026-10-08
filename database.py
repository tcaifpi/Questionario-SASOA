import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "avaliacoes_sasoa.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS avaliacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT,
            tipo_lote TEXT,
            perfil TEXT,
            q1_clareza INTEGER,
            q2_seguranca INTEGER,
            q3_suap INTEGER,
            q4_pi INTEGER,
            q5_royalties INTEGER,
            q6_global INTEGER,
            comentarios TEXT
        )
    """)
    conn.commit()
    conn.close()

def salvar_feedback(perfil, q1, q2, q3, q4, q5, q6, comentarios):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("""
        INSERT INTO avaliacoes (
            data_hora, tipo_lote, perfil, 
            q1_clareza, q2_seguranca, q3_suap, 
            q4_pi, q5_royalties, q6_global, comentarios
        )
        VALUES (?, 'pos_deposito_continuo', ?, ?, ?, ?, ?, ?, ?, ?)
    """, (data_hora, perfil, q1, q2, q3, q4, q5, q6, comentarios))
    conn.commit()
    conn.close()

def carregar_dados():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM avaliacoes", conn)
    conn.close()
    return df
