---
title: Testing
---

Most drivers here have never met their device. This page is about the only
way to check them without the hardware — and where that checking stops.

## The problem

libsigrok has 87 drivers, for hardware none of us has. Porting them from the C
source alone would give code that compiles and has never talked to anything.
Recordings are the usual fallback, but they need the devices too.

## The idea

A device model in Rust, attached through Linux's `vhci-hcd` over USB/IP, so
the kernel sees a real USB device. The real `sigrok-cli` and `oxrok` run
unmodified against the same device, and every transaction is logged. Then
compare.

{{< emulator >}}

## What is compared

The output, the errors, the exit status, every USB transfer, plus gcov on the C
driver to see what was reached. Identical bytes on the wire is a tighter claim
than identical output. It is not unconditional: node numbers and device
addresses are made generic, and a case can filter what differs for a stated
reason.

## The models are hostile

A model does not accept whatever arrives. It flags transfers to endpoints the
configuration lacks, what its protocol forbids, and it misbehaves on request:
STALLed requests, short or garbage answers, a transfer that never completes, an
unplug at a chosen transfer. Error paths are where the C and the port differ
most.

## What it cannot tell you

A model is built from the C driver and whatever public sources exist, so it can
share the C's misunderstanding of the device. Matching it proves parity with
libsigrok on the paths the cases reach, not correct behaviour on hardware.
Timing is not real: models count the host's transfers rather than the clock, and
USB/IP has no bus. So real evidence outranks it: recordings, manuals, history.
Quirks the C relies on without saying cannot be found this way.

Numbers: **{{% numbers %}}**

[How drivers are tested in the README](https://github.com/oxrok/oxrok/blob/main/README.md#how-drivers-are-tested)
and [the USB emulation notes](https://github.com/oxrok/oxrok/blob/main/docs/USB.md).
