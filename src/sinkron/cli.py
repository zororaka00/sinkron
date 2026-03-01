"""
Command Line Interface for Sinkron API
"""
import sys
import argparse
from typing import List
from .client import SinkronClient
from .exceptions import (
    SinkronError,
    SinkronAuthError,
    SinkronNotFoundError,
    SinkronRateLimitError,
    SinkronValidationError,
)


def print_error(message: str):
    """Print error message to stderr"""
    print(f"Error: {message}", file=sys.stderr)


def print_success(message: str):
    """Print success message"""
    print(f"✓ {message}")


def cmd_health(args):
    """Health check command"""
    client = SinkronClient(api_url=args.api_url)
    try:
        result = client.health_check()
        print(result.get("message", "API is running"))
        return 0
    except SinkronError as e:
        print_error(str(e))
        return 1


def cmd_register(args):
    """Register new agent command"""
    client = SinkronClient(api_url=args.api_url)
    try:
        result = client.register(args.username, args.name)
        print("Registration successful!")
        print(f"\nUsername: {result.username}")
        print(f"Email Address: {result.address}")
        print(f"Token: {result.token}")
        print(f"Created: {result.created_at}")
        
        if args.save_token:
            client.config.save()
            print("\n✓ Token saved to config file")
        
        return 0
    except SinkronError as e:
        print_error(str(e))
        return 1


def cmd_inbox(args):
    """Get inbox messages command"""
    client = SinkronClient(token=args.token, api_url=args.api_url)
    try:
        result = client.get_inbox(page=args.page, search=args.search)
        print(result.format_display())
        
        if args.show_body:
            print("\n" + "=" * 60)
            print("MESSAGE BODIES:")
            print("=" * 60)
            for msg in result.messages:
                print(f"\n--- Message {msg.id} ---")
                print(f"From: {msg.from_address}")
                print(f"Subject: {msg.subject}")
                print(f"Body:\n{msg.body}")
        
        return 0
    except SinkronError as e:
        print_error(str(e))
        return 1


def cmd_check(args):
    """Check email exists command"""
    client = SinkronClient(api_url=args.api_url)
    try:
        result = client.check_email(args.address)
        print(result.format_display())
        
        if result.exists:
            print_success(f"Email address {args.address} is registered")
            return 0
        else:
            print_error(f"Email address {args.address} is not registered")
            return 1
    except SinkronError as e:
        print_error(str(e))
        return 1


def cmd_message(args):
    """Get message by ID command"""
    client = SinkronClient(token=args.token, api_url=args.api_url)
    try:
        result = client.get_message(args.id)
        print(result.format_display())
        
        # Show attachment URLs if any
        if result.attachments:
            print("\n--- Attachment Download URLs ---")
            for att in result.attachments:
                print(f"{att.filename}: {att.download_url}")
        
        return 0
    except SinkronError as e:
        print_error(str(e))
        return 1


def cmd_delete_messages(args):
    """Delete messages command"""
    client = SinkronClient(token=args.token, api_url=args.api_url)
    
    # Parse message IDs
    try:
        if args.ids:
            message_ids = [int(x.strip()) for x in args.ids.split(",")]
        else:
            message_ids = []
    except ValueError:
        print_error("Invalid message IDs. Use comma-separated integers.")
        return 1
    
    if not message_ids:
        print_error("No message IDs provided")
        return 1
    
    if len(message_ids) > 25:
        print_error("Maximum 25 messages can be deleted at once")
        return 1
    
    try:
        result = client.delete_messages(message_ids)
        print(result.format_display())
        
        if result.success:
            print_success(f"Deleted {result.deleted} message(s)")
            return 0
        else:
            print_error("Some messages could not be deleted")
            return 1
    except SinkronError as e:
        print_error(str(e))
        return 1


def cmd_delete_inbox(args):
    """Delete inbox command"""
    client = SinkronClient(token=args.token, api_url=args.api_url)
    
    # Confirm deletion
    if not args.force:
        response = input("Are you sure you want to delete your entire inbox? This cannot be undone! (yes/no): ")
        if response.lower() != "yes":
            print("Cancelled.")
            return 0
    
    try:
        result = client.delete_inbox()
        print(result.format_display())
        
        if result.success:
            print_success("Inbox deleted successfully")
            return 0
        else:
            print_error("Failed to delete inbox")
            return 1
    except SinkronError as e:
        print_error(str(e))
        return 1


def cmd_agent(args):
    """Get agent info command"""
    client = SinkronClient(token=args.token, api_url=args.api_url)
    try:
        result = client.get_agent_info(args.username)
        print(result.format_display())
        return 0
    except SinkronError as e:
        print_error(str(e))
        return 1


def cmd_config(args):
    """Config management command"""
    from .config import Config
    
    if args.show:
        config = Config()
        print(f"API URL: {config.api_url}")
        print(f"Token: {config.token or '(not set)'}")
        return 0
    
    if args.token:
        config = Config()
        config.token = args.token
        config.save()
        print_success(f"Token saved to config file")
        return 0
    
    if args.api_url:
        config = Config()
        config.api_url = args.api_url
        config.save()
        print_success(f"API URL saved to config file")
        return 0
    
    if args.clear_token:
        config = Config()
        config.clear_token()
        config.save()
        print_success("Token cleared from config file")
        return 0
    
    # No arguments, show help
    print("Config commands:")
    print("  sinkron config --show              Show current configuration")
    print("  sinkron config --token TOKEN        Set authentication token")
    print("  sinkron config --api-url URL        Set API URL")
    print("  sinkron config --clear-token        Clear saved token")
    return 0


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        prog="sinkron",
        description="Sinkron - Email for AI Agent CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    # Global options
    parser.add_argument(
        "--api-url",
        default=None,
        help="API base URL (default: https://api.sinkron.id)"
    )
    parser.add_argument(
        "--token",
        default=None,
        help="Authentication token"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Health command
    subparsers.add_parser("health", help="Check API health status")
    
    # Register command
    register_parser = subparsers.add_parser("register", help="Register a new agent")
    register_parser.add_argument("--username", required=True, help="Username (4-25 lowercase alphanumeric)")
    register_parser.add_argument("--name", required=True, help="Display name")
    register_parser.add_argument("--save-token", action="store_true", help="Save token to config file")
    
    # Inbox command
    inbox_parser = subparsers.add_parser("inbox", help="Get inbox messages")
    inbox_parser.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
    inbox_parser.add_argument("--search", help="Search keyword")
    inbox_parser.add_argument("--show-body", action="store_true", help="Show message bodies")
    
    # Check command
    check_parser = subparsers.add_parser("check", help="Check if email address exists")
    check_parser.add_argument("address", help="Email address to check")
    
    # Message command
    message_parser = subparsers.add_parser("message", help="Get message by ID")
    message_parser.add_argument("id", type=int, help="Message ID")
    
    # Delete messages command
    delete_msgs_parser = subparsers.add_parser("delete-messages", help="Delete messages by ID")
    delete_msgs_parser.add_argument("--ids", required=True, help="Comma-separated message IDs (max 25)")
    
    # Delete inbox command
    delete_inbox_parser = subparsers.add_parser("delete-inbox", help="Delete entire inbox")
    delete_inbox_parser.add_argument("--force", action="store_true", help="Skip confirmation")
    
    # Agent command
    agent_parser = subparsers.add_parser("agent", help="Get agent info by username")
    agent_parser.add_argument("username", help="Username")
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_parser.add_argument("--show", action="store_true", help="Show current configuration")
    config_parser.add_argument("--token", help="Set authentication token")
    config_parser.add_argument("--api-url", dest="api_url", help="Set API URL")
    config_parser.add_argument("--clear-token", action="store_true", help="Clear saved token")
    
    return parser


def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Map commands to functions
    commands = {
        "health": cmd_health,
        "register": cmd_register,
        "inbox": cmd_inbox,
        "check": cmd_check,
        "message": cmd_message,
        "delete-messages": cmd_delete_messages,
        "delete-inbox": cmd_delete_inbox,
        "agent": cmd_agent,
        "config": cmd_config,
    }
    
    handler = commands.get(args.command)
    if handler:
        return handler(args)
    else:
        print_error(f"Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
