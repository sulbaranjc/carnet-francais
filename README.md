# Mon carnet de français

Aplicación web estática para practicar vocabulario de francés con ilustraciones,
pronunciación IPA y audio. El contenido de aprendizaje se presenta en francés.

## Desarrollo local

No necesita dependencias de frontend. Inicia un servidor estático:

```bash
python3 -m http.server 8000
```

Después abre `http://localhost:8000`.

## Datos y búsqueda

El catálogo vive físicamente en `assets/data/vocabulary.json`. Cada entrada
contiene todos los datos de un card: identificador, orden, palabra, artículo,
IPA, frase, regla, nombre/ruta/alternativa de la ilustración y nombre/ruta de
los audios de palabra y frase. `assets/js/app.js` obtiene ese JSON con `fetch`,
construye los cards en el DOM y filtra en cada pulsación las palabras que
comienzan por la consulta.

## Validación

```bash
npm test
```

La suite verifica el filtrado por prefijo, la estructura y rutas del catálogo
JSON y que los recursos de la aplicación existan.

## Estructura

```text
assets/
├── css/             Estilos de la aplicación
├── data/            Catálogo JSON de palabras, audios e ilustraciones
├── images/          Ilustraciones semirrealistas
├── js/              Renderizado dinámico, búsqueda y reproductor
└── media/audio/     Pronunciaciones francesas

dist/                PDF preparado para lectura e impresión
scripts/             Herramientas de generación
tests/               Validaciones automatizadas
index.html           Punto de entrada estático
```

## PDF e ilustraciones

El PDF imprimible está disponible en `dist/carnet-francais.pdf`. Las
ilustraciones de familia se generan desde las mismas funciones vectoriales que
el PDF, para que ambos formatos mantengan el mismo encuadre.

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/render_illustrations.py
.venv/bin/python scripts/generate_audio.py
.venv/bin/python scripts/generate_pdf.py
```

## Voz

Los audios usan la voz francesa masculina `fr-FR-HenriNeural`.
