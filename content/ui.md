---
title: The UI
---

**oxrok-ui is the capture, display, measurement and decoding UI for oxrok**,
written in Rust on [egui](https://egui.rs). It talks to the same devices and
decoders as the command line, and it runs on the built-in mock devices, so you
can try it without hardware.

<div class="term">
  <button class="copy" type="button">copy</button>
  <pre><span class="prompt">$</span> <span class="cmd">cargo install oxrok-ui --version {{% uiversion %}} --locked</span>
<span class="prompt">$</span> <span class="cmd">cargo install --features mock oxrok-ui --version {{% uiversion %}} --locked</span>  # no hardware: the built-in mock devices</pre>
</div>

## The capture view

Zoomed to a 2 ms window: a UART frame, SPI transfers and clock edges, with the
decoded protocols in the data table.

<img src="/ui/capture.png" alt="The capture view, zoomed to a 2 ms window" width="100%" style="height:auto">

The same in the light theme (View → Theme):

<img src="/ui/capture-light.png" alt="The capture view in the light theme" width="100%" style="height:auto">

## Rows, the row menu and the zoom tool

Rows can be renamed inline (CLK, UART TX, SPI CS, …); the row context menu shows
and hides channels. The zoom tool adds range-zoom modes and *Zoom relative to*.

<img src="/ui/row-menu.png" alt="The row context menu, with inline-renamed rows" width="100%" style="height:auto">

<img src="/ui/zoom-tool.png" alt="The zoom tool: range zoom modes and Zoom relative to" width="100%" style="height:auto">

## Decoding protocols

Protocol analyzers draw bubbles above their channels and a searchable data table.

<img src="/ui/analyzers.png" alt="Protocol analyzers: bubbles above their channels and the searchable data table" width="100%" style="height:auto">

## Markers and measurements

A marker pair, a range measurement with its metrics popup, and the Timing Markers
panel.

<img src="/ui/markers.png" alt="A marker pair, a range measurement with its metrics popup, and the Timing Markers panel" width="100%" style="height:auto">

## The start screen

<img src="/ui/start-screen.png" alt="The start screen" width="100%" style="height:auto">

## Using it

- **Open a device** — the start screen, or the *Devices* menu → *New Session*
- **Record** — `Space`; *Timed* mode stops by itself
- **Zoom / pan** — wheel, drag, `=`/`-`, the zoom tool
- **Markers and measurements** — `M`, `Shift+M`, `R`
- **Decode a protocol** — the toolbar hexagon or the Analyzers panel
- **Save / open** — `Ctrl/Cmd+S` / `Ctrl/Cmd+O` (`.oxrok`)
- **All shortcuts** — `?` (with search); any command — `Ctrl/Cmd+K`

The screenshots are regenerated on every release and come from the
[oxrok-ui repository](https://github.com/oxrok/ui), aligned with oxrok.
