# Wordcount CLI - Mejora de compatibilidad con wc (90%)

## Objetivos
- Mejorar la compatibilidad de `wordcount` con el comportamiento original de `wc` implementando funcionalidades faltantes.
- Añadir conteo de bytes correctos mediante `-c`/`--bytes`.
- Añadir conteo de caracteres mediante `-m`/`--chars`.
- Ajustar el comportamiento por defecto (sin opciones) para mostrar líneas, palabras y bytes.
- Añadir información de versión con `--version`.
- Mantener las funcionalidades existentes (líneas, palabras, entrada desde archivos y stdin, múltiples archivos, ayuda).
- Garantizar que el código siga las convenciones del proyecto (identificadores en inglés, simplicidad, etc.).

## Notas
- La aplicación será desarrollada en Python.
- El archivo `pyproject.toml` ya existe y gestiona dependencias.
- Se añadirán pruebas unitarias para verificar los nuevos contadores y el comportamiento.
- El historial de cambios se mantendrá en este documento según las restricciones.
- Se considerará la codificación UTF-8 para el cálculo de bytes.

## Histórico
- 2026-09-22: Implementación de mejoras para alcanzar 90% de cobertura con wc: conteo de bytes mediante -c, conteo de caracteres mediante -m, comportamiento por defecto (líneas, palabras, bytes) y flag --version.
- 2026-09-22: Implementación inicial de wordcount con Typer, pruebas unitarias y análisis de cobertura vs wc.
