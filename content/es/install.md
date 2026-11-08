---
title: Instalar
---

Un solo binario, compilado solo con `cargo`, con compilaciones estáticas para Linux, macOS y Windows. La última versión es 0.2.0.

## Desde crates.io

Con Rust 1.95 o más reciente:

```
cargo install oxrok --version 0.2.0 --locked
```

O, desde un checkout, que incluye lo fusionado desde entonces:

```
cargo install --path . --locked
```

Los archivos binarios, cuando una versión los incluye, están en la [página de Releases](https://github.com/oxrok/oxrok/releases) del repositorio. Cada archivo tiene un `.sha256`. Un archivo por objetivo: Linux x86_64 y aarch64 (estático, musl), macOS x86_64 y arm64, Windows x86_64. Incluye `oxrok` compilado con `rustpython`, el directorio `decoders/` de libsigrokdecode 0.5.3 para tener junto a él, y las notas legales. También hay un tarball de código fuente, con todas las crates incluidas, para poder ejecutar `make dist` en él sin red. Ninguno incluye firmware.

## En Linux

Un dispositivo USB es solo de root sin una regla de udev, y oxrok todavía no incluye reglas. Una regla con `MODE="0666"` para el `VID:PID` del dispositivo funciona. macOS y Windows no necesitan nada más allá de las [notas USB]({{< relref "docs/usb" >}}).

## Firmware

Los drivers que cargan firmware lo buscan donde lo hace libsigrok (`SIGROK_FIRMWARE_DIR`, `sigrok-firmware` en los directorios de datos), probando primero los nombres de oxrok en cada paso. oxrok no incluye ninguno.

## Características

| característica | qué hace | necesita |
|---|---|---|
| `cli` (por defecto) | el binario `oxrok` | |
| `nusb` (por defecto) | backend USB puro en Rust: Linux, macOS, Windows, Android | |
| `libusb` | backend libusb, también para BSD, Solaris, Haiku; compilado desde el código fuente. `OXROK_USB_BACKEND=libusb` lo selecciona; nusb sigue siendo el predeterminado | un compilador de C |
| `rustpython` | decodificadores Python sobre RustPython, integrados en el binario | Rust 1.96 o más reciente, `--locked` |
| `python` | decodificadores Python sobre el CPython del sistema, mediante pyo3 | Python 3.9 o más reciente con su biblioteca compartida, en compilación y ejecución |

```
cargo install --path . --locked --features rustpython
cargo install --path . --locked --features python
```

Cualquiera de las dos características necesita los decodificadores: `brew install libsigrokdecode`, el paquete de tu distribución, o el directorio `decoders` de un checkout de libsigrokdecode (0.5.3 es la versión que sigue oxrok). Para comprobarlo:

```
oxrok -L                       # también lista los decodificadores Python
oxrok -P can --show            # un decodificador sin versión nativa
```

Un decodificador nativo tiene prioridad sobre uno Python con el mismo id. Con ambas características, se usa CPython salvo que se defina `OXROK_PYTHON=rustpython`.
