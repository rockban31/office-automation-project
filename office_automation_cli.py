#!/usr/bin/env python3
"""
Office Automation Project - Unified CLI Interface

Main command-line interface for the Office Automation Project.
Provides access to all automation tools and utilities.
"""

import os
import sys
import argparse
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.auth.mist_auth import MistAuth, MistAuthError
from src.troubleshooting.mist_wireless import MistWirelessTroubleshooter


def setup_common_args(parser):
    """Add common arguments to all subcommands"""
    parser.add_argument('--token', 
                       help='Mist API Token (can also use MIST_API_TOKEN env var)')
    parser.add_argument('--org-id', 
                       help='Mist Organization ID (optional - will auto-detect if not provided, can use MIST_ORG_ID env var)')
    parser.add_argument('--verbose', '-v', 
                       action='store_true', 
                       help='Enable verbose output')


def cmd_test_auth(args):
    """Test Mist API authentication"""
    try:
        api_token = args.token or os.getenv('MIST_API_TOKEN')
        if not api_token:
            print("❌ ERROR: Mist API token is required.")
            print("   Provide via --token argument or MIST_API_TOKEN environment variable")
            return 1
        
        with MistAuth(api_token=api_token, org_id=args.org_id) as auth:
            print(f"🔧 Testing Mist API Authentication...")
            if args.verbose:
                print(f"   API Token: {api_token[:8]}...{api_token[-4:]}")
                print(f"   Organization ID: {args.org_id or 'Auto-detect'}")
            
            status = auth.test_connection()
            
            if status['status'] == 'connected':
                print(f"✅ Authentication successful!")
                print(f"   User: {status['user_info'].get('first_name', '')} {status['user_info'].get('last_name', '')}")
                print(f"   Email: {status['user_info'].get('email', 'Unknown')}")
                
                if status['org_info']:
                    print(f"   Organization: {status['org_info'].get('name', 'Unknown')}")
                    print(f"   Org ID: {status['org_info'].get('id', 'Unknown')}")
                
                return 0
            else:
                print(f"❌ Authentication failed: {status.get('error', 'Unknown error')}")
                return 1
                
    except MistAuthError as e:
        print(f"❌ Authentication error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def cmd_list_orgs(args):
    """List all available Mist organizations"""
    try:
        api_token = args.token or os.getenv('MIST_API_TOKEN')
        if not api_token:
            print("❌ ERROR: Mist API token is required.")
            return 1
        
        with MistAuth(api_token=api_token) as auth:
            orgs = auth.get_organizations()
            
            if orgs:
                print(f"\n{'='*60}")
                print(f"AVAILABLE MIST ORGANIZATIONS")
                print(f"{'='*60}")
                
                for i, org in enumerate(orgs, 1):
                    print(f"{i:2}. Name: {org['name']}")
                    print(f"    ID: {org['id']}")
                    print(f"    Type: {org.get('orgtype', 'Unknown')}")
                    if args.verbose:
                        print(f"    Created: {org.get('created_time', 'Unknown')}")
                        print(f"    Modified: {org.get('modified_time', 'Unknown')}")
                    print("-" * 60)
                
                print(f"\n💡 TIP: Set MIST_ORG_ID environment variable to skip org selection:")
                print(f"   export MIST_ORG_ID='your_preferred_org_id'")
                return 0
            else:
                print("❌ No organizations found or API token invalid")
                return 1
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


def cmd_troubleshoot_wireless(args):
    """Troubleshoot wireless client connectivity issues"""
    try:
        api_token = args.token or os.getenv('MIST_API_TOKEN')
        if not api_token:
            print("❌ ERROR: Mist API token is required.")
            print("   Provide via --token argument or MIST_API_TOKEN environment variable")
            return 1
        
        if not args.client_mac:
            print("❌ ERROR: Client MAC address is required for troubleshooting")
            return 1
        
        # Normalize MAC address format
        client_mac = args.client_mac.lower().replace(':', '').replace('-', '')
        if len(client_mac) == 12:
            client_mac = ':'.join([client_mac[i:i+2] for i in range(0, 12, 2)])
        
        if not args.client_ip:
            print("⚠️  WARNING: Client IP not provided. Some connectivity tests will be skipped.")
            args.client_ip = "unknown"
        
        # Initialize authentication
        org_id = args.org_id or os.getenv('MIST_ORG_ID')
        
        with MistAuth(api_token=api_token, org_id=org_id) as auth:
            # Auto-select org if not specified
            if not auth.org_id:
                troubleshooter = MistWirelessTroubleshooter(auth_instance=auth)
                selected_org_id = troubleshooter.auto_select_org()
                if not selected_org_id:
                    print("❌ Unable to determine organization ID")
                    return 1
                auth.org_id = selected_org_id
            
            # Initialize troubleshooter
            troubleshooter = MistWirelessTroubleshooter(auth_instance=auth)
            
            if args.verbose:
                print(f"🔧 VERBOSE MODE ENABLED")
                print(f"   API Token: {api_token[:8]}...{api_token[-4:]}")
                print(f"   Organization ID: {auth.org_id}")
                print(f"   Client IP: {args.client_ip}")
                print(f"   Client MAC: {client_mac}")
                print(f"   Hours back: {args.hours_back}")
            
            # Run troubleshooting
            results = troubleshooter.troubleshoot_client(
                client_ip=args.client_ip,
                client_mac=client_mac,
                hours_back=args.hours_back
            )
            
            # Display summary
            print(f"\n{'='*70}")
            print(f"TROUBLESHOOTING SUMMARY")
            print(f"{'='*70}")
            print(f"Status: {results['status']}")
            print(f"Steps Completed: {len(results['steps_completed'])}")
            print(f"Issues Found: {len(results['issues_found'])}")
            print(f"Escalation Path: {results.get('escalation_path', 'None')}")
            
            if results['recommendations']:
                print(f"\nRecommendations:")
                for i, rec in enumerate(results['recommendations'], 1):
                    print(f"  {i}. {rec}")
            
            # Return appropriate exit code
            if results['status'] in ['error']:
                return 1
            elif results['status'] in ['authentication_issues', 'network_infrastructure_issues', 'client_health_issues']:
                return 2  # Issues found
            else:
                return 0  # All good
                
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Analysis interrupted by user")
        return 130
    except Exception as e:
        print(f"❌ ERROR: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog='office-automation',
        description='Office Automation Project - Unified CLI Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test authentication
  office-automation auth test --token YOUR_TOKEN
  
  # List organizations
  office-automation orgs list --token YOUR_TOKEN
  
  # Troubleshoot wireless client
  office-automation wireless troubleshoot --client-mac aa:bb:cc:dd:ee:ff --client-ip 192.168.1.100
  
  # Using environment variables (recommended)
  export MIST_API_TOKEN="your_token_here"
  office-automation wireless troubleshoot --client-mac aa:bb:cc:dd:ee:ff --client-ip 192.168.1.100 --verbose
        """
    )
    
    # Create subparsers
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    subparsers.required = True
    
    # Authentication commands
    auth_parser = subparsers.add_parser('auth', help='Authentication management')
    auth_subparsers = auth_parser.add_subparsers(dest='auth_command', help='Auth commands')
    
    # Test authentication
    auth_test_parser = auth_subparsers.add_parser('test', help='Test API authentication')
    setup_common_args(auth_test_parser)
    auth_test_parser.set_defaults(func=cmd_test_auth)
    
    # Organization commands  
    orgs_parser = subparsers.add_parser('orgs', help='Organization management')
    orgs_subparsers = orgs_parser.add_subparsers(dest='orgs_command', help='Organization commands')
    
    # List organizations
    orgs_list_parser = orgs_subparsers.add_parser('list', help='List available organizations')
    setup_common_args(orgs_list_parser)
    orgs_list_parser.set_defaults(func=cmd_list_orgs)
    
    # Wireless troubleshooting commands
    wireless_parser = subparsers.add_parser('wireless', help='Wireless network troubleshooting')
    wireless_subparsers = wireless_parser.add_subparsers(dest='wireless_command', help='Wireless commands')
    
    # Troubleshoot wireless client
    wireless_troubleshoot_parser = wireless_subparsers.add_parser('troubleshoot', help='Troubleshoot wireless client connectivity')
    setup_common_args(wireless_troubleshoot_parser)
    wireless_troubleshoot_parser.add_argument('--client-ip', required=False, help='Client IP Address')
    wireless_troubleshoot_parser.add_argument('--client-mac', required=True, help='Client MAC Address')
    wireless_troubleshoot_parser.add_argument('--hours-back', type=int, default=24, help='Hours back to check for events (default: 24)')
    wireless_troubleshoot_parser.set_defaults(func=cmd_troubleshoot_wireless)
    
    # Parse arguments and dispatch
    args = parser.parse_args()
    
    # Handle nested commands
    if hasattr(args, 'func'):
        return args.func(args)
    elif args.command == 'auth':
        if not hasattr(args, 'auth_command') or args.auth_command is None:
            auth_parser.print_help()
            return 1
    elif args.command == 'orgs':
        if not hasattr(args, 'orgs_command') or args.orgs_command is None:
            orgs_parser.print_help()
            return 1
    elif args.command == 'wireless':
        if not hasattr(args, 'wireless_command') or args.wireless_command is None:
            wireless_parser.print_help()
            return 1
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())