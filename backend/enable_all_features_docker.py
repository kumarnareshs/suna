#!/usr/bin/env python3
"""
Script to enable all common feature flags in Docker environment.
This enables all the features needed for the Suna AI Worker to function properly.
"""

import asyncio
import os
import sys

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flags.flags import enable_flag, is_enabled
from utils.logger import logger


async def enable_all_features():
    """Enable all common feature flags"""
    
    # Define all the feature flags that should be enabled
    feature_flags = {
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
    
    print("🚀 Enabling All Feature Flags...")
    print("=" * 50)
    
    results = {}
    
    for flag_name, description in feature_flags.items():
        print(f"\nEnabling {flag_name}...")
        
        try:
            # Check if already enabled
            currently_enabled = await is_enabled(flag_name)
            
            if currently_enabled:
                print(f"  ✅ {flag_name} is already enabled")
                results[flag_name] = True
                continue
            
            # Enable the flag
            success = await enable_flag(flag_name, description)
            
            if success:
                # Verify the flag is now enabled
                is_now_enabled = await is_enabled(flag_name)
                if is_now_enabled:
                    print(f"  ✅ {flag_name} enabled successfully")
                    results[flag_name] = True
                else:
                    print(f"  ❌ {flag_name} verification failed")
                    results[flag_name] = False
            else:
                print(f"  ❌ {flag_name} failed to enable")
                results[flag_name] = False
                
        except Exception as e:
            print(f"  ❌ {flag_name} error: {e}")
            results[flag_name] = False
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Results Summary:")
    
    enabled_count = sum(1 for success in results.values() if success)
    total_count = len(results)
    
    for flag_name, success in results.items():
        status = "✅ Enabled" if success else "❌ Failed"
        print(f"  {flag_name:<25} {status}")
    
    print(f"\n✅ Successfully enabled {enabled_count}/{total_count} feature flags")
    
    if enabled_count == total_count:
        print("🎉 All features are now available!")
    else:
        print("⚠️  Some features failed to enable. Check the logs above.")
    
    return results


if __name__ == "__main__":
    asyncio.run(enable_all_features())
