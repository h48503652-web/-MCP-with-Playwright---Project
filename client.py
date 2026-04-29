import asyncio
from contextlib import AsyncExitStack
from pathlib import Path
import sys
from typing import Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPClient:
    def __init__(self, server_script_path: str):
        self.server_script_path = server_script_path
        self.client_name = Path(server_script_path).stem.replace("-", "_")
        self.session: Optional[ClientSession] = None
        self._session_stack = AsyncExitStack()
        self._stdio_stack = AsyncExitStack()

    async def connect_to_server(self, server_script_path: Optional[str] = None):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        server_script_path = str(Path(server_script_path or self.server_script_path).resolve())

        # Reuse the current interpreter so child MCP servers run in the same env.
        command = sys.executable
        server_params = StdioServerParameters(
            command=command, args=[server_script_path], env=None
        )

        stdio_transport = await self._stdio_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self._session_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def cleanup(self):
        """Clean up client resources."""
        try:
            await self._session_stack.aclose()
        except asyncio.CancelledError:
            # ClientSession cancels its receive loop during normal shutdown.
            pass
        finally:
            self.session = None

        await self._stdio_stack.aclose()
