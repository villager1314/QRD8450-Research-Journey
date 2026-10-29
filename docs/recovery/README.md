# Recovery / TWRP 研究

状态：规划中，尚无已验证可用的 QRD8450 专用 TWRP。

## 适配前需要确认

- 实际分区布局和 A/B 槽位。
- Recovery 的启动位置及 boot/vendor_boot 结构。
- 内核、设备树、显示和触摸依赖。
- 动态分区、文件系统与数据解密支持。
- 临时启动与恢复原系统的可行路径。

后续按“构建成功、启动成功、显示、触摸、分区挂载、解密、备份恢复”分别记录。编译成功不等于可以安全刷入。

独立设备树形成后，可拆为单独 Git 仓库，在这里保留版本链接和测试历程。当前没有可下载 Recovery 镜像。

## 2026-10-29 历史核查

本轮[相关会话核查](../journal/history-evidence.md)未找到 QRD8450 专用 TWRP 设备树、构建日志、产物哈希、临时启动、触摸或解密测试输出。“规划中”表示仓库计划与当前证据不足，不能断言所有历史任务均未开展适配；云端任务尚未完成核查。

ABL 离线分析包含 `Recovery partition doesn't exist; continue normal boot`、`Booting into Recovery Mode via Boot` 等文本，只能证明有相应处理分支，不能判定本机 recovery 分区或应修改 boot / vendor_boot。见[启动层分析](../boot/README.md)。下一次需先归档分区表、镜像头和 recovery ramdisk，再记录构建及逐项实机结果。其他平台成果不计入本机进度。
