# GPTeeee - Giving ChatGPT read/write/execute to ubuntu

This ChatGPT plugin allows users to interact with the local file system and execute shell commands. The plugin provides a set of API endpoints to perform various operations like running shell commands, listing files, reading, creating, updating, and deleting files.

## Features

- Run shell commands with optional stdout and stderr capture, and customizable timeout.
- List files in a specified directory with optional regular expression filtering and limit.
- Read, create, update, and delete files.
- Serve the plugin logo and manifest file for easy integration with ChatGPT.

## Setup

To install the required packages for this plugin, run the following command:

    docker build -t gpteeee .

Then, to run the plugin, enter the following command:

    docker run -p 5003:5003 gpteeee

Once the local server is running:

- Navigate to https://chat.openai.com.
- In the Model drop-down, select "Plugins" (note, if you don't see it there, you don't have access yet).
- Select "Plugin store."
- Select "Develop your own plugin."
- Enter localhost:5003 since this is the URL the server is running on locally, then select "Find manifest file."
- The plugin should now be installed and enabled! You can start with a question like "List all files in the current directory" or "Run the command 'ls'."

## Why use this plugin?

This plugin offers several advantages for users who want to explore interactively building systems with ChatGPT:

- Running the plugin inside a Docker container provides a level of isolation and protection, although using a more secure sandboxing solution like Firecracker VM is worth considering for enhanced security.
- The interactive nature of ChatGPT enables users to perform file management and command execution tasks in a conversational manner, making it a more intuitive experience.
- Currently, this plugin lacks the ability to persist changes using volumes; however, adding this feature could significantly improve its usefulness by allowing users to save and manage their work more effectively.
- It's important to note the potential risks of using an LLM like ChatGPT to run commands, as it may not always produce the desired output or understand the implications of executing certain commands. Users should exercise caution and verify the suggested commands before executing them in a sensitive environment.
