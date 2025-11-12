# tools.py
"""
Custom tools for CrewAI agents that save files in the workspace directory.
These tools will be properly tracked by AgentOps as "Tool" type.
"""
from crewai.tools import tool
from pathlib import Path
import config


@tool("write_file")
def write_file_tool(file_path: str, content: str) -> str:
    """
    Write content to a file in the workspace directory.

    Args:
        file_path: Relative path to the file (e.g., 'prd.md' or 'src/main.py')
        content: Content to write to the file

    Returns:
        Success message with file location
    """
    try:
        # Always save to workspace directory
        full_path = config.WORKSPACE_DIR / file_path

        # Create parent directories if needed
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Write file
        full_path.write_text(content, encoding='utf-8')

        return f"✅ Successfully wrote {len(content)} characters to workspace/{file_path}"
    except Exception as e:
        return f"❌ Error writing file: {str(e)}"


@tool("read_file")
def read_file_tool(file_path: str) -> str:
    """
    Read content from a file in the workspace directory.

    Args:
        file_path: Relative path to the file (e.g., 'prd.md' or 'src/main.py')

    Returns:
        File content or error message
    """
    try:
        full_path = config.WORKSPACE_DIR / file_path

        if not full_path.exists():
            return f"❌ File not found: workspace/{file_path}"

        content = full_path.read_text(encoding='utf-8')
        return f"📄 Content of workspace/{file_path}:\n\n{content}"
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"


@tool("list_files")
def list_files_tool(directory: str = ".") -> str:
    """
    List all files in a directory within the workspace.

    Args:
        directory: Relative path to directory (default: root of workspace)

    Returns:
        List of files in the directory
    """
    try:
        full_path = config.WORKSPACE_DIR / directory

        if not full_path.exists():
            return f"❌ Directory not found: workspace/{directory}"

        files = []
        for item in full_path.rglob("*"):
            if item.is_file():
                rel_path = item.relative_to(config.WORKSPACE_DIR)
                files.append(str(rel_path))

        if not files:
            return f"📁 Directory workspace/{directory} is empty"

        return f"📁 Files in workspace/{directory}:\n" + "\n".join(f"  - {f}" for f in sorted(files))
    except Exception as e:
        return f"❌ Error listing files: {str(e)}"


@tool("create_directory")
def create_directory_tool(directory_path: str) -> str:
    """
    Create a directory in the workspace.

    Args:
        directory_path: Relative path to the directory (e.g., 'src' or 'tests')

    Returns:
        Success message
    """
    try:
        full_path = config.WORKSPACE_DIR / directory_path
        full_path.mkdir(parents=True, exist_ok=True)
        return f"✅ Successfully created directory: workspace/{directory_path}"
    except Exception as e:
        return f"❌ Error creating directory: {str(e)}"


# Export tools
file_writer_tool = write_file_tool
file_reader_tool = read_file_tool
directory_reader_tool = list_files_tool
directory_creator_tool = create_directory_tool
