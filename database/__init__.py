import os
import sqlite3

class DatabaseManager():
  def __init__(self, connection: sqlite3.Connection) -> None:
    self.conn = connection
    self.cur = self.conn.cursor()
  
  def add_money(self, user_id: int, server_id: int, amount: int) -> int:
    rows = self.conn.execute(
      "SELECT id FROM economy WHERE user_id=? AND server_id=? ORDER BY id DESC LIMIT 1",
      (
        user_id,
        server_id,
      ),
    ).fetchall()

    if rows:
      id = rows[0][0]
      self.conn.execute(
        "UPDATE economy SET money = (?) WHERE id = (?)",
        (amount, id)
      )
    else:
      a = self.conn.execute("SELECT * FROM economy").fetchall()
      id = 1
      if a:
        id = len(a[0])
      self.conn.execute(
        "INSERT INTO economy(id, user_id, server_id, money) VALUES (?, ?, ?, ?)",
        (
          id,
          user_id,
          server_id,
          amount
        )
      )
    self.conn.commit()
    return id
