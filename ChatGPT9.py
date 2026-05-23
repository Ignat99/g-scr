import os
import sqlite3
import ast


class DrakonBuranSilhouetteConverterV10:
    def __init__(self, drn_path="rmsnorm.drn"):
        self.drn_path = drn_path
        if os.path.exists(self.drn_path):
            os.remove(self.drn_path)

        self.conn = sqlite3.connect(self.drn_path)
        self.cursor = self.conn.cursor()
        self._build_exact_schema()

        self._diagram_id = 1
        self._item_id = 1

    # === БАЗОВАЯ СХЕМА (оставьте свою если уже есть) ===
    def _build_exact_schema(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS diagrams (id INTEGER, name TEXT, pos TEXT, parent TEXT, scale REAL);"
        )
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS items (id INTEGER, dia_id INTEGER, name TEXT, code TEXT);"
        )

    # === ID ГЕНЕРАЦИЯ ===
    def _next_diagram_id(self):
        val = self._diagram_id
        self._diagram_id += 1
        return val

    def _get_next_item_id(self):
        val = self._item_id
        self._item_id += 1
        return val

    # === СБОР FOR ===
    def _collect_top_level_fors(self, node):
        result = []
        for n in ast.walk(node):
            if isinstance(n, ast.For):
                is_nested = False
                for parent in ast.walk(n):
                    if parent is not n and isinstance(parent, ast.For):
                        is_nested = True
                        break
                if not is_nested:
                    result.append(n)
        return result

    # === ГРУППИРОВКА ПО 3 ===
    def _split_for_groups(self, for_nodes):
        return [for_nodes[i:i+3] for i in range(0, len(for_nodes), 3)]

    # === ОСНОВНОЙ ПАРСЕР ===
    def _process_for_blocks(self, root):
        for_nodes = self._collect_top_level_fors(root)
        if not for_nodes:
            return

        groups = self._split_for_groups(for_nodes)
        silhouette_ids = []

        for idx, group in enumerate(groups):
            dia_id = self._next_diagram_id()
            self._create_for_silhouette(dia_id, group, idx)
            silhouette_ids.append(dia_id)

        self._create_master_for_sequence(silhouette_ids)

    # === СИЛУЭТ ===
    def _create_for_silhouette(self, dia_id, for_group, idx):
        self.cursor.execute(
            "INSERT INTO diagrams VALUES (?, ?, '0 250', NULL, 100.0);",
            (dia_id, f"for_silhouette_{idx}")
        )

        for i, for_node in enumerate(for_group):
            item_id = self._get_next_item_id()
            code = ast.unparse(for_node)

            self.cursor.execute(
                "INSERT INTO items VALUES (?, ?, ?, ?);",
                (item_id, dia_id, f"FOR_{idx}_{i}", code)
            )

    # === MASTER ===
    def _create_master_for_sequence(self, silhouette_ids):
        if not silhouette_ids:
            return

        dia_id = self._next_diagram_id()
        self.cursor.execute(
            "INSERT INTO diagrams VALUES (?, ?, '0 250', NULL, 100.0);",
            (dia_id, "for_master_sequence")
        )

        for sid in silhouette_ids:
            item_id = self._get_next_item_id()
            self.cursor.execute(
                "INSERT INTO items VALUES (?, ?, ?, ?);",
                (item_id, dia_id, f"CALL_{sid}", f"CALL {sid}")
            )


# === ВЫЗОВ (ОДНА СТРОКА В КОНЦЕ ФАЙЛА) ===
DrakonBuranSilhouetteConverterV10()._process_for_blocks(ast.parse(open("input.py", encoding="utf-8").read()))