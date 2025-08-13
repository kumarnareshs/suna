#!/usr/bin/env python3
"""
Script to manage feature flags in the Suna AI Worker.
This script can enable, disable, and list feature flags.
"""

import asyncio
import sys
import os
import argparse

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from flags.flags import enable_flag, disable_flag, is_enabled, list_flags, get_flag_details
from utils.logger import logger


async def list_all_flags():
    """List all feature flags and their status"""
    try:
        flags = await list_flags()
        
        if not flags:
            print("No feature flags found.")
            return
        
        print("\n📋 Feature Flags Status:")
        print("=" * 60)
        
        for flag_name, is_enabled_flag in flags.items():
            details = await get_flag_details(flag_name)
            status = "✅ ENABLED" if is_enabled_flag else "❌ DISABLED"
            description = details.get('description', 'No description') if details else 'No description'
            
            print(f"{flag_name:<25} {status}")
            print(f"{'':25} {description}")
            print()
            
    except Exception as e:
        logger.error(f"Error listing flags: {e}")
        print(f"❌ Error listing flags: {e}")


async def enable_feature_flag(flag_name: str, description: str = ""):
    """Enable a specific feature flag"""
    try:
        # Check if the flag is already enabled
        currently_enabled = await is_enabled(flag_name)
        
        if currently_enabled:
            print(f"ℹ️  Feature flag '{flag_name}' is already enabled")
            return True
        
        # Enable the flag
        success = await enable_flag(flag_name, description)
        
        if success:
            print(f"✅ Successfully enabled feature flag: {flag_name}")
            
            # Verify the flag is now enabled
            is_now_enabled = await is_enabled(flag_name)
            if is_now_enabled:
                print(f"✅ Verification: {flag_name} is now enabled")
                return True
            else:
                print(f"❌ Verification failed: {flag_name} is still disabled")
                return False
        else:
            print(f"❌ Failed to enable feature flag: {flag_name}")
            return False
            
    except Exception as e:
        logger.error(f"Error enabling flag {flag_name}: {e}")
        print(f"❌ Error enabling {flag_name}: {e}")
        return False


async def disable_feature_flag(flag_name: str):
    """Disable a specific feature flag"""
    try:
        # Check if the flag is currently enabled
        currently_enabled = await is_enabled(flag_name)
        
        if not currently_enabled:
            print(f"ℹ️  Feature flag '{flag_name}' is already disabled")
            return True
        
        # Disable the flag
        success = await disable_flag(flag_name, "Disabled via management script")
        
        if success:
            print(f"✅ Successfully disabled feature flag: {flag_name}")
            return True
        else:
            print(f"❌ Failed to disable feature flag: {flag_name}")
            return False
            
    except Exception as e:
        logger.error(f"Error disabling flag {flag_name}: {e}")
        print(f"❌ Error disabling {flag_name}: {e}")
        return False


async def check_flag_status(flag_name: str):
    """Check the status of a specific feature flag"""
    try:
        is_enabled_flag = await is_enabled(flag_name)
        details = await get_flag_details(flag_name)
        
        status = "✅ ENABLED" if is_enabled_flag else "❌ DISABLED"
        description = details.get('description', 'No description') if details else 'No description'
        updated_at = details.get('updated_at', 'Unknown') if details else 'Unknown'
        
        print(f"\n📊 Feature Flag: {flag_name}")
        print("=" * 40)
        print(f"Status: {status}")
        print(f"Description: {description}")
        print(f"Last Updated: {updated_at}")
        
    except Exception as e:
        logger.error(f"Error checking flag {flag_name}: {e}")
        print(f"❌ Error checking {flag_name}: {e}")


async def enable_common_flags():
    """Enable commonly used feature flags"""
    common_flags = {
        "agent_triggers": "Enable agent triggers functionality for automated agent execution",
        "custom_agents": "Enable custom agent creation and management",
        "triggers_api": "Enable triggers API endpoints",
        "workflows_api": "Enable workflows API endpoints",
        "knowledge_base": "Enable knowledge base functionality",
        "mcp_module": "Enable MCP (Model Context Protocol) module",
        "templates_api": "Enable templates API",
        "pipedream": "Enable Pipedream integration",
        "credentials_api": "Enable credentials API",
        "suna_default_agent": "Enable Suna default agent"
    }
    
    print("\n🚀 Enabling Common Feature Flags...")
    print("=" * 50)
    
    results = {}
    for flag_name, description in common_flags.items():
        print(f"\nEnabling {flag_name}...")
        success = await enable_feature_flag(flag_name, description)
        results[flag_name] = success
    
    print("\n" + "=" * 50)
    print("📊 Results Summary:")
    
    enabled_count = sum(1 for success in results.values() if success)
    total_count = len(results)
    
    for flag_name, success in results.items():
        status = "✅ Enabled" if success else "❌ Failed"
        print(f"  {flag_name:<25} {status}")
    
    print(f"\n✅ Successfully enabled {enabled_count}/{total_count} feature flags")


async def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Manage feature flags in Suna AI Worker")
    parser.add_argument("action", choices=["list", "enable", "disable", "check", "enable-common"], 
                       help="Action to perform")
    parser.add_argument("--flag", "-f", help="Feature flag name (required for enable/disable/check)")
    parser.add_argument("--description", "-d", help="Description for the flag (for enable action)")
    
    args = parser.parse_args()
    
    if args.action in ["enable", "disable", "check"] and not args.flag:
        print("❌ Error: --flag is required for enable, disable, and check actions")
        parser.print_help()
        sys.exit(1)
    
    print("🎛️  Suna AI Worker Feature Flag Manager")
    print("=" * 50)
    
    try:
        if args.action == "list":
            await list_all_flags()
        elif args.action == "enable":
            await enable_feature_flag(args.flag, args.description or "")
        elif args.action == "disable":
            await disable_feature_flag(args.flag)
        elif args.action == "check":
            await check_flag_status(args.flag)
        elif args.action == "enable-common":
            await enable_common_flags()
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
