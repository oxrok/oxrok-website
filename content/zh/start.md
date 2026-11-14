---
title: 开始使用
---

五个步骤，全部使用内置的 `demo` 驱动——无需硬件。请先安装 oxrok，或查看完整的[安装]({{< relref "install" >}})页面：

{{< install >}}

## 1. 列出驱动

<div class="term">
  <button class="copy" type="button">复制</button>
  <pre><span class="prompt">$</span> <span class="cmd">oxrok -L</span>
Supported hardware drivers:
  agilent-dmm          Agilent U12xx series DMMs
  appa-55ii            APPA 55II
  arachnid-labs-re-load-pro Arachnid Labs Re:load Pro
  ...</pre>
</div>

164 个驱动 id，其中大多数是万用表。

## 2. 扫描并查看

<div class="term">
  <button class="copy" type="button">复制</button>
  <pre><span class="prompt">$</span> <span class="cmd">oxrok -d demo --show</span>
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
    Analog: channels A0 A1 A2 A3 A4</pre>
</div>

## 3. 采集

`--samples`、`--time`、`--frames` 限制运行时长；`-C` 选择通道；`-O` 选择输出格式。

<div class="term">
  <button class="copy" type="button">复制</button>
  <pre><span class="prompt">$</span> <span class="cmd">oxrok -d demo --samples 4 -O bits</span>
oxrok 0.3.0-alpha.1
Acquisition with 8/13 channels at 200 kHz
A0: -10.0000 V DC
A0: -10.0000 V DC
...</pre>
</div>

demo 的随机模拟通道在两种工具中每次运行都不同。

## 4. 触发

`-t` 设置触发条件，`-w` 在保存数据前等待触发。匹配条件写作 `channel=value`，因此 `D0=r` 在 D0 的上升沿触发：

<div class="term">
  <button class="copy" type="button">复制</button>
  <pre><span class="prompt">$</span> <span class="cmd">oxrok -d demo -t 'D0=r' -w --samples 4 -O bits</span></pre>
</div>

两个容易出错的写法：`D0:r` 是扫描选项，不是触发匹配；不带任何限制的采集只会打印用法说明。

## 5. 解码

`-P` 运行协议解码器，`-A` 选择要显示的注解类别。

<div class="term">
  <button class="copy" type="button">复制</button>
  <pre><span class="prompt">$</span> <span class="cmd">oxrok -i tests/fixtures/uart-hi.vcd -P uart:baudrate=115200:rx=top.D0 -A uart=rx-data</span>
uart-1: 48
uart-1: 69
uart-1: 21
uart-1: 0A
uart-1: 00
uart-1: FF</pre>
</div>

那就是十六进制的 `Hi!`。

## 真实设备

`conn=` 指定端口或设备；在 Linux 上，没有 udev 规则时 USB 设备仅 root 可用。一个串口万用表：

<div class="term">
  <button class="copy" type="button">复制</button>
  <pre><span class="prompt">$</span> <span class="cmd">oxrok -d uni-t-ut61e-ser:conn=/dev/ttyUSB0 --samples 10</span></pre>
</div>

一台 SCPI 示波器：

<div class="term">
  <button class="copy" type="button">复制</button>
  <pre><span class="prompt">$</span> <span class="cmd">oxrok -d rigol-ds:conn=tcp://192.168.1.50 --samples 1000 -O csv</span></pre>
</div>

## 从 sigrok-cli 迁移

命令行接受 sigrok-cli 常用流程的参数，并打印相同的输出——除第一行标题外逐字节相同。容易踩坑的差异：

- 失败的采集以退出码 1 结束，并在 stderr 说明原因；sigrok-cli 在大多数情况下退出码为 0。
- 数值解析更严格：带小数的尺寸保留其单位（`samplerate=12.5M` 即 12.5 MHz），而裸小数会被拒绝。
- 标题行显示 `oxrok <version>` 而不是 `libsigrok <version>`。
- 触发支持扩展形式（`D0=r*5`、`D0=1>50us`、`D0-D2=3..5`、`D0=r|D1=r`）；sigrok-cli 会拒绝它们。
- `--strict` 把每个警告都变成失败的运行。

完整参考见 [CLI 指南]({{< relref "docs/cli" >}})。
