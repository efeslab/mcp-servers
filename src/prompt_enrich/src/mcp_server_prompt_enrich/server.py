import asyncio
import sys
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel

# Your original function
def get_prompt_template(domain: str, user: str):
    print(f"Domain: {domain}, User: {user}", file=sys.stderr)
    if "analysis" in domain.lower():
        return f"""As a data scientist, you need to help user to achieve their goal via code generation. While some concise thoughts are helpful, code is absolutely required. The code should be such that it can be executed by a code executor.
        
        # Current Task
        {user}

        # Task Guidance
        Write code for the incomplete sections of 'Current Task'. And avoid duplicating code from 'Finished Tasks' and 'Finished Section of Current Task', such as repeated import of packages, reading data, etc.
        Specifically, 
        The current task is about exploratory data analysis, please note the following:
        - Distinguish column types with `select_dtypes` for tailored analysis and visualization, such as correlation.
        - Remember to `import numpy as np` before using Numpy functions.
        - You can assume that the python modules are installed, and you can use them directly.

        # Constraints
        - Take on Current Task if it is in Plan Status, otherwise, tackle User Requirement directly.
        - Always prioritize using pre-defined tools for the same functionality.
        - Generate a tool call for executing the code, from the available tools.

        # Output
        While some concise thoughts are helpful, code is absolutely required. Output code in the following format:
        ```python
        your code
        ```
        - After this code execution, you should create a tool call for the next task of executing the code. 
        """




async def serve(domain: str, user: str):
    # Create the MCP server
    server = Server("prompt-enrich-server")

    @server.list_tools()
    async def handle_list_tools() -> list[Tool]:
        print("Listing tools server...", file=sys.stderr)
        """List available tools."""
        return [
            Tool(
                name="get_prompt_template",
                description="Based on the input domain, the tool returns an enriched prompt template for the user's goal",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "domain": {
                            "type": "string",
                            "description": "The domain of the prompt (Data Analysis or Model Training)"
                        },
                        "user": {
                            "type": "string",
                            "description": "The user's requirement"
                        }
                    },
                    "additionalProperties": False
                }
            )
        ]

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
        """Handle tool calls."""
        if name == "get_prompt_template":
            print(f"Arguments: {arguments}", file=sys.stderr)
            instruction_text = get_prompt_template(arguments["domain"], arguments["user"])
            return [TextContent(type="text", text=instruction_text)]
        else:
            raise ValueError(f"Unknown tool: {name}")

    """Main server loop."""
    print("Starting MCP server...", file=sys.stderr)
    async with stdio_server() as (read_stream, write_stream):
        print("Server initialized, waiting for requests...", file=sys.stderr)
        options = server.create_initialization_options()
        await server.run(
            read_stream, 
            write_stream, 
            options
        )
