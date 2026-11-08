---
title: Pruebas
---

La mayoría de los drivers aquí nunca han visto su dispositivo. Esta página trata de la única forma de comprobarlos sin el hardware — y de dónde se detiene esa comprobación.

## El problema

libsigrok tiene 87 drivers, para hardware que ninguno de nosotros tiene. Portarlos solo desde el código fuente en C daría un código que compila y que nunca ha hablado con nada. Las grabaciones son el recurso habitual, pero también necesitan los dispositivos.

## La idea

Un modelo de dispositivo en Rust, conectado mediante `vhci-hcd` de Linux por USB/IP, para que el kernel vea un dispositivo USB real. El `sigrok-cli` real y `oxrok` se ejecutan sin modificaciones contra el mismo dispositivo, y cada transacción queda registrada. Luego se comparan.

{{< emulator >}}

## Qué se compara

La salida, los errores, el estado de salida, cada transferencia USB, además de gcov sobre el driver en C para ver qué se alcanzó. Bytes idénticos en el bus es una afirmación más fuerte que salida idéntica. No es incondicional: los números de nodo y las direcciones de dispositivo se generalizan, y un caso puede filtrar lo que difiere por una razón declarada.

## Los modelos son hostiles

Un modelo no acepta cualquier cosa que llegue. Marca transferencias a endpoints que la configuración no tiene, lo que su protocolo prohíbe, y se comporta mal a propósito: peticiones STALL, respuestas cortas o basura, una transferencia que nunca termina, una desconexión en una transferencia elegida. Los caminos de error son donde más difieren el C y el port.

## Lo que no puede decirte

Un modelo se construye a partir del driver en C y de las fuentes públicas que existan, así que puede compartir la incomprensión que el C tiene del dispositivo. Igualarlo demuestra paridad con libsigrok en los caminos que los casos alcanzan, no comportamiento correcto en hardware. El tiempo no es real: los modelos cuentan las transferencias del host en lugar del reloj, y USB/IP no tiene bus. Así que la evidencia real tiene prioridad: grabaciones, manuales, historia. Las peculiaridades en las que el C confía sin decirlo no se pueden encontrar así.

Números: **{{% numbers %}}**

[Cómo se prueban los drivers en el README](https://github.com/oxrok/oxrok/blob/main/README.md#how-drivers-are-tested)
y [las notas de emulación USB](https://github.com/oxrok/oxrok/blob/main/docs/USB.md).
