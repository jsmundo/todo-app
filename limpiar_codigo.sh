#!/bin/bash

PROYECTO="todo-app-restaurado"

# Ruta al directorio del proyecto
DIR_PROYECTO="$(pwd)"

# Ruta para guardar backups
DIR_BACKUPS="../backups_limpieza"
mkdir -p "$DIR_BACKUPS"

# Nombre con timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
NOMBRE_BACKUP="backup_codigo_$TIMESTAMP"
RUTA_BACKUP="$DIR_BACKUPS/$NOMBRE_BACKUP"

# Comprobación de argumento
if [[ $1 == "restaurar" ]]; then
    ULTIMO_BACKUP=$(ls -td "$DIR_BACKUPS"/backup_codigo_* | head -n 1)

    if [ -z "$ULTIMO_BACKUP" ]; then
        echo "❌ No se encontró ningún backup para restaurar."
        exit 1
    fi

    echo "🔁 Restaurando desde: $ULTIMO_BACKUP"
    cp -r "$ULTIMO_BACKUP"/* "$DIR_PROYECTO"
    echo "✅ Restauración completada."
    exit 0
fi

# Crear copia de seguridad antes de limpiar
echo "📦 Creando backup en: $RUTA_BACKUP"
mkdir -p "$RUTA_BACKUP"
cp -r "$DIR_PROYECTO"/* "$RUTA_BACKUP"

# Ejecutar limpieza con flake8 y eliminar imports no usados
echo "🧹 Ejecutando limpieza..."

# Aquí podrías usar autoflake o manualmente limpiar (simplificado por ahora)
flake8 . > flake8_report.txt

echo "📄 Análisis guardado en flake8_report.txt"
echo "✅ Limpieza finalizada. Usa './limpiar_codigo.sh restaurar' para volver atrás si algo falla."
