---
title: vusb
---

<img src="/vusb/lockup.svg" alt="vusb" width="220" style="height:auto">

**vusb 把一个纯 Rust 代码构成的 USB 设备放到了总线上。** 无需硬件即可测试你的驱动，可在 CI 中进行，并支持故障注入。

<img src="/vusb/hero.svg" alt="你的软件通过 USB 与一个纯 Rust 代码、无需硬件的设备通信。" width="100%" style="height:auto">

在 Linux 上，这个设备对整个机器都是真实的：`lsusb` 会列出它，libusb、hidraw、`/dev/ttyACM0` 和 `/dev/ttyUSB0` 都能使用。在单元测试中，它不需要内核，也不需要 root。无论哪种方式都是同一份代码，而且每当主机违反协议时它都会报告。

## 一个模型

这个串口会把收到的内容转成大写回传。CDC-ACM 外壳处理 USB 这一侧，因此模型只需处理字节：

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

## 各层

程序、连接在电缆上的主机，或者测试，都通过相同的总线层和设备层触达你的设备模型；`vusb-ctl` 在它运行时控制它。

<img src="/vusb/overview.svg" alt="程序、连接在电缆上的主机或测试，都通过相同的总线层和设备层触达你的设备模型。vusb-ctl 在它运行时控制它。" width="100%" style="height:auto">

## 一次传输是如何完成的

模型以 NAK 应答的传输会被总线保留，并再次提供，直到模型有数据为止。只有到那时主机才会看到完成。

<img src="/vusb/transfer.svg" alt="模型以 NAK 应答的传输会被总线保留，并再次提供，直到模型有数据为止。只有到那时主机才会看到完成。" width="100%" style="height:auto">

## 它提供什么

- **类别外壳**，承载一类设备共享的部分：HID、FTDI 芯片、EZ-USB 固件上传与重新枚举、CDC-ACM、USBTMC、大容量存储。
- **故障注入**：STALL 请求、过短或垃圾应答、永不完成的传输、在选定传输处拔插。
- **传输日志**：主机发出的每一次传输，采用 golden 测试所书写的方言。

oxrok 的整个测试方法都建立在它之上：[测试]({{< relref "testing" >}})中的设备模型就是 vusb 模型，通过 `vhci-hcd` 挂载，让内核看到一个真实的 USB 设备。

[vusb 仓库](https://github.com/oxrok/vusb) ·
[crates.io](https://crates.io/crates/vusb) ·
[docs.rs](https://docs.rs/vusb)
