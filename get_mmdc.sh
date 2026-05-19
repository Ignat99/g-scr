#!/bib/bash

# Установка компилятора
npm install -g @mermaid-js/mermaid-cli

# Генерация PNG картинки из текстового файла
mmdc -i scheme.mmd -o scheme.png -w 1024 -H 768
