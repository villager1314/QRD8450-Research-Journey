# Windows SSH 别名

多个容器轮流使用同一宿主端口时，可以用独立 HostKeyAlias 保存各自的主机密钥。别名不会自动启动容器，也不会改变端口转发。

Windows `%USERPROFILE%\.ssh\config` 示例：

```sshconfig
Host archkdemobile
    HostName YOUR_PHONE_IP
    Port 2222
    User Gold
    HostKeyAlias droidspace-archkdemobile
```

本次使用 NAT 转发：宿主 TCP 2222 → 容器 TCP 22。其他容器可以添加自己的 Host 和 HostKeyAlias。

首次连接应核对新容器指纹。重装同一容器后，别名下的密钥也可能变化，不应无条件绕过主机密钥验证。
