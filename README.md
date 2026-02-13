# File Upload + Script Processor (Vercel)

App en Flask para subir un archivo XML, procesarlo con un script Python y descargarlo modificado.

## Archivos clave

- `app.py`: interfaz web + endpoint de carga/descarga.
- `excel_script.py`: logica de transformacion del Excel (aqui personalizas tu script).
- `templates/index.html`: formulario de carga.
- `vercel.json`: configuracion para deploy en Vercel.

## Ejecutar local

```bash
cd fix_dte
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Abrir: `http://localhost:5000`

## Deploy en Vercel

1. Sube este proyecto a un repo GitHub.
2. En Vercel: **Add New Project** -> importa el repo.
3. En **Root Directory** selecciona `fix_dte`.
4. En variables de entorno agrega:
   - `FLASK_SECRET_KEY`: una clave larga aleatoria.
5. Deploy.

Vercel usara `vercel.json` y montara la app Flask desde `app.py`.

## Personalizar transformacion

Edita la funcion `modificar_archivo` en `excel_script.py`.

Actualmente el ejemplo:
- En Excel: recorta espacios de celdas de texto y agrega columna `PROCESADO`.
- En XML: mantiene la primera linea y recorta al primer bloque `<DTE ... </DTE>`.
