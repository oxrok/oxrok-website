---
title: 安装
---

单个二进制，仅用 `cargo` 构建，为 Linux、macOS 和 Windows 提供静态构建。最新版本是 0.2.0。

## 从 crates.io 安装

需要 Rust 1.95 或更新版本：

```
cargo install oxrok --version 0.2.0 --locked
```

或者，从源码检出安装（包含合并之后的内容）：

```
cargo install --path . --locked
```

有二进制归档的版本，位于仓库的 [Releases 页面](https://github.com/oxrok/oxrok/releases)。每个文件都有对应的 `.sha256`。每个目标平台一个归档：Linux x86_64 与 aarch64（静态，musl）、macOS x86_64 与 arm64、Windows x86_64。其中包含使用 `rustpython` 构建的 `oxrok`、需要放在其旁边的 libsigrokdecode 0.5.3 的 `decoders/` 目录，以及版权声明。另外还有一个源码 tar 包，其中包含了所有 crate 的本地副本，因此无需联网即可在其内运行 `make dist`。两者都不包含固件。

## 在 Linux 上

没有 udev 规则时，USB 设备仅 root 可用，而 oxrok 目前不附带任何规则。为设备的 `VID:PID` 添加一条 `MODE="0666"` 的规则即可。macOS 和 Windows 无需额外配置，只需参考 [USB 说明]({{< relref "docs/usb" >}})。

## 固件

需要上传固件的驱动会按照 libsigrok 的方式查找固件（`SIGROK_FIRMWARE_DIR`、数据目录下的 `sigrok-firmware`），每一步都优先使用 oxrok 的文件名。oxrok 不附带任何固件。

## 功能特性

| 特性 | 作用 | 需要 |
|---|---|---|
| `cli`（默认） | `oxrok` 二进制 | |
| `nusb`（默认） | 纯 Rust 的 USB 后端：Linux、macOS、Windows、Android | |
| `libusb` | libusb 后端，也用于 BSD、Solaris、Haiku；从源码构建。用 `OXROK_USB_BACKEND=libusb` 选择它，nusb 仍是默认 | 一个 C 编译器 |
| `rustpython` | 在内置的 RustPython 上运行 Python 协议解码器 | Rust 1.96 或更新版本，`--locked` |
| `python` | 通过 pyo3 在系统的 CPython 上运行 Python 协议解码器 | Python 3.9 或更新版本及其共享库，构建和运行时都需要 |

```
cargo install --path . --locked --features rustpython
cargo install --path . --locked --features python
```

任一特性都需要协议解码器本身：`brew install libsigrokdecode`、你的发行版软件包，或 libsigrokdecode 源码检出的 `decoders` 目录（oxrok 遵循的版本是 0.5.3）。检查方法：

```
oxrok -L                       # 同时列出 Python 协议解码器
oxrok -P can --show            # 一个没有原生版本的协议解码器
```

原生协议解码器优先于具有相同 id 的 Python 版本。同时启用两个特性时，除非设置 `OXROK_PYTHON=rustpython`，否则使用 CPython。
