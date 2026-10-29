# Android 启动层研究

## 当前范围

研究启动链、A/B 分区、boot/vendor_boot、GKI 与模块关系，以及原厂 Android 和其他系统用户空间之间的兼容性。

已观察到的内核版本为 5.10.81，设备平台为 taro。曾尝试通过 DSU 启动其他 Android 系统，未形成稳定可用结果。具体镜像版本、日志和操作顺序尚待重新归档，暂不提供可复现刷机教程。

## 后续记录

- 只读采集分区名称、当前槽位、启动镜像头和内核配置。
- 根据实际镜像分析 boot 与 vendor_boot 的职责，不凭 Android 版本假定存在 init_boot。
- 分别记录 Bootloader 解锁状态、AVB 状态与安全启动信息，避免将它们混为一谈。
- 先完成本机备份和恢复验证，再考虑启动镜像实验。

本目录目前没有经过验证的刷写指令或可分发启动镜像。

## 2026-10-23 历史补录

来源见[会话证据索引](../journal/history-evidence.md)。本轮仅复核历史，没有连接手机重新测试。

### ABL / UEFI：离线分析

同套固件的 `abl_a.img` 为 1 MiB，历史 SHA-256：
`ea26301f2e3b5883270bad2fd77209937879e348999a6d083ef5b7002ba2f3b0`。
当时从 ELF 容器的压缩固件卷解出 AArch64 PE `LinuxLoader`，包含 `taro`、`Mar 31 2022` 字符串。内部日期不等于固件发布日期。

ABL 包含 AVB、`vendor_boot`、`BootLinux`、Fastboot boot 处理线索及锁定设备禁止临时启动的错误文本；这些不能证明本机当前解锁状态或 Fastboot boot 可用。

`uefi_a.img` 当时解出两个压缩固件卷，包含 `DxeCore`、`QcomBds`、`BootOrder`、`BootNext`、`\EFI\BOOT\BOOTAA64.EFI`、USB 启动枚举线索。平台字符串为 `BOOT.MXF.2.0-00756-WAIPIO-1`。配置包括：

```ini
DefaultBDSBootApp = "LinuxLoader"
EnableShell = 0x1
DetectRetailUserAttentionHotkey = 0x00
SecurityFlag = 0xC4
```

菜单含 `Enter Shell`、`Boot USB First`。QcomBds GUID 为 `5A50AA81-C3AE-4608-A0E3-41A2E69BAF94`：原镜像固件卷位于 `0x1000`，GZIP 节位于 `0x4AF10`，解压卷内 FFS 位于 `0x364540`；两个偏移坐标不能混用。

镜像线索支持以下待核实关系：

```text
uefi_a 的 DXE / QcomBds
  → 默认应用 LinuxLoader（abl_a）
  → Android 镜像加载 / AVB / BootLinux
  → 内核 → Android 用户空间
```

尚未完成完整反汇编调用链或真机启动跟踪，更早阶段和签名链未在本轮重新核验。USB EFI、Shell、BootNext、封装为 Android boot 镜像的其他 UEFI 仍是候选路线。菜单不能证明 Shell 模块存在或入口可触发，`SecurityFlag` 不能证明整机安全启动关闭；`LoadImageAndAuth` 不能直接等同于通用 EFI `LoadImage()`。

### 内核与 Gunyah：用户回传实机输出

- `uname -a`：`5.10.81-android12-9-g7181a15d6d4b`，`SMP PREEMPT`、`aarch64`，构建时间 `Wed Mar 30 19:06:53 UTC 2022`。
- 设备树声明 Gunyah、RM、watchdog。RM 绑定 `gh_rm_driver`，watchdog、QRTR 也有驱动链接；驱动列表含 `gh_virtio_backend`。
- `guestvm_loader@e0600000` 的固件名是 `cpusys_vm`，`guestvm_loader@e0b00000` 是 `trustedvm`；两者均绑定 `qcom_guestvm_loader`。
- 发现 `/dev/gh_virtio_backend_trustedvm` 和 `cpusys_vm.mdt`、`.b00` 至 `.b04`。当时未找到 `/dev/gunyah` 或 OEM VM 加载节点，不能据此认定没有 Gunyah。
- `vmmgr` 字符串引用 `/sys/kernel/load_guestvm/boot_guestvm`，实机该目录不存在；`vmmgr --help` 无输出、返回 255，不能当作可用启动接口。
- `/product/bin/qvirtmgr` 存在。回传的 `/product/etc/qvirtmgr.json` 对两个 VM 都设置 `loader_type: secured`、`enable: true`、`legacy: true`。trustedvm 配置 `create` → `start`，磁盘为 `/vendor/vm-system/trustedvm/system.img`（label 11）；cpusys_vm 配置 `start`，未列磁盘。

这些结果确认驱动绑定、配置和固件存在，尚未确认 RM 通信、VM 运行、guest 内核来源或自定义 Linux 启动成功。`secured` / `legacy` 语义仍需实现佐证，其他设备的新接口教程不能算本机成果。

Boot 镜像头、ramdisk 分工、DTB/DTBO、槽位和内核配置仍待归档；不能从 ABL 通用字符串反推实际布局。匹配源码、配置、工具链及原厂模块 ABI 尚待定位。
