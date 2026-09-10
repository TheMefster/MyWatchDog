<h1>About MyWatchDog</h1>
MyWatchDog is a free, open-source application designed to block unwanted or distracting content. It is not a perfect or complete solution. MyWatchDog <i> does not</i> catch everything. But it will hopefully prove to be helpful in getting back the time we all loose to the internet.

<h3>License Agreement</h3>
See LICENSE for the full license agreement. In short, the software is completely free to use, modify, and distribute (etc.); however, MyWatchDog Co. is in no way responsible for any claims/damages related to the software in any way <i>(NOTICE: this summary is not legally binding: you must read the full license agreement before usage)</i>.

<h3>Privacy Policy</h3>
It's the 21st century. If you think your privacy is still a thing, I envy your innocent ignorance. That being said, MyWatchDog Co. does not collect any personal information or data from your computer in any way. Any data needed to run the program is stored only on your device and is never uploaded anywhere on the internet. That being said, MyWatchDog is powered by a few different external dependencies, each of which have their own license and privacy policy <i>(a full list of dependencies can be found under LICENSES -> LIB-LICENSES)</i>. MyWatchDog is not affiliated with or responsible for the actions of these dependencies. While it is unlikely that these dependencies collect your data, it is highly recommended to read through their licenses and policies for more information.

<h1>User Guide</h1>
MyWatchDog is intended to be as simple as possible, regardless of technological knowledge. Keep in mind that, while the program can technically run on any device, MyWatchDog is designed for Windows and macOS, with limited support for Linux. It is not recommended to attempt to run this program on any other hardware. Additionally, Linux setup and execution can be difficult for users who are not familiar with the command line. If you have no experience in programming, it is recommended to use Windows or macOS rather than Linux.

<h3>Setting Up</h3>
<li>To run MyWatchDog, simply download the <a href="https://github.com/TheMefster/MyWatchDog/releases">applicable release</a>, then extract the file to the desired location and open the application. Please noted that the application itself is located inside of the "MyWatchDog" folder. GetCode is a different application <i>(explained in Custom Blocking)</i>.</li>
<li>On Windows devices, MyWatchDog will automatically run on login once the program has been opened once. On macOS, you can set this up yourself by opening System Settings, clicking the "General" tab, opening the "Login Items" menu, and adding MyWatchDog under the "Open at Login" section. Each Linux distribution is different, but the typical setup uses the systemd or crontab commands.</li>
<li>MyWatchDog will apply settings changes automatically on Windows and macOS. On Linux, the filter is hosted as a proxy on localhost port 6692. You will need to manually install the mitmproxy certificate (found under ~/.mitmproxy), then manually set the proxy to localhost port 6692 on your browser of choice.</li>

<h3>Custom Blocking</h3>
<li>By default, MyWatchDog blocks a variety of inappropriate keywords and websites. However, additional custom keywords, websites, and applications can be blocked using the block.xxx file.</li>
<li><b>Editing block.xxx:</b> block.xxx is located in the user's default folder <i>(C:\Users\username on Windows; HOME folder on macOS)</i>. Once this file has been created, MyWatchDog will prevent any changes to the file to ensure the blocklist is not easily overridden. To edit the blocklist, it is suggested to create the file "toblock.txt" in the same folder. You can create/edit this file using Notepad on Windows or TextEdit on macOS. To apply the changes, you must paste a 36-digit code at the top of "toblock.txt". Note that this code is generated using the "GetCode" application in the same directory as the MyWatchDog folder <i>(see Setting Up)</i>. These codes are only valid during the same hour in which the code was generated, and codes generated on the same device as the program will not be effective - <b>you must get the code from another person</b> in order to update the blocklist file.</li>
<li>When making changes to block.xxx, each new line is considered its own block command. Whatever keyword is listed on that line will be blocked. These keywords are not case sensitive <i>("MAGIC" is the same as "magic")</i>, but they are context sensitive <i>("magic trick" is not the same as "trick magic")</i>.</li>
<li>By default, block commands are applied to <b>only</b> to urls <i>(e.g. google.com)</i>. To block a keyword, begin the line with '#' followed by the keyword. To block an application, use '@' followed by the application name.</li>
<li>
  <b>Advanced Blocking:</b> use the ` character <i>(usually found on the top left of the keyboard)</i> to apply more advanced filtering to the keywords <i>(not compatible with applications or urls)</i>. 
  <ul>
    <li>After using the ` character once <i>(#keyword`____)</i>, enter a specific hour of the day or day of the week <b>to two digits</b> to apply the filter only at that specific time and day. For example, "#magic`14" would block the keyword "magic" from 2PM (14:00) until 2:59. Multiple hours/days can be specified, seperated by spaces: "#youtube`Mo Tu We Th Fr" would block the keyword "youtube" on any weekdays. If both a day and a time are specified, the filter is exclusive: "#polar bear`12 13 14 Mo Tu" will block the keyword "polar bear" only on Monday and Tuesday from 12-3PM. To block a keyword on both certain days and at certain times, create two different block commands for the same keyword.</li>
    <li>After using the ` character twice <i>(#keyword``____)</i>, enter a number to specify the severity of a certain keyword. Each time a keyword appears in a website, the severity of the website will increase by the severity of the keyword. The website is blocked only once its severity reaches over 100. By default, a keyword has a severity of 50.</li>
    <li>You can specify both the time/date and the severity of a keyword in one command <i>(#keyword`time`sev)</i>.</li>
  </ul>
</li>

<h3>Uninstalling</h3>
MyWatchDog is intentionally difficult to uninstall. If you absolutely need to uninstall the program, first stop all current running instances using Task Manager on Windows, Activity Monitor on macOS, or System Monitor on Linux. You will also need to stop all running instances of MS Powershell, which is usually labeled "pwsh". If you have set the program to run automatically, you will also need to disable it in settings (on with command line on Linux). Finally, remove the filter by turning off the proxy: disable Settings -> Network & Internet -> Proxy -> Use a Proxy Server on Windows, or remove the "http_proxy" and "https_proxy" environment variables on macOS. After doing these things, you can safely delete the MyWatchDog folder and block lists.

<h3>Common Issues</h3>
<h5>Network Error: Proxy is not configured correctly</h5>
Try restarting MyWatchDog by opening the application again, or by restarting your computer.
<h5>Error: Access to mitmproxy_rc is denied (Windows-Specific)</h5>
Open Windows Security and disable App & browser control -> Smart App Control
<h5>MyWatchDog is blocking sites it shouldn't block!</h5>
Firstly, check to see if the site is blocked by a custom keyword. Some words appear in places you wouldn't expect; for example, "#verb" will block any instance of the word "hoverboard". If you can find an alternative site that is not blocked, try using that. If you cannot find a replacement and it is blocked by the program itself, you can use an advanced command with a negative value for a keyword on that particular site <i>(see Advanced Blocking)</i>. For example, adding "#kellogg``-100" will most likely unblock wkkellogg.com.
<h5>My Watchdog isn't blocking sites is should block!</h5>
If you think a specific site should be blocked for everyone, please email me at dimensional0coder@gmail.com. If a specific url should be blocked for you specifically and it seems to not be working, try finding a particular keyword unique to that page (or similar pages) and adding that to the custom blocklist. 


<h3>Note: on YouTube Shorts</h3>
The youtube.com/shorts domain is blocked by default on MyWatchDog, with the intent of helping you fight the urge to doomscroll. If you truly need to watch a specific short, change the url as follows [www.youtube.com/shorts/XXXXXXXXXXX -> www.youtube.com/watch?v=XXXXXXXXXXX]
