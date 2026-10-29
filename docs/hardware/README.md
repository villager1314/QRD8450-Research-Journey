# 设备信息

以下数据来自本机命令输出。

| 项目 | 观察值 |
| --- | --- |
| 设备称呼 | QRD8450 |
| ro.product.board | taro |
| device-tree model | Qualcomm Technologies, Inc. Waipio QRD with PM8010 |
| compatible | qcom,waipio-qrd / qcom,waipio / qcom,qrd |
| soc_id | 457 |
| machine / family / revision | WAIPIO / Snapdragon / 1.0 |
| 原厂系统 | Android 12 userdebug |
| 内核 | 5.10.81-android12-9-g7181a15d6d4b |
| Mesa GPU / chip ID | 0x2da / 0x07030000 |

GPU ID 的十进制值为 730。匹配表补丁后 Mesa 将其报告为 FD730；这不证明工程版 GPU 与量产版在所有硬件细节上相同。

普通 shell 读取设备树 model 曾被拒绝，切换 root 后成功。设备标识、序列号和网络地址不作为公开记录的必要内容。
