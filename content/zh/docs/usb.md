---
title: USB 与仿真
type: docs
---

驱动通过一个很小的 `Transport` trait 与设备通信——带超时的控制传输和批量传输、接口占用和重置——并且从不知道使用的是哪个后端。串口、TCP、HID 和 SCPI 是形状相同的独立传输。

| 特性 | 后端 | 平台 |
|---|---|---|
| `nusb`（默认） | 纯 Rust，无系统库 | Linux、macOS、Windows、Android |
| `libusb` | rusb，从源码构建 | 上述平台，以及 BSD、Solaris、Haiku |

若两者都编译进去，`OXROK_USB_BACKEND=libusb` 或 `=nusb` 在运行时选择其一；nusb 是默认。

## 连接

`conn=` 指定端口或设备：一个 `/dev/ttyUSB0`、一个 `tcp://` 地址，或一个 USB `bus.address`。在 Linux 上，没有 udev 规则时 USB 设备仅 root 可用——为设备的 `VID:PID` 添加一条 `MODE="0666"` 的规则即可。macOS 和 Windows 无需额外配置，只需参考[仓库中的 USB 文档](https://github.com/oxrok/oxrok/blob/main/docs/USB.md#troubleshooting)。

## 行为异常的驱动：录制与回放

大多数驱动问题只出现在某台设备上，而能修复它的人却没有这台设备。oxrok 的答案是录制：

```sh
OXROK_USB_RECORD=capture.txt oxrok -d intronix-logicport --samples 64
```

每一次 USB 传输——控制与批量、请求与应答——都会落入一个小文本文件，可读也可手工编辑：

```text
# oxrok usb fixture 1
device vid=0403 pid=dc48 product="LogicPort Logic Analyzer"
claim 0 -> ok
ctl_out 40 09 0004 0000 - -> ok
ctl_in 40 0a 0000 0000 1 -> 04
bulk_in 81 4096 -> 3160aabb
```

把该文件随[硬件报告](https://github.com/oxrok/oxrok/issues/new?template=hardware-report.yml)一起发送，问题就能在任何机器上复现，无需设备：

```sh
OXROK_USB_REPLAY=capture.txt oxrok -d intronix-logicport --samples 64
```

回放在与录制不同的第一处传输即失败，从而精确定位驱动行为在哪里发生了变化。测试也是以同样的方式构建的：每个驱动都至少附带一段录制的会话，CI 无需硬件即可回放它们。`OXROK_HID_RECORD` 和 `OXROK_HID_REPLAY` 对 HID 设备起同样作用。

## 通过 USB/IP 仿真

录制回放的是已发生的事；仿真设备则可以做任何事。`oxrok-emu` 通过 Linux 的 `vhci-hcd` 挂载一个 Rust 设备模型，让内核看到一个真实的 USB 设备，sigrok-cli 和 oxrok 不加修改地对同一模型运行。这正是整个[测试]({{< relref "testing" >}})故事的基石：

{{< emulator >}}

模型和测试装置在[仓库](https://github.com/oxrok/oxrok/tree/main/emu)中，构建于 [vusb](https://github.com/oxrok/vusb) crate 之上。

完整参考——录制格式、流、编写设备模型、各操作系统的故障排查——保留在[仓库的 `docs/USB.md`](https://github.com/oxrok/oxrok/blob/main/docs/USB.md)。
