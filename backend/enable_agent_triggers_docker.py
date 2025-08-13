#!/usr/bin/env python3
"""
Simple script to enable agent_triggers feature flag in Docker environment.
Run this script inside the Docker container.
"""

import asyncio
import os
import sys

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flags.flags import enable_flag, is_enabled
from utils.logger import logger


async def enable_agent_triggers():
    """Enable the agent_triggers feature flag"""
    try:
        print("🚀 Enabling agent_triggers feature flag...")
        
        # Check if already enabled
        currently_enabled = await is_enabled("agent_triggers")
        if currently_enabled:
            print("✅ Agent triggers feature flag is already enabled!")
            return True
        
        # Enable the flag
        success = await enable_flag(
            "agent_triggers", 
            "Enable agent triggers functionality for automated agent execution"
        )
        
        if success:
            print("✅ Successfully enabled agent_triggers feature flag!")
            
            # Verify
            is_now_enabled = await is_enabled("agent_triggers")
            if is_now_enabled:
                print("✅ Verification: agent_triggers is now enabled")
                return True
            else:
                print("❌ Verification failed: agent_triggers is still disabled")
                return False
        else:
            print("❌ Failed to enable agent_triggers feature flag")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Error enabling agent_triggers: {e}")
        return False


if __name__ == "__main__":
    asyncio.run(enable_agent_triggers())
