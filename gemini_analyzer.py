# $language = "python3"
# $interface = "1.0"

import google.generativeai as genai
import time
import re
import os
import sys
import subprocess
import tempfile

# === CONFIGURATION ===
# IMPORTANT: Replace with your real Gemini API key
GENAI_API_KEY = "Gemini API key"
# You can change the model if you wish. gemini-1.5-flash is fast and efficient for chat.
MODEL_NAME = "gemma-3-27b-it"

# --- SCRIPT ---

try:
    genai.configure(api_key=GENAI_API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)
except Exception as e:
    crt.Dialog.MessageBox(f"Failed to initialize Gemini: {e}")
    exit()

def open_file_in_editor(filepath):
    """
    Opens a file with the default system editor (cross-platform).
    """
    try:
        if sys.platform == "win32":
            os.startfile(filepath)
        elif sys.platform == "darwin": # macOS
            subprocess.run(['open', filepath], check=True)
        else: # Linux, etc.
            subprocess.run(['xdg-open', filepath], check=True)
    except Exception as e:
        crt.Dialog.MessageBox(f"Could not open text editor. Error: {e}\n\nPlease open the file manually:\n{filepath}")

def capture_output(tab, command):
    """
    Runs a command and captures its full output using a unique delimiter.
    """
    delimiter = "d34db33f-3a2b-4a5c-8b9f-7da7a8a1b2c3"
    tab.Screen.Synchronous = True
    tab.Screen.Send(f"{command}; echo {delimiter}\n")
    if not tab.Screen.WaitForString(delimiter, 60):
        crt.Dialog.MessageBox("Error: Command timed out or delimiter not found.")
        tab.Screen.Synchronous = False
        return None
    output = tab.Screen.ReadString(delimiter)
    tab.Screen.Synchronous = False
    output = re.sub(re.escape(command.strip()), '', output, 1).strip()
    return output

def main():
    """
    Main function with improved conversational flow and a single log file per topic.
    """
    if not crt.Session.Connected:
        crt.Dialog.MessageBox("Please connect to a session before running this script.")
        return

    tab = crt.GetScriptTab()
    
    while True:
        chat = model.start_chat(history=[])
        log_filepath = None  # Will store the path to our log file for the current conversation

        action = crt.Dialog.Prompt(
            "What would you like to analyze?\n\nEnter 'command' or 'file', or 'quit' to exit.",
            "Gemini Log Analyzer"
        ).lower().strip()

        initial_prompt = ""
        
        if action == "command":
            user_command = crt.Dialog.Prompt("Enter the Linux command to execute:", "Analyze Command")
            if not user_command: continue
            output = capture_output(tab, user_command)
            if output:
                initial_prompt = f"### USER PROMPT (Command: {user_command}) ###\n{output}\n"

        elif action == "file":
            file_path = crt.Dialog.Prompt("Enter the full path to the log file:", "Analyze Log File", "/var/log/syslog")
            if not file_path: continue
            output = capture_output(tab, f"cat {file_path}")
            if output:
                initial_prompt = f"### USER PROMPT (File: {file_path}) ###\n{output}\n"

        elif action == "quit":
            break
        else:
            if action == "": break
            continue

        if initial_prompt:
            response = chat.send_message(initial_prompt)
            
            # This is the first message, so we create the log file
            with tempfile.NamedTemporaryFile(mode='w+', suffix=".txt", prefix="gemini-log-", delete=False, encoding='utf-8') as tf:
                log_filepath = tf.name
                tf.write(initial_prompt)
                tf.write("\n\n### GEMINI'S ANALYSIS ###\n")
                tf.write(response.text)
            
            open_file_in_editor(log_filepath)

            # Enter the follow-up loop
            while True:
                follow_up = crt.Dialog.Prompt(
                    "The analysis has opened in a text editor.\n\nAsk a follow-up question, type 'new' for a new topic, or 'quit' to exit.",
                    "Continue Conversation"
                ).strip()

                if follow_up.lower() == "quit":
                    action = "quit"
                    break
                if follow_up.lower() == "new":
                    break
                if not follow_up:
                    continue

                response = chat.send_message(follow_up)

                # Append the follow-up Q&A to the *same* log file
                with open(log_filepath, 'a', encoding='utf-8') as f:
                    f.write("\n\n" + ("-"*40) + "\n\n")
                    f.write(f"### USER FOLLOW-UP ###\n{follow_up}\n")
                    f.write("\n\n### GEMINI'S ANALYSIS ###\n")
                    f.write(response.text)
                
                crt.Dialog.MessageBox("Analysis appended to the log file.", "Update")
        
        if action == "quit":
            break

    crt.Dialog.MessageBox("Exiting Gemini analysis session.")

main()