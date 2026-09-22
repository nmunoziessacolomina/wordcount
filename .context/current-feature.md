# Wordcount CLI

## Objetivos
- Construir una aplicación de línea de comandos llamada `wordcount` que imite el comportamiento básico de `wc`.
- Utilizar la biblioteca Typer para definir la CLI.
- Implementar opciones para contar líneas (`-l` o `--lines`), palabras (`-w` o `--words`) y caracteres (`-c` o `--chars`).
- Cuando no se especifique ninguna opción, mostrar líneas, palabras y caracteres (como `wc` por defecto).
- Aceptar entrada desde archivos especificados o desde stdin si no se proporciona archivo.
- Garantizar que el código siga las convenciones del proyecto (identificadores en inglés, simplicidad, etc.).

## Notas
- La aplicación será desarrollada en Python.
- Se debe incluir un archivo `pyproject.toml` o `setup.py` para gestionar dependencias.
- Se recomienda añadir pruebas unitarias para verificar los contadores.
- El historial de cambios se mantendrá en este documento según las restricciones.

## Histórico
- 2026-09-22: Implementación inicial de wordcount con Typer, pruebas unitarias y análisis de cobertura vs wc.
