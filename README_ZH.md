## Miside_Baby - 你的 AI 聊天伙伴

**Miside_Baby** 是一款基于 **Miside 模型** 的开源项目，旨在创建一位友好的 AI 聊天伙伴。目前处于测试阶段，欢迎您体验并提供反馈！


**特性:**

* 基于 Miside 模型，能够进行自然流畅的对话。
* 提供多种交互模式，例如文本输入和输出。
* 支持简单的问答、故事创作等基本功能。

**目标:**

*  构建一个简单、易用且令人愉快的 AI 聊天伙伴。
* 通过开源促进 AI 技术的普及和发展。


**使用说明:**

* 下载项目代码并按照 README 文件中的说明进行部署。
* 在终端运行脚本启动服务。
* 在文本框输入您的对话内容，AI 将自动回复。

**贡献指南:**

* 我们欢迎您参与项目的开发！您可以提交 bug 报告、提出新的功能请求或直接修改代码。
* 请遵守项目内的贡献指南。

**联系我们:**

* 如果您有任何问题或建议，请联系我们：[lhl2786256218@gmail.com]

**许可证:**

* 此项目根据 [MIT] 许可证授权。

**注意:** Miside_Baby 目前处于测试阶段，功能有限，可能存在一些 bug。感谢您的理解和支持！


**安装:**
* Python 3.6 or later.
  
* 由于使用了开源项目 whisper，因此可以参考 whisper 仓库进行安装   https://github.com/openai/whisper.
  
<pre><code>pip install openai-whisper</code></pre>

<pre><code>pip install setuptools-rust</code></pre>

* 如果Python自带的torch不能正常工作，请卸载后重新安装，否则请跳过此步骤。
  
<pre><code>pip uninstall torch</code></pre>

<pre><code>pip install torch</code></pre>

* 您可以通过 choco 安装 ffmpeg。如果已经安装，请跳过此步骤。
* 以管理员身份运行 PowerShell，并执行以下命令来安装 Choco。
<pre><code>Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; </code></pre>
<pre><code>iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))</code></pre>
* 使用 choco 安装 ffmpeg。
<pre><code>choco install ffmpeg</code></pre>
* 转换简体中文
<pre><code>pip install opencc</code></pre>
* 对于其他依赖环境，执行以下命令。
<pre><code>pip install -r requirements.txt</code></pre>
