# Konveer
mkfifo drakon_pipe

# Schema pipe
# [Input SCR/Metatext] -> [Python-konverter to Drakon/SQLite3] -> [Refal-5 Meta optimizer] -> [Output microgpt.py]
cat input_window.scr | python3 drakon_converter.py | refal5 meta_optimizer.r5 > microgpt.py
