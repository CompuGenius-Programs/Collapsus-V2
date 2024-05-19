import sqlite3

import parsers


def create_table():
    conn = sqlite3.connect('grottos.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS grottos (
                name text,
                url text,
                special int,
                seed text,
                rank text,
                type text,
                floors text,
                boss text,
                monster_rank text,
                chests text,
                locations text,
                notes text,
                owner text
                )''')
    conn.commit()
    conn.close()


def insert_grotto(grotto):
    conn = sqlite3.connect('grottos.db')
    c = conn.cursor()

    c.execute('''INSERT INTO grottos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        grotto.name, grotto.url, grotto.special, grotto.seed, grotto.rank, grotto.type, grotto.floors, grotto.boss,
        grotto.monster_rank, grotto.chests, grotto.locations, grotto.notes, grotto.owner))
    conn.commit()
    conn.close()


def delete_grotto(user_id, grotto_note):
    conn = sqlite3.connect('grottos.db')
    c = conn.cursor()

    c.execute('''DELETE FROM grottos WHERE owner = ? AND notes = ?''', (user_id, grotto_note))
    conn.commit()
    conn.close()

    return c.rowcount > 0


def get_grottos(user_id):
    conn = sqlite3.connect('grottos.db')
    c = conn.cursor()

    c.execute('''SELECT * FROM grottos WHERE owner = ?''', (user_id,))
    grottos_db = c.fetchall()

    conn.close()
    grottos = [parsers.Grotto(*grotto) for grotto in grottos_db]
    return grottos


def confirm_unique_note(user_id, note):
    conn = sqlite3.connect('grottos.db')
    c = conn.cursor()

    c.execute('''SELECT * FROM grottos WHERE owner = ? AND notes = ?''', (user_id, note))
    grottos_db = c.fetchall()

    conn.close()
    return len(grottos_db) == 0
