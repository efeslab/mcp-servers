# test_client.py
import json
import sys
import time

def send_and_wait(message, delay=0.1):
    """Send a message and wait briefly"""
    print(json.dumps(message))
    sys.stdout.flush()
    time.sleep(delay)

def main():
    # 1. Initialize
    print("Sending initialize...", file=sys.stderr)
    init_msg = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    send_and_wait(init_msg)
    
    # 2. Send initialized notification
    print("Sending initialized...", file=sys.stderr)
    initialized_msg = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }
    send_and_wait(initialized_msg)
    
    # 3. List tools
    print("Listing tools client...", file=sys.stderr)
    list_tools_msg = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    send_and_wait(list_tools_msg)
    
    # 4. Call tool
    print("Calling tool client...", file=sys.stderr)
    call_tool_msg = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "get_prompt_template",
            "arguments": {
                "domain": "data analysis",
                "user_requirement": "Load and explore the sklearn Iris dataset with basic statistics and visualization"
            }
        }
    }
    send_and_wait(call_tool_msg)

if __name__ == "__main__":
    main()