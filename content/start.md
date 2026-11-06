---
title: Getting started
---

A path of five small steps, each a command and its output, using `demo` so
anyone can follow with no hardware.

## 1. List the drivers

```
$ oxrok -L
Supported hardware drivers:
  agilent-dmm          Agilent U12xx series DMMs
  appa-55ii            APPA 55II
  arachnid-labs-re-load-pro Arachnid Labs Re:load Pro
  ...
```

164 driver ids, most of them multimeters.

## 2. Scan and show

```
$ oxrok -d demo --show
Driver functions:
    Demo device
    Logic analyzer
    Oscilloscope
Scan options:
    logic_channels
    analog_channels
    limit_frames
demo - Demo device with 13 channels: D0 D1 D2 D3 D4 D5 D6 D7 A0 A1 A2 A3 A4
Channel groups:
    Logic: channels D0 D1 D2 D3 D4 D5 D6 D7
    Analog: channels A0 A1 A2 A3 A4
```

## 3. Capture

`--samples`, `--time`, `--frames` limit the run; `-C` selects channels; `-O`
picks the output format.

```
$ oxrok -d demo --samples 4 -O bits
oxrok 0.1.0-alpha.2
Acquisition with 8/13 channels at 200 kHz
A0: -10.0000 V DC
A0: -10.0000 V DC
...
```

The demo's random analog channel differs from run to run in both tools.

## 4. Trigger

`-t` arms a trigger, `-w` waits for it before saving data. The form is
`channel=match`:

```
$ oxrok -d demo -t 'D0=r' -w --samples 4 -O bits
```

`D0:r` is the wrong form (that is a scan option, not a trigger match), and a
capture with no limit only prints the usage. The right form is `D0=r`: fire on
a rising edge of D0.

## 5. Decode

`-P` runs a protocol decoder, `-A` selects the annotation classes to show.

```
$ oxrok -i tests/fixtures/uart-hi.vcd -P uart:baudrate=115200:rx=top.D0 -A uart=rx-data
uart-1: 48
uart-1: 69
uart-1: 21
uart-1: 0A
uart-1: 00
uart-1: FF
```

That is `Hi!` in hex.

## Real devices

`conn=` names the port or device; on Linux a USB device is root only without a
udev rule. A serial meter:

```
oxrok -d uni-t-ut61e-ser:conn=/dev/ttyUSB0 --samples 10
```

A SCPI scope:

```
oxrok -d rigol-ds:conn=tcp://192.168.1.50 --samples 1000 -O csv
```

## Coming from sigrok-cli

The command line takes the sigrok-cli flags for the common flows and prints the
same output, byte for byte after the first header line. The differences that
bite:

- A capture that fails exits 1 and says why on stderr; sigrok-cli exits 0 on
  most of them.
- Values are parsed more strictly: a size with a fraction keeps its suffix
  (`samplerate=12.5M` is 12.5 MHz), and a bare fraction is refused.
- The header line says `oxrok <version>` instead of `libsigrok <version>`.
- Triggers take the extended forms (`D0=r*5`, `D0=1>50us`, `D0-D2=3..5`,
  `D0=r|D1=r`); sigrok-cli rejects them.
- `--strict` turns every warning into a failed run.

The full reference is in the [CLI guide](/docs/cli/).
