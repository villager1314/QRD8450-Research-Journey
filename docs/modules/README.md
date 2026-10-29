# 模块与注入研究

本方向关注模块加载条件、KernelSU 集成方式和用户空间注入的实现与兼容性。

## 分开记录的层次

| 层次 | 研究内容 |
| --- | --- |
| 内核模块 | vermagic、符号版本、内核配置和加载权限 |
| Root 框架 | KernelSU 的集成方式及用户空间管理 |
| 用户空间注入 | Zygisk 等框架的适用进程和生命周期 |

LKM、Root 框架与应用进程注入不是同一层的功能。不能用“模块可以加载”推导“所有模块都兼容”。

## 已归档与剩余缺口

- 下文已归档部分模块元数据、DWARF 比较和加载失败日志；完整内核配置仍待补齐。
- 模块公开来源、版本与具体样本哈希之间的对应关系仍需核对。
- 新增启动日志证据见下文；卸载、重启持久性与长期稳定性仍未验证。

本页已补充部分离线布局与日志证据；仓库不附带模块二进制。

## 2026-10-23 历史补录

来源见[会话证据索引](../journal/history-evidence.md)。本轮没有重新加载模块。

### 离线分析

| 样本 | 历史编译标识 | 结论范围 |
| --- | --- | --- |
| `DroidSpaces-LKM.zip` 内 `droid-lkm.ko` | `6.1.166-dirty` | 容器功能 shim，与本机 5.10.81 明显不匹配 |
| `droid_lkm-android13-5.10.zip` 内 `droid_lkm.ko` | `5.10.245` | 有 BTF / 布局解析函数和日志线索 |
| 桌面附件 `lkm4ctr.ko` | `5.10.252-dirty` | 有命名空间、IPC、OverlayFS、诊断线索；未确认动态字段布局修正 |

首个包当时只有 KO、`module.prop`、`service.sh`，脚本用 `insmod` 加载 KO；未证明包已安装，也未证明可提供 Gunyah VM 管理能力。

历史 DWARF 工具输出中，后两个 KO 抽查字段的编译时偏移一致，单位为十进制字节：

| 字段 | 两个 KO 的偏移 |
| --- | ---: |
| `task_struct.mm` | 1304 |
| `task_struct.pid` / `tgid` | 1480 / 1484 |
| `task_struct.cred` / `nsproxy` | 1920 / 2000 |
| `nsproxy.ipc_ns` / `pid_ns_for_children` | 16 / 32 |
| `cred.user_ns` | 136 |
| `pid_namespace.child_reaper` | 56 |
| `ipc_namespace.user_ns` | 952 |
| `file.private_data` | 216 |

这不是本机运行内核的布局表，也未覆盖全部字段。历史分析最终纠正：虽有 `modversions` 标识，两者实际 `__versions` 段均为空，没有可比较的符号 CRC 表。

`droid_lkm` 可见 `btf_open`、`droid_lkm_layout_init`、`droid_lkm_layout_off` 等符号。结合日志推测会解析 BTF 并建立运行时布局，完整控制流与覆盖范围未还原。历史记录称未发现 `/sys/kernel/btf/vmlinux`，这不能排除内存 BTF 路径；`__start_BTF` / `__stop_BTF` 线索也不能证明本机可解析。

`lkm4ctr` 的 `shadow_hook_resolve`、`vns_compat_resolve` 名称不能证明会修正字段偏移。附件样本不能与实机另一个 `lkm4ctr-4.0.5-android12-5.10-arm64.ko` 混为同一构建。

### 实机加载失败

用户执行 `insmod /data/local/tmp/droid_lkm.ko` 返回 `No such file or directory`。随后 `ls -l` 确认文件存在，大小 9,384,544 字节、权限 644。历史工具读取日志得到：

```text
[6736.884698] droid_lkm: Unknown symbol init_user_ns (err -2)
```

用户随后回传 `/proc/kallsyms` 中存在 `init_user_ns`，但搜索对应 `__ksymtab_` / `__kstrtab_` 条目无输出。证据支持“符号存在但模块无法解析，疑似未导出”；最终仍应核对匹配源码或 `Module.symvers`。

阻断发生在符号解析，尚未验证 BTF、布局、hook 或容器功能。不能归因于文件不存在或缺少 755 权限。没有找到本会话中 lkm4ctr 成功加载、卸载或重启持久性的证据。

### KernelSU 与用户空间注入

历史日志原始工具输出还出现：

```text
[6643.562625] KernelSU: handle_setresuid from 0 to 10037
```

可确认这次内核日志带有 KernelSU 运行线索，但版本、集成方式和管理器状态仍不明。本轮未找到 Zygisk 等用户空间注入成功记录。root shell 本身及包内 `module.prop` / `service.sh` 均不足以证明具体框架与安装状态。

## 2026-10-29：原始启动日志复核与布局审计缺口

本轮直接读取 `D:/workspace/UotanToolbox/Bin/platform-tools/lkm4ctr-debug-3.txt`，SHA-256 为 `9a2ddf88d0eb1f5e290c15d92e15a3614211fe45af89329b153d8dedde4bdde0`。以下是原文行号与关键输出：

| 原文行号 | 证据 |
| --- | --- |
| 843 | `[5.157856] ... /data/adb/ksud services ... exited with status 0` |
| 1320 | `[9.304970] KernelSU: on_boot_completed!` |
| 1325 | `[9.344815] ... /data/adb/ksud boot-completed ... exited with status 0` |

可确认此日志记录了 KernelSU boot-completed 回调，以及这两次 ksud 调用正常退出。不能外推所有 ksud 工作均成功、lkm4ctr 成功加载或长期稳定。日志时间是启动后的相对秒数，不作为实验日期。

同一原始日志另有 lkm4ctr 自身的初始化输出：行 3603 为 `[296.350659] ... loaded (34 hook(s) installed)`，行 3609 为 `[296.369880] ... loaded unified module`；这些是模块自报的初始化线索，独立于 KernelSU 的启动记录。行 3605 同时报告 `mkdir(/dev/mqueue) failed: -13`。当前没有与该次日志绑定的 KO 哈希、完整功能验收或长期稳定性证据，不能把初始化文本写成完整兼容验证。

此前提到的 `QRD8450_lkm4ctr_layout_audit.md` 原文未找到，因此本轮不能核实“模块与原厂内核指令交叉核对的部分字段一致”的具体字段、偏移、指令地址或样本对应关系；不从摘要补造表格。前文两个 KO 的 DWARF 比较也不能替代原厂内核指令交叉核对。

即使后续找到审计并确认部分字段一致，也只能支持所核验字段，不能证明整个模块兼容，不能解释延迟卡死的唯一根因。卡死原因仍需与同次样本、时间线、故障日志及控制实验对应。来源与缺口见[REFERENCES](../../REFERENCES.md)。
