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

El catálogo vive físicamente en `assets/data/vocabulary.json`. Las entradas enriquecidas
incluyen identificador, orden, palabra, artículo, IPA, frase, regla, ilustración y
audios. Las entradas recién importadas desde Duolingo conservan la palabra, expresión
y significado de referencia interno (`importGloss`), sin mostrar español en la interfaz;
se señalan como «à enrichir» hasta disponer de frase, ilustración y audio propios.
`assets/js/app.js` obtiene ese JSON con `fetch`, construye los cards en el DOM y filtra
en cada pulsación las palabras que comienzan por la consulta.

Para importar de nuevo la lista visible de Duolingo sin usar APIs internas ni cookies,
guarda el árbol CUA de `Practice Hub > Words` y ejecuta:

```bash
python3 scripts/import_duolingo_words.py duolingo-words-tree.txt assets/data/vocabulary.json
```

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

## Despliegue público con Docker

La imagen se sirve con Nginx y se integra con la red externa `nginx-proxy` de
VM104. No publica puertos propios: el proxy recibe el subdominio y enruta al
contenedor mediante `VIRTUAL_HOST` y `VIRTUAL_PORT`.

```bash
cp .env.example .env
# Edita APP_DOMAIN con el subdominio elegido.
docker compose up -d --build
```

Comprueba el contenedor con `docker compose ps` y la ruta con:

```bash
curl --resolve "$APP_DOMAIN:80:127.0.0.1" "http://$APP_DOMAIN/health"
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
