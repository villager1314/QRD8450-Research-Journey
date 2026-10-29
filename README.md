# QRD8450 Research Journey

QRD8450（Qualcomm Waipio QRD）个人研究历程：记录设备探索、Android 启动层、Linux 桌面容器、内核模块及 Recovery 适配研究。

这里整理的是单台设备的实测记录，不代表所有 QRD8450，也不是 Qualcomm 或各上游项目的官方文档。当前记录整理于 2026-10-29。

## 研究导航

| 方向 | 内容 | 状态 |
| --- | --- | --- |
| [设备信息](docs/hardware/README.md) | 设备树、SoC、系统和内核 | 已采集部分信息 |
| [Android 启动层](docs/boot/README.md) | 启动链、分区、启动镜像与 DSU | 研究中 |
| [Droidspaces](docs/droidspaces/README.md) | GPU、SSH、桌面与服务排错 | 部分已验证 |
| [模块与注入](docs/modules/README.md) | 内核模块、KernelSU 与用户空间注入的区别 | 研究中 |
| [Recovery / TWRP](docs/recovery/README.md) | 专用 Recovery 适配规划 | 尚无可用适配成果 |
| [研究历程](docs/journal/README.md) | 实验经过、成功结果和未解决问题 | 持续整理 |

## 已验证的结果

- Ubuntu 和 Arch 的指定 Mesa Gallium 二进制修改 GPU 匹配表后，可以创建 FD730 的 EGL / OpenGL 上下文。
- 指定容器中的 UPower 用户命名空间启动失败，通过单服务 `PrivateUsers=no` 覆盖后能够启动。
- Arch KDE 曾因 Plasma 组件版本混用而缺库或崩溃；调整部分组件后观察到 plasmashell 和 Chrome 运行。
- Arch KDE Mobile 中 KWin 使用 `wayland-1`，用户服务却指向 `wayland-0`；临时修正环境后 plasmashell 能启动。

这些结果不等于完整 GPU 兼容性、长期稳定性或重启持久性已经验证。Denial 卡顿、Mobile 快捷设置和屏幕键盘语言切换仍有待研究。

## 记录方式

每篇实验尽量包含：环境、原始现象、假设、操作、结果、回滚与尚未确认的事项。失败的方案也保留，避免重复试错。

[实验模板](docs/experiment-template.md) · [资料与归属](REFERENCES.md) · [本地使用与推送](PUSH.md)

本仓库初版不包含固件、驱动二进制、设备密钥或可刷写 Recovery。补丁脚本严格限制为已核验的驱动文件；运行前阅读对应文档。

## 历史证据补录

已补录启动固件离线分析、Gunyah 配置、模块加载失败和 KernelSU 日志线索；TWRP 仍缺适配证据。[会话证据索引](docs/journal/history-evidence.md)列出来源、验证程度与云端核查限制。
