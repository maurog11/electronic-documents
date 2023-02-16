# API Electronic Documents

API Rest - Python Framework Flask - DB MySQL

## Requerimientos
Para ejecutar el proyecto, se requiere tener instalados:
- Python versiones 3 (superiores a la 3.6)
- virtualenv
- Gestor de Base de Batos (MySQL)

## Instalación proyecto local
Para la instalación de recursos, se debe tener en cuenta los siguientes pasos:

### Creación del Entorno
Para la creación del entorno virtual se deben ejecutar los siguientes comandos
en la raíz del proyecto:
```
python -m venv venv
```

### Instalar Requerimientos
```
source ./venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Instalación proyecto Docker
```
make compile-local
```
### ejecutar el proyecto docker
```
make run-local
```

### Creación de la Base de Datos
Para que la migración funcione, deben crear una base de datos llamada ```electronic_doc_db```

> **Nota:** dentro de la carpeta ```api``` crear un archivo llamado ```.env``` este archivo
> debe tener la configuración para conectarse a la base de datos.

## Ejecutar Migración

Para generar el archivo de migración con los cambios realizados en los modelos

```flask db migrate -m "agregar descripción aquí"```

Para ejecutar los archivos de migración
```
flask db upgrade
```
Para eliminar las tablas
```
flask db downgrade
```

### Ejecutar API
Los comandos a continuación permitirán la ejecución de la API
```
cd api
python run.py
```

# Documentación de API

## Requisitos

Se debe tener instalado:

- apidoc

!Nota: En caso de no tener creada la carpeta doc, se debe crear

## Compilar y Generar la Documentación

Para generar la documentación del api

```
apidoc -i src/doc/api -o src/doc/apidoc/ -f ".*\\.py$" --debug
```

## Ejecutar la Documentación

Para visualizar la documentación se debe ingresar a la carpeta src/doc/apidoc,
luego abrir el archivo index.html en cualquier navegador

