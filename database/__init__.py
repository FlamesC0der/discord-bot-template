import os
import sqlite3

class DatabaseManager():
  def __init__(self, connection: sqlite3.Connection) -> None:
    self.conn = connection
    self.cur = self.conn.cursor()
