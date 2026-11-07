---
title: USB and emulation
---

Drivers talk to devices through one small `Transport` trait — control
and bulk transfers with timeouts, interface claims and resets — and
never see which backend is in use. Serial, TCP, HID and SCPI are
separate transports with the same shape.

| feature | backend | platforms |
|---|---|---|
| `nusb` (default) | pure Rust, no system library | Linux, macOS, Windows, Android |
| `libusb` | rusb, built from source | the above, plus the BSDs, Solaris, Haiku |

With both compiled in, `OXROK_USB_BACKEND=libusb` or `=nusb` picks one
at run time; nusb is the default.

## Connecting

`conn=` names the port or device: a `/dev/ttyUSB0`, a `tcp://` address,
or a USB `bus.address`. On Linux a USB device is root only without a
udev rule — a rule with `MODE="0666"` for the device's `VID:PID` does.
macOS and Windows need nothing beyond the notes in the
[repository's USB doc](https://github.com/oxrok/oxrok/blob/main/docs/USB.md#troubleshooting).

## A driver that misbehaves: record and replay

Most driver problems show up only on one device, and whoever could fix
them doesn't have it. oxrok's answer is a recording:

```sh
OXROK_USB_RECORD=capture.txt oxrok -d intronix-logicport --samples 64
```

Every USB transfer — control and bulk, requests and answers — lands in
a small text file, readable and hand editable:

```text
# oxrok usb fixture 1
device vid=0403 pid=dc48 product="LogicPort Logic Analyzer"
claim 0 -> ok
ctl_out 40 09 0004 0000 - -> ok
ctl_in 40 0a 0000 0000 1 -> 04
bulk_in 81 4096 -> 3160aabb
```

Send that file with a [hardware
report](https://github.com/oxrok/oxrok/issues/new?template=hardware-report.yml),
and the problem replays on any machine, with no device:

```sh
OXROK_USB_REPLAY=capture.txt oxrok -d intronix-logicport --samples 64
```

A replay fails at the first transfer that differs from the recording,
which pins down where a driver's behaviour changed. The tests are built
the same way: every driver ships with at least one recorded session,
and CI plays them back without hardware. `OXROK_HID_RECORD` and
`OXROK_HID_REPLAY` do the same for HID devices.

## Emulation over USB/IP

A recording replays what happened; an emulated device can do anything.
`oxrok-emu` attaches a device model in Rust through Linux's `vhci-hcd`,
so the kernel sees a real USB device, and sigrok-cli and oxrok run
unmodified against the same model. That is the basis of the whole
[testing](/testing/) story:

{{< emulator >}}

The models and the harness are in the
[repository](https://github.com/oxrok/oxrok/tree/main/emu), built on the
[vusb](https://github.com/oxrok/vusb) crate.

The full reference — the record format, streams, writing a device model,
the per-OS troubleshooting — stays in the
[repository's `docs/USB.md`](https://github.com/oxrok/oxrok/blob/main/docs/USB.md).
