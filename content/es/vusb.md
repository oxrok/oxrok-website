---
title: vusb
---

<img src="/vusb/lockup.svg" alt="vusb" width="220" style="height:auto">

**vusb pone en el bus un dispositivo USB que es solo código Rust.** Prueba tu driver sin el hardware, en CI y con inyección de fallos.

<img src="/vusb/hero.svg" alt="Tu software habla por USB con un dispositivo que es solo código Rust, sin hardware." width="100%" style="height:auto">

En Linux el dispositivo es real para toda la máquina: `lsusb` lo lista, y libusb, hidraw, `/dev/ttyACM0` y `/dev/ttyUSB0` funcionan. En una prueba unitaria no necesita kernel ni root. De cualquier forma es el mismo código, y avisa cada vez que el host rompe el protocolo.

## Un modelo

Este puerto serie responde en mayúsculas. El shell CDC-ACM maneja la parte USB, así que el modelo solo ve bytes:

```rust
use vusb::shells::cdc::{Cdc, Faults, Identity, Port, Serial};

struct Shout;

impl Serial for Shout {
    fn received(&mut self, data: &[u8], port: &mut Port<'_>) {
        port.send(&data.to_ascii_uppercase());
    }
}

fn main() -> vusb::Result<()> {
    let id = Identity::new(0x1209, 0x0001, "Maker", "Shouter");
    let model = Cdc::new("shout", &id, Faults::default(), Shout);
    // hand it to a session, or run it in-process on a Bus with no kernel
    Ok(())
}
```

## Las capas

Un programa, un host en un cable o una prueba llegan a tu modelo de dispositivo a través de las mismas capas de bus y dispositivo; `vusb-ctl` lo controla mientras se ejecuta.

<img src="/vusb/overview.svg" alt="Un programa, un host en un cable o una prueba llegan a tu modelo de dispositivo a través de las mismas capas de bus y dispositivo. vusb-ctl lo controla mientras se ejecuta." width="100%" style="height:auto">

## Cómo funciona una transferencia

Una transferencia que el modelo responde con NAK es retenida por el bus y ofrecida de nuevo hasta que el modelo tenga datos. Solo entonces el host ve una finalización.

<img src="/vusb/transfer.svg" alt="Una transferencia que el modelo responde con NAK es retenida por el bus y ofrecida de nuevo hasta que el modelo tenga datos. Solo entonces el host ve una finalización." width="100%" style="height:auto">

## Qué ofrece

- **Shells de clase** que llevan lo que comparte un tipo de dispositivo: HID, los chips FTDI, carga de firmware y renumeración EZ-USB, CDC-ACM, USBTMC, almacenamiento masivo.
- **Inyección de fallos**: peticiones STALL, respuestas cortas o basura, una transferencia que nunca termina, una desconexión en una transferencia elegida.
- **El registro de transacciones**: cada transferencia que hace el host, en un dialecto en el que se escriben los goldens.

Todo el enfoque de pruebas de oxrok se apoya en él: los modelos de dispositivo en [Pruebas]({{< relref "testing" >}}) son modelos de vusb, conectados mediante `vhci-hcd` para que el kernel vea un dispositivo USB real.

[El repositorio de vusb](https://github.com/oxrok/vusb) ·
[crates.io](https://crates.io/crates/vusb) ·
[docs.rs](https://docs.rs/vusb)
