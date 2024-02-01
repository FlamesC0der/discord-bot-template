import sqlite3


class DatabaseManager():
    def __init__(self, connection: sqlite3.Connection) -> None:
        self.conn = connection

    def set_money(self, user_id: int, server_id: int, amount: int) -> str:
        result = self.conn.execute(
            "SELECT id FROM economy WHERE server_id=? AND user_id=?",
            (
                server_id,
                user_id
            )
        ).fetchone()
        if not result:
            self.conn.execute(
                "INSERT INTO economy (server_id, user_id, money) VALUES (?, ?, ?)",
                (
                    server_id,
                    user_id,
                    amount
                )
            )
        else:
            self.conn.execute(
                "UPDATE economy SET money = ? WHERE server_id = ? AND user_id = ?",
                (
                    amount,
                    server_id,
                    user_id
                )
            )
        self.conn.commit()
        return "ok"

    def get_top(self, server_id: int) -> list:
        rows = self.conn.execute(
            "SELECT * FROM economy WHERE server_id = ? ORDER BY money DESC",
            (
                server_id
                ,)
        ).fetchall()
        return rows
