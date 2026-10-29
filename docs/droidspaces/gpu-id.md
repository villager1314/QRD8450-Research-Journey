# Mesa GPU ID 实验

## 现象和判断范围

原始日志：

```text
fd_pipe_new2:49: unsupported GPU id 0x2da / chip id 0x7030000
Failed to create gbm device
```

检查实际加载库后，在该版本 GPU 匹配表中定位到 A730 记录。将两处记录的 chip ID 尾字节从 01 改为 00 后，本机 EGL 初始化成功。这是指定二进制的兼容性实验，不会修改 GPU 硬件身份或内核，也不是通用设备 ID 伪装开关。

## 已分析的文件

| 项目 | Arch | Ubuntu |
| --- | --- | --- |
| 文件 | libgallium-26.3.0-arch1.1.so | libgallium-26.3.0-devel.so |
| 字节数 | 22960040 | 28528880 |
| 第一处偏移 | 0x1579bb8 | 0x18440a8 |
| 第二处偏移 | 0x1579bd8 | 0x18440c8 |

第一条 64 位小端记录：`0x07030001 → 0x07030000`；第二条：`0xffff07030001 → 0xffff07030000`。总计仅两个字节变化。偏移不能用于其他构建。

Arch 原始 SHA-256：

```text
acae732269aabb9e08da23f6f3b19b67e74c3092065950ba3988b2bfec03b060
```

Arch 修改后 SHA-256：

```text
dbef58a4aa96543ff8d2c10b453ac81e543fcecf8aee215ff4b19194463563cd
```

Ubuntu 原始 SHA-256：

```text
698e75bcf9c155a51cb5cc5ee337f724bcaa1498db4e6fb6246edbf709ff1a94
```

Ubuntu 修改后 SHA-256：

```text
9bf99e7133ad9240009b5fbaf4ee757fc08253974500da3279a2668265a608d7
```

## Arch 脚本

从仓库根目录执行。默认只校验；不支持 Ubuntu 库。

```bash
python3 scripts/patch_arch_a730.py
sudo python3 scripts/patch_arch_a730.py --apply
```

脚本核对完整哈希、目标记录和修改结果，保留同目录 `.before-a730-patch` 备份，并原子替换目标文件。不要在包管理器更新或其他进程写驱动文件时同时运行。

恢复原始库：

```bash
sudo python3 scripts/patch_arch_a730.py --restore
```

仅接受已知补丁版本和校验正确的备份。恢复后新启动的应用会重新遇到原始不支持 ID 问题。已有进程仍可能使用旧映射，驱动修改或恢复后需要重新启动相关图形会话。

## 验证结果

```bash
EGL_PLATFORM=surfaceless eglinfo -B
```

观察到 GBM、surfaceless 与一个 device 平台报告 freedreno / FD730，OpenGL 4.6、OpenGL ES 3.2。root SSH 中没有正确图形会话环境时，X11/Wayland 初始化失败不能单独作为驱动失败结论。

这只证明设备识别和图形上下文创建。工程版 GPU 的绘制正确性、DMA-BUF 导入导出、同步和长期稳定性仍需验证。Vulkan 的 libvulkan_freedreno.so 没有修改，不能从 EGL 成功推导 Vulkan 正常。

Mesa 升级可能覆盖补丁；必须重新检查哈希，不能照旧偏移强行修改。二进制备份应保存在设备本地，不提交到此仓库。
