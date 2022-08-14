import sqlite3
import platform
def test():
    print(platform.system())
    conn = sqlite3.connect('./resources/acting_method.db')
    cursor = conn.execute("select ID FROM guilds")
    print([c for c in cursor])