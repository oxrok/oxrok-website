---
title: Testing
---

## The problem

libsigrok has 87 drivers for devices nobody here owns. Porting them from the C
source alone would give code that compiles and has never talked to anything.
Recordings would need the devices too.

## The idea

A device model in Rust, attached through Linux's `vhci-hcd` over USB/IP, so
the kernel sees a real USB device. The real `sigrok-cli` and `oxrok` run
unmodified against the same device, and every transaction is logged. Then
compare.

<svg viewBox="0 0 640 300" role="img" aria-label="A device model in Rust is attached to the Linux kernel over USB/IP; sigrok-cli and oxrok both run against it and their transactions are compared." style="width:100%;height:auto">
  <defs>
    <style>
      .box { fill: none; stroke: var(--steel, #557a9c); stroke-width: 2; }
      .box2 { fill: none; stroke: var(--accent, #c8501e); stroke-width: 2; }
      .lbl { fill: var(--fg, #1c1e21); font: 13px system-ui, sans-serif; }
      .sub { fill: var(--muted, #5f6670); font: 11px system-ui, sans-serif; }
      .arrow { stroke: var(--fg, #1c1e21); stroke-width: 1.5; fill: none; }
      .albl { fill: var(--muted, #5f6670); font: 11px system-ui, sans-serif; }
    </style>
  </defs>
  <!-- oxrok-emu -->
  <rect class="box" x="20" y="40" width="200" height="120" rx="6"/>
  <text class="lbl" x="120" y="66" text-anchor="middle">oxrok-emu</text>
  <text class="sub" x="120" y="90" text-anchor="middle">device model in Rust</text>
  <text class="sub" x="120" y="108" text-anchor="middle">pedantic checks</text>
  <text class="sub" x="120" y="126" text-anchor="middle">fault injection</text>
  <text class="sub" x="120" y="144" text-anchor="middle">transaction log</text>
  <!-- Linux kernel -->
  <rect class="box" x="420" y="40" width="200" height="120" rx="6"/>
  <text class="lbl" x="520" y="66" text-anchor="middle">Linux kernel</text>
  <text class="sub" x="520" y="90" text-anchor="middle">vhci-hcd</text>
  <text class="sub" x="520" y="108" text-anchor="middle">(virtual host controller)</text>
  <text class="sub" x="520" y="126" text-anchor="middle">usbcore, usbhid, ...</text>
  <!-- USB/IP arrow -->
  <line class="arrow" x1="220" y1="100" x2="420" y2="100"/>
  <polygon points="420,100 410,95 410,105" fill="var(--fg,#1c1e21)"/>
  <polygon points="220,100 230,95 230,105" fill="var(--fg,#1c1e21)"/>
  <text class="albl" x="320" y="88" text-anchor="middle">USB/IP over TCP</text>
  <!-- down to devices -->
  <line class="arrow" x1="520" y1="160" x2="520" y2="190"/>
  <text class="albl" x="520" y="182" text-anchor="middle">/dev/bus/usb, /dev/hidraw</text>
  <!-- two tools -->
  <rect class="box2" x="120" y="200" width="180" height="60" rx="6"/>
  <text class="lbl" x="210" y="226" text-anchor="middle">sigrok-cli</text>
  <text class="sub" x="210" y="244" text-anchor="middle">the oracle, the same model</text>
  <rect class="box2" x="440" y="200" width="180" height="60" rx="6"/>
  <text class="lbl" x="530" y="226" text-anchor="middle">oxrok</text>
  <text class="sub" x="530" y="244" text-anchor="middle">the port</text>
  <line class="arrow" x1="520" y1="190" x2="210" y2="200"/>
  <line class="arrow" x1="520" y1="190" x2="530" y2="200"/>
</svg>

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

## Reviews

Each model and port also goes to a reviewer, another agent, reading it against
the C, with mutation testing and stalls. The examples here are bugs found in
oxrok's own ports: a late reply that shifted every later reading, a shared
method built on a false comment about a dependency that caused a hang, and a
model whose checks never fired in any test.

Numbers: **{{% numbers %}}**

[How drivers are tested in the README](https://github.com/oxrok/oxrok/blob/main/README.md#how-drivers-are-tested)
and [the USB emulation notes](https://github.com/oxrok/oxrok/blob/main/docs/USB.md).
