---
title: 图形界面
---

**oxrok-ui 是 oxrok 的采集、显示、测量和解码界面**，基于 [egui](https://egui.rs) 用 Rust 编写。它与命令行工具使用相同的设备和协议解码器，并且可以运行在内置的模拟设备上，因此你无需硬件即可试用。

<div class="term">
  <button class="copy" type="button">复制</button>
  <pre><span class="prompt">$</span> <span class="cmd">cargo install oxrok-ui --version {{% uiversion %}} --locked</span>
<span class="prompt">$</span> <span class="cmd">cargo install --features mock oxrok-ui --version {{% uiversion %}} --locked</span>  # 无需硬件：内置模拟设备</pre>
</div>

## 采集视图

缩放到 2 ms 窗口：一个 UART 帧、SPI 传输和时钟边沿，数据表中是解码后的协议。

<img src="/ui/capture.png" alt="采集视图，缩放到 2 ms 窗口" width="100%" style="height:auto">

浅色主题下同样的画面（视图 → 主题）：

<img src="/ui/capture-light.png" alt="浅色主题下的采集视图" width="100%" style="height:auto">

## 行、行菜单和缩放工具

行可以就地重命名（CLK、UART TX、SPI CS、…）；行上下文菜单用于显示和隐藏通道。缩放工具增加了范围缩放模式和*相对缩放*。

<img src="/ui/row-menu.png" alt="行上下文菜单，含就地重命名的行" width="100%" style="height:auto">

<img src="/ui/zoom-tool.png" alt="缩放工具：范围缩放模式和相对缩放" width="100%" style="height:auto">

## 解码协议

协议分析器会在其通道上方绘制气泡，并提供一个可搜索的数据表。

<img src="/ui/analyzers.png" alt="协议分析器：通道上方的气泡和可搜索的数据表" width="100%" style="height:auto">

## 标记与测量

一对标记、一个带指标弹窗的范围测量，以及时序标记面板。

<img src="/ui/markers.png" alt="一对标记、一个带指标弹窗的范围测量，以及时序标记面板" width="100%" style="height:auto">

## 启动界面

<img src="/ui/start-screen.png" alt="启动界面" width="100%" style="height:auto">

## 使用它

- **打开设备**——启动界面，或*设备*菜单 → *新建会话*
- **录制**——`Space`；*定时*模式会自动停止
- **缩放 / 平移**——滚轮、拖拽、`=`/`-`、缩放工具
- **标记和测量**——`M`、`Shift+M`、`R`
- **解码协议**——工具栏的六边形按钮或分析器面板
- **保存 / 打开**——`Ctrl/Cmd+S` / `Ctrl/Cmd+O`（`.oxrok`）
- **全部快捷键**——`?`（可搜索）；任意命令——`Ctrl/Cmd+K`

截图在每次发布时重新生成，来自与 oxrok 对齐的 [oxrok-ui 仓库](https://github.com/oxrok/ui)。
