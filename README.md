# Google-Dorking-Tool
Building a fully functioning web rendering engine (like Chrome or Firefox) from scratch using only Tkinter is virtually impossible, as Tkinter doesn't natively support rendering modern HTML/JS/CSS.

However, we can build exactly what you're asking for: a "Smart Search" GUI tool using Tkinter. This tool will act as the "brain" to construct advanced Google Dorking queries (specifically focusing on the filetype: operator) and then dispatch those highly targeted searches to your system's default web browser to display the results.

Here is the complete, runnable Python code to create your Smart Dorking Search Tool.

**Prerequisites**
This script uses Python's standard libraries, so you shouldn't need to pip install anything.

**How This Tool Works Behind the Scenes**

The GUI (Tkinter): It provides a clean, user-friendly interface. Instead of forcing you to remember the exact syntax for Google operators, it uses dropdowns and text fields to gather your intent.

The Dork Compiler: When you click "Execute", the script strings together standard Google Search Operators:

"" (Exact Match): It wraps your keyword in quotes to ensure Google looks for that specific phrase.

filetype:ext: This operator forces Google to only return indexed files matching that exact extension (e.g., skipping HTML web pages and only giving you direct downloads to .pdf or .csv files).

site:domain: This optional addition restricts the search to a specific top-level domain (like .edu for universities) or a specific website.

The Dispatcher (webbrowser): The urllib.parse library encodes spaces and special characters into a valid URL string, which is then passed to Python's built-in webbrowser module, securely opening your results in your default browser.
Window Geometry: Increased the window size from "450x300" to "450x350" to make room for the new dropdown.

Browser Dictionary: Added self.browsers which maps user-friendly names (like "Google Chrome") to the specific string keywords the webbrowser library looks for (like "chrome"). "System Default" is mapped to None.

Targeted Dispatch: In execute_search(), it checks if a specific browser was requested. If yes, it uses webbrowser.get('browser_name').open(url).

Graceful Fallback: I added an inner try/except block catching webbrowser.Error. If a user selects "Safari" on a Windows machine, the code won't crash; it will pop up a warning letting them know the browser wasn't found and will seamlessly failover to their default browser.
