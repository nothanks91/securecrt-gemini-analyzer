# securecrt-gemini-analyzer
AI-powered troubleshooting assistant for SecureCRT using Google Gemini
This Python script integrates Google's Gemini AI directly into your SecureCRT workflow, allowing you to analyze remote command outputs and log files through a conversational AI interface. It is designed to be safe, easy to use, and to keep a persistent record of your analysis sessions.
Features

    Interactive AI Analysis: Send command output or log files directly to Gemini for troubleshooting, explanation, or analysis.
    Analyze Remote Data: Works seamlessly with your live SSH sessions to capture output from any Linux command or read entire log files.
    Conversational Context: The script maintains a chat session, allowing you to ask multiple follow-up questions about an initial piece of data.
    Persistent Chat Logs: Each conversation is automatically saved to its own dedicated text file on your local machine, creating a complete record of your analysis.
    Safe Output Handling: All AI responses are displayed in your local text editor, not printed to the live terminal, preventing any risk of accidental command execution.
    Cross-Platform Compatibility: The script automatically uses the default text editor on Windows, macOS, or Linux to display the chat logs.
    User-Friendly Workflow: A simple, prompt-driven interface allows you to start new analyses, ask follow-up questions, or quit the session easily.

Requirements

    VanDyke SecureCRT version 8.0 or newer.
    An active session (e.g., an SSH connection) in SecureCRT.
    A Google Cloud account with the "Vertex AI API" or "Generative Language API" enabled.
    A Gemini API Key from Google AI Studio.

Installation and Configuration on Windows

Follow these steps to set up the script.
Step 1: Get Your Gemini API Key

    Go to Google AI Studio.
    Sign in with your Google account.
    Click "Create API key".
    Copy the generated key and save it somewhere safe. You will need it in the next step.

Step 2: Save and Configure the Script File

    Download gemini_analyzer.py file.

    Crucially, you must add your API key to the script:
        Open the gemini_analyzer.py file you just saved.
        Find this line near the top:
        Python

        GENAI_API_KEY = "YOUR_GEMINI_API_KEY"

        Replace the text YOUR_GEMINI_API_KEY with the actual key you copied from Google AI Studio. Make sure to keep the quotation marks.
        Save the file.

Step 3: (Recommended) Create a Button in SecureCRT

For easy access, you can map the script to a button on SecureCRT's button bar.

    In SecureCRT, go to the View menu and make sure Button Bar is checked.
    Right-click on an empty spot on the Button Bar and select New Button.
    In the dialog box that appears:
        In the Function dropdown menu, select Run Script.
        In the Script File field, click the ... button to browse to and select your gemini_analyzer.py file.
        In the Label field, give the button a name, like Gemini AI.
        Click OK.

You will now have a "Gemini AI" button on your toolbar.
How to Use the Script

    Launch the Script:
        Connect to a server in SecureCRT.
        Click the Gemini AI button you created, or run the script from the menu via Script > Run....

    Start a New Analysis:
        A dialog box will appear asking what you want to analyze.
        Type command or file and click OK.

    Provide Your Input:
        If you chose command, you will be prompted to enter a Linux command (e.g., dmesg | tail -n 20 or sudo journalctl -u sshd -n 10).
        If you chose file, you will be prompted for the full path to a file on the remote server (e.g., /var/log/syslog or ~/.bash_history).

    View the Initial Analysis:
        The script will run, capture the data, and send it to Gemini.
        A new text file will automatically open in your default editor (Notepad). This file is the "Chat Log" for your current conversation and contains Gemini's initial analysis.

    Continue the Conversation:
        Switch back to SecureCRT. A new dialog box will be waiting, asking for a follow-up question.
        Type any question about the analysis you just received (e.g., "What does that error code mean?" or "Explain the first warning in more detail.").
        A small confirmation box will appear saying "Analysis appended to the log file."
        Switch back to your open text editor. The new question and Gemini's answer will be at the bottom of the file. You can repeat this step as many times as you like.

    Start a New Topic or Quit:
        To start over with a new command or file, type new in the follow-up prompt. This will close the current conversation and take you back to the main menu. A new, separate log file will be created for your next topic.
        To end the session, type quit in any prompt.
