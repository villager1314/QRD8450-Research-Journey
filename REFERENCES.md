# 资料与归属

初版主要依据本机实验输出与研究过程整理。以下为相关上游项目入口，不代表上游认可本仓库结论；本文未据这些链接新增未经核验的技术结论。

- [Droidspaces](https://github.com/ravindu644/Droidspaces-OSS)
- [Anland](https://github.com/Goldzxcbug/anland)
- [Mesa](https://gitlab.freedesktop.org/mesa/mesa)
- [KDE Plasma](https://kde.org/plasma-desktop/)
- [KernelSU](https://github.com/tiann/KernelSU)
- [TWRP](https://github.com/TeamWin)

后续引用外部代码应记录仓库、路径、commit/tag 和许可证。本仓库不附上述项目的二进制，也不将自写二进制修改脚本描述为上游官方修复。

本初版尚未选择统一许可证；后续应分别明确原创文档、原创脚本与第三方内容的许可。

## 本机原始材料复核（2026-10-29）

这些是本机材料定位信息，不是公开下载链接；仓库未复制固件或完整设备日志。

| 材料 | 本轮复核结果 |
| --- | --- |
| `D:/qrd/8450V3固件/QCTool_ParReadback_2024.09.25_00.33.37.715/boot_a.img` | 直接读取：100,663,296 字节、ANDROID!、header v4；SHA-256：`87c63cc4319205d731837d37b71c256b64aaa4ebde5384e989ab8e65a8d7f54f` |
| `D:/workspace/UotanToolbox/Bin/platform-tools/lkm4ctr-debug-3.txt` | 直接读取；SHA-256：`9a2ddf88d0eb1f5e290c15d92e15a3614211fe45af89329b153d8dedde4bdde0`；行 843、1320、1325 为 ksud / KernelSU 证据；行 3603、3605、3609 为模块自报初始化及错误 |
| `QRD8450_lkm4ctr_layout_audit.md` | 未找到原文；无法核实审计样本身份、字段清单、原厂指令与偏移。不能将用户提供的摘要当作已复核证据 |

已在 C:、D: 按审计文件名检索，并补查用户目录、临时目录与本机 Codex 会话；部分目录不可读，未读取认证或密钥，也未访问独立云端材料，因此不声称查全。现有两份 KO 的 DWARF 比较不是原厂内核指令审计的替代证据。

详细结论见[启动层](docs/boot/README.md)、[模块研究](docs/modules/README.md)、[研究历程](docs/journal/README.md)及[历史会话索引](docs/journal/history-evidence.md)。
