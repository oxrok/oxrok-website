---
title: The oxrok command line
---

`oxrok` takes the sigrok-cli flags for the common flows and prints the same
output, byte for byte after the first header line (which names the tool).

## Options

```
-V, --version                 Show version and support list
-L, --list-supported         List supported devices/modules/decoders
-l, --loglevel <LEVEL>       Set loglevel (0-5, default 2)
    --strict                 Treat warnings as errors: stop and exit with failure
-d, --driver <DRIVER>        The driver to use, with scan options: driver[:key=value]...
-c, --config <CONFIG>        Device option: [channel_group=GROUP:]key=value[:key=value]...
-i, --input-file <FILE>      Load input from file (- for stdin)
-I, --input-format <FORMAT>  Input format: module[:option=value]...
-o, --output-file <FILE>     Save output to file
-O, --output-format <FORMAT> Output format: module[:option=value]...
-C, --channels <CHANNELS>    Channels to use: names or ranges, comma separated, name=newname to rename
-g, --channel-group <GROUP>  Channel group to show or configure
-t, --triggers <TRIGGERS>    Trigger: channel=matches[,channel=matches]... with ; between stages
-w, --wait-trigger           Wait for trigger before saving data
    --scan                   Scan for devices
    --show                   Show device details
    --time <TIME>            How long to sample (ms, or with a unit: 2s, 500ms)
    --samples <SAMPLES>      Number of samples to acquire (with size suffix: 1k, 2m)
    --frames <FRAMES>        Number of frames to acquire
    --continuous             Sample continuously until stopped
-P, --protocol-decoders <DECODERS>            Protocol decoders to run
-A, --protocol-decoder-annotations <ANN>      Annotations to show
-B, --protocol-decoder-binary <BIN>           Binary output to show
-M, --protocol-decoder-meta <META>            Decoder metadata to show
    --protocol-decoder-samplenum             Show sample numbers with annotations
    --protocol-decoder-ann-class            Show the annotation class with annotations
    --get <KEY>                Get device option only: [channel_group=GROUP:]key
    --set                      Set device options only
```

## Outputs

`bits`, `hex`, `ascii`, `analog`, `csv`, `vcd`, `binary`, `srzip` and `null`.
Inputs: `.sr`, VCD and binary.

## Triggers

`-t` takes stages separated by `;`, e.g. `-t 'D0=r;D1=1'`. One stage is written
as in sigrok-cli. On top of that, where the device supports it (the parser
rejects what it does not):

- `D0=r*5` fires on the fifth rising edge, `D0=r*5c` on the fifth in a row.
- `D0=1>100` fires once D0 has been high for more than 100 samples,
  `D0=1>50us` with a time, converted with the sample rate.
- `D0-D2=3..5` fires while the value on D2 D1 D0 is within 3..5,
  `D0-D2=!7` while it is not 7. Decimal or `0x` hex.
- `D0=r|D1=r` fires on either stage, `D0=r&D1=r` once both have fired in any
  order. Exactly two stages.

`>`, `;`, `|` and `&` need quoting in a shell.

## Exit status

0 when the run did what was asked; 1 otherwise, with the reason on stderr. A
capture that started has failed when it ended for any reason other than a limit
being met, a stop asked for (Ctrl-C, a device's own cancel button), or the
natural end of the device's data. So these fail: a device that leaves, a read or
write error, a poll or retry limit giving up, a bound on silence that ends a
capture whose limit was not met, a stream with no limit that runs out, and an
output that can no longer be written (a full disk).

A failed capture says so on one line, the last one it writes:

```
capture failed: device disconnected
```

with the driver's own error after the colon. What came before the failure is
written and flushed; the output is closed. A stop wins over a failure that comes
after it: such a run exits 0.

## Not available yet

- `--protocol-decoder-jsontrace`. Python decoders need the `python` build
  feature; see [Protocol decoders](/docs/decoders/).
- `-T` (transform modules), `--list-supported-wiki`, the `gnuplot` and `scale`
  options of the `csv` output.
- The `csv` input and the other long-tail input modules.
- The other libsigrok hardware drivers: the rest of the serial instruments come
  next, the rest after them.
