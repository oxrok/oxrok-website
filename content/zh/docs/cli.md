---
title: oxrok 命令行
type: docs
---

`oxrok` 接受 sigrok-cli 常用流程的参数，并打印相同的输出——除第一行标题（标明工具名）外逐字节相同。

## 选项

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

## 输出

`bits`、`hex`、`ascii`、`analog`、`csv`、`vcd`、`binary`、`srzip` 和 `null`。输入：`.sr`、VCD 和二进制。

## 触发

`-t` 接受以 `;` 分隔的多个阶段，例如 `-t 'D0=r;D1=1'`。单个阶段的写法与 sigrok-cli 相同。在此之上，若设备支持（解析器会拒绝不支持的部分）：

- `D0=r*5` 在第五个上升沿触发，`D0=r*5c` 在连续第五个上升沿触发。
- `D0=1>100` 在 D0 持续高电平超过 100 个采样后触发，`D0=1>50us` 使用时间，并按采样率换算。
- `D0-D2=3..5` 在 D2 D1 D0 的值位于 3..5 之间时触发，`D0-D2=!7` 在该值不为 7 时触发。十进制或 `0x` 十六进制。
- `D0=r|D1=r` 在任一阶段触发，`D0=r&D1=r` 在两者以任意顺序都已触发后触发。恰好两个阶段。

`>`、`;`、`|` 和 `&` 在 shell 中需要加引号。

## 退出状态

按要求完成运行时为 0；否则为 1，并在 stderr 说明原因。一次已开始的采集，只要它因任何非正常原因结束——达到限制、主动停止（Ctrl-C、设备自身的取消按钮）、或设备数据的自然结束——都算失败。因此以下情况会失败：设备离开、读取或写入错误、轮询或重试限制放弃、静默超时结束了一次未达到限制的采集、无限制的流耗尽、以及输出无法再写入（磁盘已满）。

失败的采集会在其写出的最后一行说明原因：

```
capture failed: device disconnected
```

冒号后是驱动自身的错误。失败之前的内容会被写出并刷新；输出随后关闭。主动停止优先于其后到来的失败：这样的运行退出码为 0。

## 尚不可用

- `--protocol-decoder-jsontrace`。Python 协议解码器需要 `python` 构建特性；参见[协议解码器](/docs/decoders/)。
- `-T`（变换模块）、`--list-supported-wiki`、`csv` 输出的 `gnuplot` 和 `scale` 选项。
- `csv` 输入以及其他长尾输入模块。
- 其他 libsigrok 硬件驱动：其余的串口仪器紧随其后，再往后是其余部分。
