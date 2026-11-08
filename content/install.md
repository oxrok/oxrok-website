---
title: Install
---

One binary, built with `cargo` alone, with static builds for Linux, macOS and
Windows. The latest release is 0.2.0.

## From crates.io

With Rust 1.95 or newer:

```
cargo install oxrok --version 0.2.0 --locked
```

Or, from a checkout, which has what was merged since:

```
cargo install --path . --locked
```

Binary archives, where a release has them, are on the repository's
[Releases page](https://github.com/oxrok/oxrok/releases). Each file has a
`.sha256`. One archive per target: Linux x86_64 and aarch64 (static, musl),
macOS x86_64 and arm64, Windows x86_64. It has `oxrok` built with
`rustpython`, libsigrokdecode 0.5.3's `decoders/` to keep next to it, and the
notices. There is also one source tarball, with every crate vendored, so that
`make dist` works in it with no network. No firmware is in either.

## On Linux

A USB device is root only without a udev rule, and oxrok ships no rules yet.
A rule with `MODE="0666"` for the device's `VID:PID` does. macOS and Windows
need nothing beyond the [USB notes](/docs/usb/).

## Firmware

Drivers that upload firmware look for it where libsigrok does
(`SIGROK_FIRMWARE_DIR`, `sigrok-firmware` under the data directories), with
oxrok's names first at each step. oxrok ships none.

## Features

| feature | what | needs |
|---|---|---|
| `cli` (default) | the `oxrok` binary | |
| `nusb` (default) | pure Rust USB backend: Linux, macOS, Windows, Android | |
| `libusb` | libusb backend, also for the BSDs, Solaris, Haiku; built from source. `OXROK_USB_BACKEND=libusb` selects it, nusb stays the default | a C compiler |
| `rustpython` | Python decoders on RustPython, built into the binary | Rust 1.96 or newer, `--locked` |
| `python` | Python decoders on the system's CPython, through pyo3 | Python 3.9 or newer with its shared library, at build and run time |

```
cargo install --path . --locked --features rustpython
cargo install --path . --locked --features python
```

Either feature needs the decoders themselves: `brew install libsigrokdecode`,
your distribution's package, or the `decoders` directory of a libsigrokdecode
checkout (0.5.3 is the version oxrok follows). To check:

```
oxrok -L                       # lists the Python decoders too
oxrok -P can --show            # a decoder with no native version
```

A native decoder takes precedence over a Python one with the same id. With
both features, CPython is used unless `OXROK_PYTHON=rustpython`.
