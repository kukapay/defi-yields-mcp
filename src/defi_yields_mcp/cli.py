import asyncio
from typing import List, Dict, Any
from mcp.server.fastmcp import FastMCP, Context
import httpx

# Initialize the MCP server
mcp = FastMCP("DeFi Yields Server")

# Tool to fetch and filter yield pools
@mcp.tool()
async def get_yield_pools(chain: str = None, project: str = None, ctx: Context = None) -> List[Dict[str, Any]]:
    """
    Fetch DeFi yield pools from the yields.llama.fi API, optionally filtering by chain or project.
    Returns symbol, project, tvlUsd, apy, apyMean30d, and predictions for each pool.
    
    Args:
        chain: Optional filter for blockchain (e.g., 'Ethereum', 'Solana')
        project: Optional filter for project name (e.g., 'lido', 'aave-v3')
    """
    async with httpx.AsyncClient() as client:
        try:
            ctx.info("Fetching yield pools from yields.llama.fi")
            response = await client.get("https://yields.llama.fi/pools")
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") != "success":
                raise ValueError("API returned non-success status")
            
            pools = data.get("data", [])
            filtered_pools = []
            
            for pool in pools:
                # Extract required fields
                yield_pool = {
                    "chain": pool.get("chain", ""),
                    "pool": pool.get("symbol", ""),
                    "project": pool.get("project", ""),
                    "tvlUsd": pool.get("tvlUsd", 0.0),
                    "apy": pool.get("apy", 0.0),
                    "apyMean30d": pool.get("apyMean30d", 0.0),
                    "predictions": pool.get("predictions", {})
                }
                
                # Apply filters
                if chain and pool.get("chain", "").lower() != chain.lower():
                    continue
                if project and yield_pool["project"].lower() != project.lower():
                    continue
                
                filtered_pools.append(yield_pool)
            
            ctx.info(f"Returning {len(filtered_pools)} yield pools")
            return filtered_pools
        except Exception as e:
            ctx.error(f"Error fetching yield pools: {str(e)}")
            raise

# Prompt to guide users in analyzing yield pools
@mcp.prompt()
def analyze_yields(chain: str = None, project: str = None) -> str:
    """
    Generate a prompt to analyze DeFi yield pools, optionally filtered by chain or project.
    
    Args:
        chain: Optional blockchain filter
        project: Optional project filter
    """
    base_prompt = "Please analyze the following DeFi yield pools data, including symbol, project name, TVL (USD), APY (%), 30-day mean APY (%), and predictions."
    
    if chain and project:
        return f"{base_prompt} Focus on pools from the '{project}' project on the '{chain}' chain."
    elif chain:
        return f"{base_prompt} Focus on pools on the '{chain}' chain."
    elif project:
        return f"{base_prompt} Focus on pools from the '{project}' project."
    else:
        return f"{base_prompt} Include all available pools."

# Run the server
def main() -> None:
    mcp.run()
