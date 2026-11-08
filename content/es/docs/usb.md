---
title: USB y emulación
type: docs
---

Los drivers hablan con los dispositivos a través de un pequeño trait `Transport` — transferencias de control y bulk con tiempos de espera, ocupación de interfaces y reseteos — y nunca ven qué backend se usa. Serial, TCP, HID y SCPI son transportes separados con la misma forma.

| característica | backend | plataformas |
|---|---|---|
| `nusb` (por defecto) | Rust puro, sin biblioteca de sistema | Linux, macOS, Windows, Android |
| `libusb` | rusb, compilado desde el código fuente | lo anterior, más BSD, Solaris, Haiku |

Con ambos compilados, `OXROK_USB_BACKEND=libusb` o `=nusb` elige uno en tiempo de ejecución; nusb es el predeterminado.

## Conectar

`conn=` nombra el puerto o dispositivo: un `/dev/ttyUSB0`, una dirección `tcp://`, o un USB `bus.address`. En Linux un dispositivo USB es solo de root sin una regla de udev — una regla con `MODE="0666"` para el `VID:PID` del dispositivo funciona. macOS y Windows no necesitan nada más allá de las notas en el [documento USB del repositorio](https://github.com/oxrok/oxrok/blob/main/docs/USB.md#troubleshooting).

## Un driver que se comporta mal: grabar y reproducir

La mayoría de los problemas de drivers solo aparecen en un dispositivo, y quien podría arreglarlos no lo tiene. La respuesta de oxrok es una grabación:

```sh
OXROK_USB_RECORD=capture.txt oxrok -d intronix-logicport --samples 64
```

Cada transferencia USB — control y bulk, peticiones y respuestas — cae en un pequeño archivo de texto, legible y editable a mano:

```text
# oxrok usb fixture 1
device vid=0403 pid=dc48 product="LogicPort Logic Analyzer"
claim 0 -> ok
ctl_out 40 09 0004 0000 - -> ok
ctl_in 40 0a 0000 0000 1 -> 04
bulk_in 81 4096 -> 3160aabb
```

Envía ese archivo con un [informe de hardware](https://github.com/oxrok/oxrok/issues/new?template=hardware-report.yml), y el problema se reproduce en cualquier máquina, sin dispositivo:

```sh
OXROK_USB_REPLAY=capture.txt oxrok -d intronix-logicport --samples 64
```

Una reproducción falla en la primera transferencia que difiere de la grabación, lo que localiza dónde cambió el comportamiento de un driver. Las pruebas se construyen igual: cada driver incluye al menos una sesión grabada, y CI las reproduce sin hardware. `OXROK_HID_RECORD` y `OXROK_HID_REPLAY` hacen lo mismo para dispositivos HID.

## Emulación por USB/IP

Una grabación reproduce lo que pasó; un dispositivo emulado puede hacer cualquier cosa. `oxrok-emu` conecta un modelo de dispositivo en Rust mediante `vhci-hcd` de Linux, para que el kernel vea un dispositivo USB real, y sigrok-cli y oxrok se ejecutan sin modificaciones contra el mismo modelo. Esa es la base de toda la historia de [pruebas]({{< relref "testing" >}}):

{{< emulator >}}

Los modelos y el arnés están en el [repositorio](https://github.com/oxrok/oxrok/tree/main/emu), construidos sobre la crate [vusb](https://github.com/oxrok/vusb).

La referencia completa — el formato de grabación, los flujos, escribir un modelo de dispositivo, la resolución de problemas por sistema operativo — queda en el [`docs/USB.md` del repositorio](https://github.com/oxrok/oxrok/blob/main/docs/USB.md).
