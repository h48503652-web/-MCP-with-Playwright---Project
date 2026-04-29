# 🌤️ Israel Weather MCP Server

A custom Model Context Protocol (MCP) server that empowers LLMs to fetch real-time, highly accurate localized weather forecasts for Israeli cities. 

Instead of relying on generic global APIs, this agent utilizes **Playwright** to autonomously navigate to the local Israeli weather portal ([weather2day.co.il](https://www.weather2day.co.il/)), interact with the DOM, and extract live data (RAG) directly into the chat context.

## 🎯 Project Purpose

This project explores the integration of autonomous browser control within an AI Agent architecture. 
The main learning objectives achieved are:
1. **Custom MCP Server Development:** Building a dedicated server to expose specific tools to an LLM.
2. **Browser Automation via AI:** Using Microsoft's `Playwright` to give the LLM "hands" and "eyes" on the web—allowing it to navigate, search, select from autocomplete dropdowns, and scrape data dynamically.
3. **Overcoming Language & State Barriers:** Handling stateful web interactions (waiting for animations, typing sequentially) and ensuring the LLM correctly translates queries to Hebrew before interacting with local UI elements.

## 🛠️ Technology Stack

* **MCP SDK:** The official Anthropic library for defining the protocol and exposing tools.
* **Playwright:** Modern browser automation tool used to programmatically control Chromium.
* **uv:** Ultra-fast Python package and environment manager.

## 🚀 How to Run

### 1. Prerequisites
Ensure you have `uv` installed on your system.
* **Windows (PowerShell):** `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
* **Mac/Linux:** `curl -LsSf https://astral.sh/uv/install.sh | sh`

### 2. Setup the Environment
Clone the repository, navigate to the `project-template` folder, and sync the dependencies:
```bash
uv sync
3. Install the Browser Engine
Install the Chromium browser required by Playwright:

```bash
uv run playwright install chromium
4. Start the Host
Run the interactive terminal chat to start communicating with the Agent:

```bash
uv run host.py
💬 Example Queries
Once the Host is running, you can ask the Agent questions like:

"What is the forecast in Jerusalem?"

"מה מזג האוויר בתל אביב היום?"

"Is it going to rain in Haifa tomorrow?"

Watch the magic happen: The Agent will automatically open Chromium, translate the city name to Hebrew, search for it, select the correct autocomplete option, scrape the latest forecast, and provide you with a clean, localized answer right in the terminal!

Developed by Chani Zarbiv

