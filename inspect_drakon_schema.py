import sqlite3

def inspect_drakon_schema(db_path="microgpt.drn"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("=== Список таблиц в файле .drn ===")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    for table in tables:
        print(f"Таблица: {table}")
        
    print("\n=== Структура ключевых таблиц ===")
    for table in ['diagrams', 'elements', 'vertices', 'links']:
        if table in tables:
            print(f"\nСхема таблицы '{table}':")
            cursor.execute(f"PRAGMA table_info({table});")
            for col in cursor.fetchall():
                print(f"  Поле: {col[1]} ({col[2]})")
                
    # Посмотрим примеры типов икон, которые получились при ручном переносе
    if 'elements' in tables:
        print("\n=== Примеры записанных икон (первых 5) ===")
        try:
            cursor.execute("SELECT id, type, text FROM elements LIMIT 5;")
            for row in cursor.fetchall():
                print(f"  ID: {row[0]} | Тип: {row[1]} | Текст: {row[2][:50]}...")
        except sqlite3.OperationalError:
            # Если имена полей немного отличаются в этой версии DRAKONEditor
            cursor.execute("SELECT * FROM elements LIMIT 1;")
            print("  Фактическая строка:", cursor.fetchone())
            
    conn.close()

if __name__ == "__main__":
    inspect_drakon_schema()
  
