import argparse
from pathlib import Path

from .workflow import KnowledgeInjectionWorkflow


def main():
    parser = argparse.ArgumentParser(
        prog="knowledge-editor",
        description="2FUN Knowledge Injection Editor"
    )

    subparsers = parser.add_subparsers(dest="command")

    # import
    import_parser = subparsers.add_parser(
        "import",
        help="Import a knowledge node"
    )

    import_parser.add_argument(
        "file",
        help="Path to knowledge node JSON file"
    )

    import_parser.add_argument(
        "--repo",
        default="modules/knowledge",
        help="Knowledge repository path"
    )

    args = parser.parse_args()

    if args.command == "import":
        workflow = KnowledgeInjectionWorkflow()

        result = workflow.process(
            json_file=args.file,
            repository=args.repo,
        )

        print("\n===== RESULT =====")
        print(f"Success      : {result['success']}")
        print(f"Status       : {result['status']}")
        print(f"Completeness : {result['completeness']}%")
        print(f"File         : {result['file']}")

        if result["errors"]:
            print("\nErrors:")
            for error in result["errors"]:
                print(f" - {error}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
