# Vision: Unity & C# Integration for ADHD Framework

## Overview
This document explores the possibilities of using the ADHD Framework within a Unity/C# development environment. The goal is to leverage the framework's AI-driven high-speed development capabilities for game development without necessarily rewriting the entire framework in C#.

## Strategic Analysis

### Option 1: Native C# Port (Not Recommended)
Porting the entire ADHD framework to C# is theoretically possible but strategically inadvisable.
*   **Pros**: Native integration with Unity Editor; no Python dependency.
*   **Cons**:
    *   **Massive Effort**: Rewriting all cores, managers, and utilities.
    *   **Maintenance Burden**: Keeping Python and C# versions in sync would be difficult.
    *   **Ecosystem Mismatch**: The framework relies on Python's rich AI/ML ecosystem (Pydantic, LangChain, etc.) which may not have direct equivalents in C#.

### Option 2: MCP (Model Context Protocol) Integration (Highly Recommended)
The ADHD framework already supports MCP (`mcps/` directory). We can expose the framework's capabilities as an MCP Server.
*   **Concept**: The ADHD framework runs as a background process (MCP Server). A Unity Editor extension acts as an MCP Client.
*   **Workflow**:
    1.  Unity developer asks for a new feature (e.g., "Create a new Inventory System").
    2.  Unity MCP Client sends the request to the ADHD MCP Server.
    3.  ADHD Server processes the request, generates code/assets, and writes them to the Unity project folder.
    4.  Unity detects file changes and recompiles.
*   **Pros**:
    *   Decoupled architecture.
    *   Leverages existing Python code.
    *   Standardized protocol.

### Option 3: CLI Wrapper / Sidecar
Unity can execute external processes. We can create a lightweight C# wrapper in Unity that calls the ADHD CLI.
*   **Concept**: `System.Diagnostics.Process.Start("python", "adhd_cli.py ...")`
*   **Pros**: Simple to implement.
*   **Cons**: Limited interactivity compared to MCP; parsing stdout/stderr can be brittle.

### Option 4: HTTP/WebSocket API Layer
Wrap the ADHD framework in a FastAPI server.
*   **Concept**: Run `python server.py`. Unity communicates via `UnityWebRequest`.
*   **Pros**: Real-time communication; language agnostic.
*   **Cons**: Requires building a new API layer on top of the framework.

## Proposed Architecture: The "Sidecar" Approach

The most robust and "AI-native" way to proceed is **Option 2 (MCP)** or **Option 4 (API)**. Since MCP is already part of the framework's DNA:

1.  **ADHD Host**: A Python process running the framework.
2.  **Unity Bridge**: A C# Editor Window script in Unity.
3.  **Communication**: JSON-RPC (via MCP) or HTTP.

### Roadmap for Unity Support
1.  **Verify MCP Capabilities**: Ensure `adhd_mcp` can expose core framework functions (scaffolding, refactoring, etc.).
2.  **Create Unity Client**: Develop a generic Unity Editor Window that connects to an MCP server.
3.  **Shared File System**: Since both run locally, they share the same disk. ADHD writes files; Unity reads them.

## Conclusion
Do not port to C#. Instead, **bridge** to C#. Treat the ADHD framework as an intelligent "Development Server" that runs alongside Unity, providing code generation and architectural guidance via a standardized protocol like MCP.
