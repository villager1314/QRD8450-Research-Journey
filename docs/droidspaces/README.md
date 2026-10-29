# Droidspaces 实验

本组实验运行在 QRD8450 的 Android 12 / 5.10.81 内核上，Linux 容器共享宿主内核，不应与其他手机上的 AVF 实验混写。

| 项目 | 记录 |
| --- | --- |
| Droidspaces | v7.0.0 |
| Anland consumer | 5.21-c66310b，versionCode 364 |
| Linux GPU 节点 | /dev/kgsl-3d0、/dev/dri/renderD128 |
| GPU 访问组 | droidspaces-gpu |
| 环境 | MESA_LOADER_DRIVER_OVERRIDE=kgsl、GALLIUM_DRIVER=kgsl |

- [Mesa GPU ID 兼容性实验](gpu-id.md)
- [UPower 用户命名空间修复](upower.md)
- [Plasma 组件和 Wayland 环境排错](plasma.md)
- [SSH 容器别名](ssh.md)

## Denial 实验结果

GPU 初始化恢复后仍存在桌面区域交互卡顿、输入会话重建和 DMA-BUF 导入失败。出现过 EGL_BAD_ALLOC、MissingAuthorization、冷场景恢复超时及桌面进程 ABRT。

鼠标在 Settings 内容区较流畅，在桌面背景区域较卡。固定时长对照中，卡顿的桌面区域反而 CPU 使用率、调度排队等待更低；没有足够证据把问题归因于单核跑满或 WALT。软件栈、帧提交和输入恢复链路仍需分析。

切换 Skia、offscreen blit、绑定可用大核和安卓性能模式均未形成有效修复。不能把这些试验写成推荐配置。
