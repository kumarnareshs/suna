#!/usr/bin/env python3
"""
Simple script to check if agent_triggers feature flag is enabled.
"""

import asyncio
import os
import sys

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flags.flags import is_enabled


async def check_agent_triggers():
    """Check if agent_triggers feature flag is enabled"""
    try:
        enabled = await is_enabled("agent_triggers")
        
        if enabled:
            print("✅ Agent triggers feature flag is ENABLED")
            print("🎉 You can now use agent triggers functionality!")
        else:
            print("❌ Agent triggers feature flag is DISABLED")
            print("💡 Run the enable script to activate this feature")
            
        return enabled
        
    except Exception as e:
        print(f"❌ Error checking flag: {e}")
        return False


if __name__ == "__main__":
    asyncio.run(check_agent_triggers())
