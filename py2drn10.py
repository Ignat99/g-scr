import sqlite3
import os

class DrakonBuranDirectDiffConverter:
    def __init__(self, drn_path="rmsnorm.drn"):
        self.drn_path = drn_path
        if os.path.exists(self.drn_path):
            os.remove(self.drn_path)
            
        self.conn = sqlite3.connect(self.drn_path)
        self.cursor = self.conn.cursor()
        self._build_schema()

    def _build_schema(self):
        # Создаем оригинальную структуру таблиц drakon_qt
        self.cursor.execute("CREATE TABLE tree_nodes (node_id integer primary key, parent integer, type text, name text, diagram_id integer);")
        self.cursor.execute("CREATE TABLE state (row integer primary key, current_dia integer, description text);")
        self.cursor.execute("""
            CREATE TABLE items (
                item_id integer primary key,
                diagram_id integer,
                type text,
                text text,
                selected integer,
                x integer,
                y integer,
                w integer,
                h integer,
                a integer,
                b integer,
                aux_value integer,
                color text,
                format text,
                text2 text
            );
        """)
        self.cursor.execute("CREATE TABLE info (key text primary key, value text);")
        self.cursor.execute("INSERT INTO info VALUES ('type', 'drakon');")
        self.cursor.execute("INSERT INTO info VALUES ('version', '33');")
        self.cursor.execute("INSERT INTO info VALUES ('start_version', '1');")
        self.cursor.execute("INSERT INTO info VALUES ('language', 'Python 3.x');")

        self.cursor.execute("CREATE TABLE diagrams (diagram_id integer primary key, name text unique, origin text, description text, zoom double);")
        self.cursor.execute("CREATE TABLE diagram_info (diagram_id integer, name text, value text, primary key (diagram_id, name));")
        self.conn.commit()

    def inject_diff_queries(self, queries):
        for q in queries:
            # Заменяем имена таблиц в обратных кавычках на обычные для совместимости со стандартным SQLite
            clean_q = q.replace("`tree_nodes`", "tree_nodes")\
                       .replace("`state`", "state")\
                       .replace("`items`", "items")\
                       .replace("`diagrams`", "diagrams")\
                       .replace("`diagram_info`", "diagram_info")
            try:
                self.cursor.execute(clean_q)
            except Exception as e:
                # Если инсерт в state имеет пустую строку вместо диаграммы '', заменим на NULL или 0
                if "VALUES (1,''," in clean_q:
                    alt_q = clean_q.replace("VALUES (1,'',", "VALUES (1,NULL,")
                    self.cursor.execute(alt_q)
                else:
                    print(f"Ошибка выполнения: {e} в запросе: {clean_q[:100]}")
        
        # Добавим дефолтные метаданные ориентации для новых диаграмм, чтобы DRAKON Editor открывал их без сбоев
        for dia_id in [7, 8, 9, 10, 11, 12]:
            try:
                self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'papersize', 'a4');", (dia_id,))
                self.cursor.execute("INSERT INTO diagram_info VALUES (?, 'orientation', 'portrait');", (dia_id,))
            except sqlite3.IntegrityError:
                pass

        self.conn.commit()
        self.conn.close()
        print("[Успех] SQLite база данных rmsnorm.drn полностью собрана на основе оригинального sql.diff.")

if __name__ == "__main__":
    # Вытягиваем сырые вставки из sql.diff
    with open("sql.diff", "r", encoding="utf-8") as f:
        lines = f.readlines()

    insert_queries = []
    current_query = []

    for line in lines:
        if line.startswith("> "):
            content = line[2:]
            if "INSERT INTO" in content and current_query:
                insert_queries.append("".join(current_query).strip())
                current_query = [content]
            else:
                current_query.append(content)
    if current_query:
        insert_queries.append("".join(current_query).strip())

    valid_inserts = [q for q in insert_queries if q.startswith("INSERT INTO")]
    
    converter = DrakonBuranDirectDiffConverter("rmsnorm.drn")
    converter.inject_diff_queries(valid_inserts)
