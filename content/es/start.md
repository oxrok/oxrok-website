---
title: Empezar
---

Cinco pasos, todos con el driver `demo` integrado, sin necesidad de hardware. Instala oxrok primero, o consulta la página completa de [instalación]({{< relref "install" >}}):

{{< install >}}

## 1. Lista los drivers

<div class="term">
  <button class="copy" type="button">copiar</button>
  <pre><span class="prompt">$</span> <span class="cmd">oxrok -L</span>
Supported hardware drivers:
  agilent-dmm          Agilent U12xx series DMMs
  appa-55ii            APPA 55II
  arachnid-labs-re-load-pro Arachnid Labs Re:load Pro
  ...</pre>
</div>

164 ids de driver, la mayoría multímetros.

## 2. Escanea y muestra

<div class="term">
  <button class="copy" type="button">copiar</button>
  <pre><span class="prompt">$</span> <span class="cmd">oxrok -d demo --show</span>
Driver functions:
    Demo device
    Logic analyzer
    Oscilloscope
Scan options:
    logic_channels
    analog_channels
    limit_frames
demo - Demo device with 13 channels: D0 D1 D2 D3 D4 D5 D6 D7 A0 A1 A2 A3 A4
Channel groups:
    Logic: channels D0 D1 D2 D3 D4 D5 D6 D7
    Analog: channels A0 A1 A2 A3 A4</pre>
</div>

## 3. Captura

`--samples`, `--time` y `--frames` limitan la ejecución; `-C` selecciona canales; `-O` elige el formato de salida.

<div class="term">
  <button class="copy" type="button">copiar</button>
  <pre><span class="prompt">$</span> <span class="cmd">oxrok -d demo --samples 4 -O bits</span>
oxrok 0.3.0-alpha.1
Acquisition with 8/13 channels at 200 kHz
A0: -10.0000 V DC
A0: -10.0000 V DC
...</pre>
</div>

El canal analógico aleatorio del demo difiere en cada ejecución en ambas herramientas.

## 4. Disparo

`-t` arma un disparo y `-w` espera a que ocurra antes de guardar datos. La coincidencia se escribe `canal=valor`, así que `D0=r` se dispara en un flanco de subida de D0:

<div class="term">
  <button class="copy" type="button">copiar</button>
  <pre><span class="prompt">$</span> <span class="cmd">oxrok -d demo -t 'D0=r' -w --samples 4 -O bits</span></pre>
</div>

Dos formas que confunden: `D0:r` es una opción de escaneo, no una coincidencia de disparo, y una captura sin límite solo imprime la ayuda.

## 5. Decodifica

`-P` ejecuta un decodificador de protocolo y `-A` selecciona las clases de anotación a mostrar.

<div class="term">
  <button class="copy" type="button">copiar</button>
  <pre><span class="prompt">$</span> <span class="cmd">oxrok -i tests/fixtures/uart-hi.vcd -P uart:baudrate=115200:rx=top.D0 -A uart=rx-data</span>
uart-1: 48
uart-1: 69
uart-1: 21
uart-1: 0A
uart-1: 00
uart-1: FF</pre>
</div>

Eso es `Hi!` en hexadecimal.

## Dispositivos reales

`conn=` nombra el puerto o dispositivo; en Linux un dispositivo USB es solo de root sin una regla de udev. Un multímetro serie:

<div class="term">
  <button class="copy" type="button">copiar</button>
  <pre><span class="prompt">$</span> <span class="cmd">oxrok -d uni-t-ut61e-ser:conn=/dev/ttyUSB0 --samples 10</span></pre>
</div>

Un osciloscopio SCPI:

<div class="term">
  <button class="copy" type="button">copiar</button>
  <pre><span class="prompt">$</span> <span class="cmd">oxrok -d rigol-ds:conn=tcp://192.168.1.50 --samples 1000 -O csv</span></pre>
</div>

## Vienes de sigrok-cli

La línea de comandos acepta las opciones de sigrok-cli para los flujos comunes e imprime la misma salida, byte a byte después de la primera línea de encabezado. Las diferencias que confunden:

- Una captura que falla sale con código 1 y dice por qué en stderr; sigrok-cli sale con 0 en la mayoría.
- Los valores se analizan de forma más estricta: un tamaño con fracción conserva su sufijo (`samplerate=12.5M` es 12.5 MHz), y una fracción sola se rechaza.
- La línea de encabezado dice `oxrok <version>` en lugar de `libsigrok <version>`.
- Los disparos aceptan las formas extendidas (`D0=r*5`, `D0=1>50us`, `D0-D2=3..5`, `D0=r|D1=r`); sigrok-cli las rechaza.
- `--strict` convierte cada advertencia en una ejecución fallida.

La referencia completa está en la [guía de CLI]({{< relref "docs/cli" >}}).
