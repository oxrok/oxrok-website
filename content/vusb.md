---
title: vusb
---

<img src="{{ "vusb/lockup.svg" | relURL }}" alt="vusb" width="220" style="height:auto">

**vusb puts a USB device on the bus that is only Rust code.** Test your driver
without the hardware, in CI, and with fault injection.

On Linux the device is real to the whole machine: `lsusb` lists it, and libusb,
hidraw, `/dev/ttyACM0` and `/dev/ttyUSB0` all work. In a unit test it needs no
kernel and no root. Either way it is the same code, and it reports every time
the host breaks the protocol.

## A model

This serial port answers in capitals. The CDC-ACM shell handles the USB side,
so the model only sees bytes:

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

## What it offers

- **Class shells** that carry what a kind of device shares: HID, the FTDI
  chips, EZ-USB firmware upload and renumeration, CDC-ACM, USBTMC, mass
  storage.
- **Fault injection**: STALLed requests, short or garbage answers, a transfer
  that never completes, an unplug at a chosen transfer.
- **The transaction log**: every transfer the host makes, in a dialect the
  goldens are written in.

oxrok's whole test approach rests on it: the device models in
[Testing](/testing/) are vusb models, attached through `vhci-hcd` so the kernel
sees a real USB device.

[The vusb repository]({{ .Site.Params.vusb_repo }}) ·
[crates.io](https://crates.io/crates/vusb) ·
[docs.rs](https://docs.rs/vusb)
