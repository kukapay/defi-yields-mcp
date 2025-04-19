# DeFi Yields MCP

An MCP server for AI agents to explore DeFi yield opportunities, powered by DefiLlama.

[![Discord](https://img.shields.io/discord/1353556181251133481?cacheSeconds=3600)](https://discord.gg/aRnuu2eJ)
![GitHub License](https://img.shields.io/github/license/kukapay/defi-yields-mcp)
![Python Version](https://img.shields.io/badge/python-3.10+-blue)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

## Features

- **Data Fetching Tool**: The `get_yield_pools` tool retrieves DeFi yield pool data from the DefiLlama, allowing filtering by chain (e.g., Ethereum, Solana) or project (e.g., Lido, Aave).
- **Analysis Prompt**: The `analyze_yields` prompt generates tailored instructions for AI agents to analyze yield pool data, focusing on key metrics like APY, 30-day mean APY, and predictions.
- **Packaged for Ease**: Run the server directly with `uvx defi-yields-mcp`.

## Installation

To use the server with Claude Desktop, you can either install it automatically or manually configure the Claude Desktop configuration file.

### Option 1: Automatic Installation
Install the server for Claude Desktop:
```bash
uvx mcp install -m defi_yields_mcp --name "DeFi Yields Server"
```

### Option 2: Manual Configuration


Locate the configuration file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add the server configuration:

```json
{
 "mcpServers": {
   "defi-yields-mcp": {
     "command": "uvx",
     "args": [ "defi-yields-mcp" ]
   }
 }
}
```

Restart Claude Desktop.

## Examples

You can use commands like:

- "Fetch yield pools for the Lido project."
- "Analyze yield pools on Ethereum."
- "What are the 30-day mean APYs for Solana pools?"

The `get_yield_pools` tool fetches and filters the data, while the `analyze_yields` prompt guides the LLM to provide a detailed analysis.

### Example Output

Running the `get_yield_pools` tool with a filter for Ethereum:
```json
[
  {
    "chain": "Ethereum",
    "pool": "STETH",
    "project": "lido",
    "tvlUsd": 14804019222,
    "apy": 2.722,
    "apyMean30d": 3.00669,
    "predictions": {
        "predictedClass": "Stable/Up",
        "predictedProbability": 75,
        "binnedConfidence": 3      
    }
  },
  ...
]
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
