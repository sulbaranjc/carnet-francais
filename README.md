# Mon carnet de français

Cuaderno visual para aprender francés con vocabulario, pronunciación IPA,
ilustraciones y audio.

## Abrir el cuaderno interactivo

Abre `index.html` en un navegador. Los botones verdes reproducen los audios
franceses ubicados en `assets/audio/`.

## Estructura

```text
assets/audio/   Pronunciaciones en francés
assets/images/  Ilustraciones del cuaderno
dist/           PDF preparado para lectura e impresión
scripts/        Generador del PDF
```

## Regenerar el PDF

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/generate_pdf.py
```

El contenido pedagógico del cuaderno está en francés.
