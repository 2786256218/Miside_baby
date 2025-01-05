[中文](https://github.com/2786256218/Miside_baby/blob/main/README_ZH.md)
## Miside_Baby - Your AI Chat Companion

**Miside_Baby** is an open-source project built on the **Miside model**, aiming to create a friendly AI chat companion. Currently in the testing phase, we welcome you to experience it and provide feedback!

**Features:**

* Based on the Miside model, capable of engaging in natural and fluent conversations.
* Offers multiple interaction modes, such as text input and output.
* Supports simple question answering, story creation, and other basic functionalities.

**Goals:**

* To build a simple, user-friendly, and enjoyable AI chat companion.
* To promote the popularization and development of AI technology through open-source.

**Usage Instructions:**

* Download the project code and follow the instructions in the README file for deployment.
* Run the script in the terminal to start the service.
* Input your conversation content in the text box, and the AI will respond automatically.

**Contribution Guidelines:**

* We welcome you to participate in the project's development! You can submit bug reports, propose new feature requests, or directly modify the code.
* Please adhere to the contribution guidelines within the project.

**Contact Us:**

* If you have any questions or suggestions, please contact us at [lhl2786256218@gmail.com].

**License:**

* This project is licensed under the [MIT] license.



**Note:** Miside_Baby is currently in the testing phase with limited functionalities and may contain some bugs. Thank you for your understanding and support!


**Setup:**
* Python 3.6 or later.
  
* Since the open source project whisper is used, you can refer to the whisper repository to install it   https://github.com/openai/whisper.
  
<pre><code>pip install openai-whisper</code></pre>

<pre><code>pip install setuptools-rust</code></pre>

* If the torch that comes with Python does not work properly, please uninstall and reinstall it, otherwise please skip this step.
  
<pre><code>pip uninstall torch</code></pre>

<pre><code>pip install torch</code></pre>

* You can install ffmpeg via choco. If it is already installed, please skip this step.
* Run PowerShell as an administrator and execute the following command to install Choco.
<pre><code>Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; </code></pre>
<pre><code>iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))</code></pre>
* Install ffmpeg using choco.
<pre><code>choco install ffmpeg</code></pre>
* Convert Simplified Chinese
<pre><code>pip install opencc</code></pre>
* For other dependent environments, execute the following commands.
<pre><code>pip install -r requirements.txt</code></pre>

