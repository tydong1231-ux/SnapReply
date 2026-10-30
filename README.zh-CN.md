# SnapReply — 微信截图 AI 回复

**不用自己开发输入法，也不用上架 App Store。** 打开微信聊天 → 轻点 iPhone 背面三下 → AI 读取当前屏幕内容 → 生成一条适合发送的中文回复 → 自动复制到剪贴板 → 在微信输入法候选栏点击粘贴，检查后自己发送。

目前是可公开分享的 **MVP 快捷指令模板**，只做截图回复这一条核心流程：**没有后台录屏，不会自动发微信，不会读到屏幕之外的聊天记录。**

**状态说明：** 源码生成和静态测试已通过；GitHub Actions 的苹果签名已经验证**失败（缺少 iCloud 登录）**，iOS 26.2 真机运行仍需实际验证，不能把静态测试当成安装成功。

## 只用 iPhone 安装（推荐）

**无需 Mac、Python、签名或开发者账号**：在 iPhone 自带「快捷指令」App 里创建同等流程，详见 [iPhone 一步步教程](docs/iphone-setup.zh-CN.md)。这是完全手机端的方案；首次需要手动添加动作。GitHub 自动构建生成的未签名文件仍然不能直接导入 iPhone。

## 从 GitHub 文件安装：在自己的 Mac 签名

GitHub Actions 只负责生成和检查 **未签名开发模板**，不能直接在 iPhone 导入。我们已实测 GitHub 的临时 Mac 因未登录 iCloud 而被苹果拒绝签名。因此请在自己的已登录 iCloud 的 Mac 上使用下方一键脚本，生成可安装的 `SnapReply.shortcut`。导入到 iPhone 后，设置：
   - Base URL：`https://api.openai.com/v1`（不能多写尾部斜杠，也不用加 `/chat/completions`）
   - API Key：你自己的私密 Key（**只能在自己的设备上输入**）
   - Model：默认 `gpt-5.4-mini`（支持图片的 OpenAI 兼容模型）
1. 如果导入时没出现以上问题，请进入快捷指令编辑页面，修改最前面的三个「文本」动作。
2. 先用没有客户隐私的假聊天测试。iPhone「设置 → 辅助功能 → 触控 → 轻点背面 → 轻点三下 → SnapReply」。有操作按钮的机型也可以绑定。

GitHub Actions 可以下载未签名模板做开发调试，但不能直接安装；必须先通过 macOS 的快捷指令 CLI 签名。

## Mac 本地签名（备用）

在 Mac「终端」执行：

```sh
git clone https://github.com/tydong1231-ux/SnapReply.git
cd SnapReply
zsh scripts/sign-on-mac.sh
```

输出文件在 `dist/SnapReply.shortcut`，AirDrop 到手机安装即可。无需付费 Apple Developer 账号。

## 功能和限制

| 功能 | 当前版本 |
| --- | --- |
| 微信当前画面自动截图 | ✅ |
| GPT-5.4 mini 视觉识别并写回复 | ✅ 代码已实现，待真机验收 |
| 自定义 Base URL / Key / Model | ✅ |
| 回复自动复制到剪贴板 | ✅ 代码已实现 |
| 微信输入法快速粘贴 | ✅ 或长按输入框粘贴，视输入法设置而定 |
| 直接读微信数据库 / 历史消息 | ❌ |
| 自动发消息 | ❌ |
| 相册品牌自动分类、图片回复 | ❌ 后续功能 |

AI 生成内容由你自己检查。没有确切依据时不会编造价格、库存、物流、折扣和付款状态。只看到**当前一屏**，不能自动读取隐藏的历史聊天。第一版请求使用 **图片 detail=high** 来增加小字识别精度，但会影响输入 token 费用。

## 安全特别提醒

- 每次会将当前**整张屏幕截图**经 HTTPS 发送给所填的 API 提供商；截图上的联系人、地址、电话号码、付款信息也会被传出。不要在包含敏感信息的画面使用。
- API Key 存在个人快捷指令中的明文「文本」动作中，**不要把填过真实 Key 的快捷指令公开上传到 GitHub 或分享给别人**。建议为它专门创建低额度 Key。
- 不要用不可信的 Base URL。对方服务器可以得到你的截图和 API Key。
- 剪贴板属于系统共享内容；回复文本可能被获得剪贴板读取权限的 App 访问。
- GitHub 上的公开版本只包含空白 Key 模板，项目不收集用户数据，不依赖自己的中转服务器。

代码结构见 [英文 README](README.md) 和 [安全说明](SECURITY.md)。仓库沿用已有的 **Apache 2.0** 开源许可证。本项目参考 [Relay](https://github.com/rishiv7/relay) 的交互思路，**没有复制其无许可证的代码/已签名文件**。
