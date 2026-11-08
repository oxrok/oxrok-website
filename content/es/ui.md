---
title: La interfaz
---

**oxrok-ui es la interfaz de captura, visualización, medición y decodificación de oxrok**, escrita en Rust sobre [egui](https://egui.rs). Habla con los mismos dispositivos y decodificadores que la línea de comandos, y funciona con los dispositivos simulados integrados, así que puedes probarla sin hardware.

<div class="term">
  <button class="copy" type="button">copiar</button>
  <pre><span class="prompt">$</span> <span class="cmd">cargo install oxrok-ui --version {{% uiversion %}} --locked</span>
<span class="prompt">$</span> <span class="cmd">cargo install --features mock oxrok-ui --version {{% uiversion %}} --locked</span>  # sin hardware: los dispositivos simulados integrados</pre>
</div>

## La vista de captura

Con zoom a una ventana de 2 ms: una trama UART, transferencias SPI y flancos de reloj, con los protocolos decodificados en la tabla de datos.

<img src="/ui/capture.png" alt="La vista de captura, con zoom a una ventana de 2 ms" width="100%" style="height:auto">

Lo mismo en el tema claro (Ver → Tema):

<img src="/ui/capture-light.png" alt="La vista de captura en el tema claro" width="100%" style="height:auto">

## Filas, el menú de filas y la herramienta de zoom

Las filas se pueden renombrar en línea (CLK, UART TX, SPI CS, …); el menú contextual de fila muestra y oculta canales. La herramienta de zoom añade modos de zoom por rango y *Zoom relativo a*.

<img src="/ui/row-menu.png" alt="El menú contextual de fila, con filas renombradas en línea" width="100%" style="height:auto">

<img src="/ui/zoom-tool.png" alt="La herramienta de zoom: modos de zoom por rango y Zoom relativo a" width="100%" style="height:auto">

## Decodificar protocolos

Los analizadores de protocolo dibujan burbujas sobre sus canales y una tabla de datos con búsqueda.

<img src="/ui/analyzers.png" alt="Analizadores de protocolo: burbujas sobre sus canales y la tabla de datos con búsqueda" width="100%" style="height:auto">

## Marcadores y mediciones

Un par de marcadores, una medición de rango con su ventana de métricas y el panel de marcadores de tiempo.

<img src="/ui/markers.png" alt="Un par de marcadores, una medición de rango con su ventana de métricas y el panel de marcadores de tiempo" width="100%" style="height:auto">

## La pantalla de inicio

<img src="/ui/start-screen.png" alt="La pantalla de inicio" width="100%" style="height:auto">

## Cómo usarla

- **Abrir un dispositivo** — la pantalla de inicio, o el menú *Dispositivos* → *Nueva sesión*
- **Grabar** — `Space`; el modo *Temporizado* se detiene solo
- **Zoom / desplazar** — rueda, arrastrar, `=`/`-`, la herramienta de zoom
- **Marcadores y mediciones** — `M`, `Shift+M`, `R`
- **Decodificar un protocolo** — el hexágono de la barra de herramientas o el panel de analizadores
- **Guardar / abrir** — `Ctrl/Cmd+S` / `Ctrl/Cmd+O` (`.oxrok`)
- **Todos los atajos** — `?` (con búsqueda); cualquier comando — `Ctrl/Cmd+K`

Las capturas se regeneran en cada versión y provienen del [repositorio de oxrok-ui](https://github.com/oxrok/ui), alineado con oxrok.
