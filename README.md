[中文](https://github.com/2786256218/Miside_baby/blob/main/README_ZH.md)
## Miside_Baby - Your AI Chat Companion

**Prepare:**
* Go to Volcano Cloud platform to register an account  https://console.volcengine.com/auth/login?redirectURI=%2Fhome
<img width="1269" alt="1" src="https://github.com/user-attachments/assets/602da30e-8d48-4b22-a11b-63c486a4f1eb" />

* After completion, enter the console  https://console.volcengine.com/speech/app
<img width="1275" alt="2" src="https://github.com/user-attachments/assets/514f025e-7052-489b-8d1b-d0e658acd81c" />

* Activate the service and copy your key and token to the source code. Initially, only two tones are given. Other free tones can be purchased on the purchase page.
![3](https://github.com/user-attachments/assets/f3973446-2f07-4680-a294-2909d021d984)


**Miside_Baby** is an open-source project built on the **Models in ollama**, aiming to create a friendly AI chat companion. Currently in the testing phase, we welcome you to experience it and provide feedback!

**Features:**

* Based on the Models in ollama, capable of engaging in natural and fluent conversations.
* Offers multiple interaction modes, such as text input and output.
* Supports simple question answering, story creation, and other basic functionalities.

**Goals:**

* To build a simple, user-friendly, and enjoyable AI chat companion.

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
* Install ollama:https://ollama.com/
* The gemma2 model is used by default
* Since whisper is used as the ASR for this project, you can go to the whisper repository to view detailed information https://github.com/openai/whisper. If you think whisper is too slow, you can replace it with other online ASRs such as Seed-ASR or Baidu ASR  .
  
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


**Replenish**
* First of all, thanks to Xlmy, the provider of misside 3D animation.
* Currently, the models and animations of Miside are quite scarce. Since I have not learned 3D animation production, I cannot make other animations. If any friends are willing to provide materials, please send them to my email lhl2786256218@gmail.com. I will add new animations and functions in the next version update.
* Thanks to everyone who helped with this project
* The voice function is used in the command line, s to record, q to pause