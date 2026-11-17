# Mon carnet de français

Aplicación web estática para practicar vocabulario de francés con ilustraciones,
pronunciación IPA y audio. El contenido de aprendizaje se presenta en francés.

## Desarrollo local

No necesita dependencias de frontend. Abre `index.html` directamente o inicia
un servidor estático:

```bash
python3 -m http.server 8000
```

Después abre `http://localhost:8000`.

## Validación

```bash
python3 tests/validate_static_site.py
```

La validación comprueba que no haya estilos ni JavaScript embebidos, que los
recursos referenciados existan y que el inventario de audios e ilustraciones
esté completo.

## Estructura

```text
assets/
├── css/             Estilos de la aplicación
├── js/              Comportamiento del reproductor de audio
├── images/          Ilustraciones semirrealistas
└── media/audio/     Pronunciaciones francesas

dist/                PDF preparado para lectura e impresión
scripts/             Herramientas de generación
tests/               Validaciones automatizadas
index.html           Punto de entrada estático
```

## PDF

El PDF imprimible está disponible en `dist/carnet-francais.pdf`.
Para regenerarlo:

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/generate_pdf.py
```

## Voz

Los audios usan la voz francesa masculina `fr-FR-HenriNeural`.
