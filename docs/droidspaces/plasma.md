# Plasma 桌面排错

## Arch KDE：缺库和组件混用

最初 `desktop-session.service` 返回 127。实际错误为 startplasma-wayland 需要 `libPlasma.so.7`，而已安装 libplasma 6.8.0 只提供 `.so.8`。

当时 plasma-workspace 为 6.7.5，定制 KWin 为 6.8.0.r0.g066d1e17c9。更新 workspace 至 6.8.1 后启动器运行，但 plasmashell 仍 SEGV；软件渲染测试也崩溃。进一步对齐 plasma-desktop、libplasma、plasma-integration 至 6.8.1 后，观察到 plasmashell 持续运行和 Chrome 打开。

这是本次实验中的先后结果，不是完整崩溃栈证明。没有拿到 coredump。不要将不同 SONAME 强行软链接，也不要无预览地升级定制 KWin/Mesa。Arch 的局部升级可能引入其他 ABI 不一致，这次操作不是通用升级方案。

## Arch KDE Mobile：错误的 Wayland 地址

实际存在 `/run/user/1000/wayland-1`，KWin 参数也为 `--socket wayland-1`，而 systemd 用户服务环境为 `WAYLAND_DISPLAY=wayland-0`。

plasmashell 日志：

```text
Failed to create wl_display (No such file or directory)
Could not load the Qt platform plugin "wayland" ... even though it was found
```

本次 root shell 的临时修复如下。用户名、UID 和 socket 必须先确认，不能照搬到其他会话：

```bash
sudo -u Gold env   XDG_RUNTIME_DIR=/run/user/1000   DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus   bash -c '
    systemctl --user set-environment WAYLAND_DISPLAY=wayland-1
    dbus-update-activation-environment WAYLAND_DISPLAY=wayland-1
    systemctl --user reset-failed plasma-plasmashell.service
    systemctl --user restart plasma-plasmashell.service
  '
```

之后 plasmashell 启动。错误地址的写入来源及重启持久修复还未确认，不能固定所有机器都使用 wayland-1。

## 未解决

- Mobile QuickSettings.qml 反复引用 undefined 属性。
- Plasma Keyboard 6.8.1-1 的地球仪按钮灰色，语言切换原因尚未确认。
- Fcitx 的英文输入配置不等于 Plasma Keyboard 的屏幕布局配置；此前混淆两者的建议不作为有效结论。
- 巨大光标的独立原因未确认，不能简单归因于桌面外壳崩溃。
