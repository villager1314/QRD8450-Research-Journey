# 研究历程

本记录依据命令输出与实验过程整理，未保留的细节不补写为事实。时间使用中国标准时间；宿主和容器日志可能相差 8 小时，关联事件时须核对。

## 2026-10-28：GPU 与桌面探索

1. 读取设备树与 SoC 信息，识别 Waipio QRD。
2. 定位 Mesa `unsupported GPU id 0x2da / chip id 0x7030000`。
3. 验证实际加载的 Gallium 库；包管理器版本不一定等于运行时库版本。
4. 在指定 Ubuntu、Arch 库中修改两条 GPU 匹配记录，EGL 测试报告 FD730。
5. Ubuntu GNOME 的 UPower user namespace 问题得到单服务配置修复。
6. Arch Denial 能启动但交互异常；进行了渲染后端、线程 CPU 与调度对照，尚未得到稳定解决方案。

## 2026-10-29：KDE 与 KDE Mobile

1. 新容器的 Arch Gallium 哈希与已分析版本一致，重复补丁后 GPU 初始化成功。
2. Arch KDE 的启动 127 定位到 libPlasma SONAME 不匹配。
3. 调整部分 Plasma 组件版本后，plasmashell 和 Chrome 被观察到运行。
4. Arch KDE Mobile 再次修复 UPower。
5. 发现实际 socket wayland-1 与用户服务环境 wayland-0 不一致，临时调整后 Mobile 外壳启动。
6. 快捷设置 QML 报错与 Plasma Keyboard 地球仪灰色仍待研究。
7. 建立研究仓库，分出启动层、容器、模块和 Recovery 方向。

## 下一步

- 找到 WAYLAND_DISPLAY 的错误注入来源，验证重启持久性。
- 将 GPU 上下文测试扩展为实际绘制、DMA-BUF 共享及稳定性验证。
- 独立调查 Mobile 快捷设置与键盘配置。
- 补齐启动层和模块的剩余证据、Recovery 只读采集；已有 Boot 样本、布局与日志见对应补录。

## 2026-10-29：历史会话补录

复核 10 月 23 日相关会话，补充 ABL/UEFI 离线分析、Gunyah 厂商 VM 路径、模块布局比较、`init_user_ns` 加载失败及 KernelSU 日志线索。TWRP 尚缺构建与启动证据，云端任务未完成核查。详见[证据索引与检索边界](history-evidence.md)。

## 2026-10-29：原始材料补查

- 直接核验指定 `boot_a.img` 为 header v4，记录样本路径、大小和哈希；不外推到当前运行 Boot 或未找到的审计样本。见[启动层](../boot/README.md)。
- 直接复核 `lkm4ctr-debug-3.txt`，确认 `KernelSU: on_boot_completed!` 及两次 ksud 状态 0 退出；另记录模块自报初始化和 mqueue 错误，未据此认定完整兼容或长期稳定。见[模块研究](../modules/README.md)。
- 未找到 `QRD8450_lkm4ctr_layout_audit.md`，部分字段与原厂内核指令交叉核对的结论尚不能复核；不根据摘要补造字段。即便部分一致，也不能证明整模块兼容或唯一定位延迟卡死原因。
- [REFERENCES](../../REFERENCES.md)记录原始材料及检索缺口；[PUSH](../../PUSH.md)补充现有远程仓库的 clone 与日常提交推送方法。本轮未提交或推送。
