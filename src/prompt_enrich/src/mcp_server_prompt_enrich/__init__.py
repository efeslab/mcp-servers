from .server import serve


def main():
    """MCP Prompt Enrich Server - Prompt enrichment functionality for MCP"""
    import argparse
    import asyncio

    parser = argparse.ArgumentParser(
        description="give a model the ability to handle prompt enrichment"
    )
    parser.add_argument("--domain", type=str, help="Domain of the prompt (data analysis or model training)")
    parser.add_argument("--user", type=str, help="User requirement")

    args = parser.parse_args()
    asyncio.run(serve(args.domain, args.user))


if __name__ == "__main__":
    main()
