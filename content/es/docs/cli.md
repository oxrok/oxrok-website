---
title: La línea de comandos de oxrok
type: docs
---

`oxrok` acepta las opciones de sigrok-cli para los flujos comunes e imprime la misma salida, byte a byte después de la primera línea de encabezado (que nombra la herramienta).

## Opciones

```
-V, --version                 Show version and support list
-L, --list-supported         List supported devices/modules/decoders
-l, --loglevel <LEVEL>       Set loglevel (0-5, default 2)
    --strict                 Treat warnings as errors: stop and exit with failure
-d, --driver <DRIVER>        The driver to use, with scan options: driver[:key=value]...
-c, --config <CONFIG>        Device option: [channel_group=GROUP:]key=value[:key=value]...
-i, --input-file <FILE>      Load input from file (- for stdin)
-I, --input-format <FORMAT>  Input format: module[:option=value]...
-o, --output-file <FILE>     Save output to file
-O, --output-format <FORMAT> Output format: module[:option=value]...
-C, --channels <CHANNELS>    Channels to use: names or ranges, comma separated, name=newname to rename
-g, --channel-group <GROUP>  Channel group to show or configure
-t, --triggers <TRIGGERS>    Trigger: channel=matches[,channel=matches]... with ; between stages
-w, --wait-trigger           Wait for trigger before saving data
    --scan                   Scan for devices
    --show                   Show device details
    --time <TIME>            How long to sample (ms, or with a unit: 2s, 500ms)
    --samples <SAMPLES>      Number of samples to acquire (with size suffix: 1k, 2m)
    --frames <FRAMES>        Number of frames to acquire
    --continuous             Sample continuously until stopped
-P, --protocol-decoders <DECODERS>            Protocol decoders to run
-A, --protocol-decoder-annotations <ANN>      Annotations to show
-B, --protocol-decoder-binary <BIN>           Binary output to show
-M, --protocol-decoder-meta <META>            Decoder metadata to show
    --protocol-decoder-samplenum             Show sample numbers with annotations
    --protocol-decoder-ann-class            Show the annotation class with annotations
    --get <KEY>                Get device option only: [channel_group=GROUP:]key
    --set                      Set device options only
```

## Salidas

`bits`, `hex`, `ascii`, `analog`, `csv`, `vcd`, `binary`, `srzip` y `null`. Entradas: `.sr`, VCD y binario.

## Disparos

`-t` acepta etapas separadas por `;`, p. ej. `-t 'D0=r;D1=1'`. Una etapa se escribe como en sigrok-cli. Encima de eso, donde el dispositivo lo soporta (el parser rechaza lo que no):

- `D0=r*5` se dispara en el quinto flanco de subida, `D0=r*5c` en el quinto consecutivo.
- `D0=1>100` se dispara cuando D0 lleva en alto más de 100 muestras, `D0=1>50us` con un tiempo, convertido con la tasa de muestreo.
- `D0-D2=3..5` se dispara mientras el valor en D2 D1 D0 esté entre 3..5, `D0-D2=!7` mientras no sea 7. Decimal o hex `0x`.
- `D0=r|D1=r` se dispara en cualquiera de las etapas, `D0=r&D1=r` cuando ambas se han disparado en cualquier orden. Exactamente dos etapas.

`>`, `;`, `|` y `&` necesitan comillas en una shell.

## Estado de salida

0 cuando la ejecución hizo lo que se pidió; 1 en caso contrario, con el motivo en stderr. Una captura que comenzó ha fallado cuando terminó por cualquier razón distinta a alcanzar un límite, una parada solicitada (Ctrl-C, el botón de cancelación del propio dispositivo) o el fin natural de los datos del dispositivo. Así que fallan: un dispositivo que se va, un error de lectura o escritura, un límite de sondeo o reintentos que se rinde, un límite de silencio que termina una captura cuyo límite no se alcanzó, un flujo sin límite que se agota, y una salida que ya no se puede escribir (disco lleno).

Una captura fallida lo dice en una línea, la última que escribe:

```
capture failed: device disconnected
```

con el error propio del driver tras los dos puntos. Lo anterior al fallo se escribe y se vacía; la salida se cierra. Una parada gana sobre un fallo que viene después: esa ejecución sale con 0.

## Aún no disponible

- `--protocol-decoder-jsontrace`. Los decodificadores Python necesitan la característica de compilación `python`; ver [Decodificadores de protocolo](/docs/decoders/).
- `-T` (módulos de transformación), `--list-supported-wiki`, las opciones `gnuplot` y `scale` de la salida `csv`.
- La entrada `csv` y los demás módulos de entrada de la cola larga.
- Los demás drivers de hardware de libsigrok: el resto de los instrumentos serie vienen a continuación, y el resto después.
