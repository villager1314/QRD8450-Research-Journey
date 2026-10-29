# UPower 用户命名空间启动失败

## 现象

服务启动失败并快速重试，日志包含：

```text
Failed to set up user namespacing: Operation not permitted
Failed at step USER spawning /usr/lib/upowerd
status=217/USER
```

`start-limit-hit` 是连续失败之后的结果，定位时应查看前面的实际错误。217/USER 本身不唯一指向 user namespace。

## 本机有效的处理

在容器 root shell 执行：

```bash
mkdir -p /etc/systemd/system/upower.service.d
cat > /etc/systemd/system/upower.service.d/90-droidspaces-userns.conf <<'EOF'
[Service]
PrivateUsers=no
EOF
systemctl daemon-reload
systemctl reset-failed upower.service
systemctl restart upower.service
systemctl status upower.service --no-pager -l
```

Ubuntu GNOME、Arch KDE 与 Arch KDE Mobile 中观察到启动成功。这只关闭 UPower 的用户命名空间隔离，降低该服务的一项隔离保护，不是全局放开容器权限。

`did not recognize type Wireless` 和 object_path 断言警告仍出现，但本次没有阻止服务进入 running；设备电池信息是否完整仍未验证。

## 回滚

仅在这个文件由本实验新建时删除它，然后重载并重启 UPower；若原来已有同名配置，应恢复自己的备份。

```bash
rm /etc/systemd/system/upower.service.d/90-droidspaces-userns.conf
systemctl daemon-reload
systemctl restart upower.service
```
