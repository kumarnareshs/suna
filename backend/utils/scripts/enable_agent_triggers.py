#!/usr/bin/env python3
"""
Script to enable the agent_triggers feature flag.
This script enables the agent triggers functionality in the Suna AI Worker.
"""

import asyncio
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from flags.flags import enable_flag, is_enabled
from utils.logger import logger


async def enable_agent_triggers():
    """Enable the agent_triggers feature flag"""
    try:
        # Check if the flag is already enabled
        currently_enabled = await is_enabled("agent_triggers")
        
        if currently_enabled:
            logger.info("Agent triggers feature flag is already enabled")
            return True
        
        # Enable the flag
        success = await enable_flag(
            "agent_triggers", 
            "Enable agent triggers functionality for automated agent execution"
        )
        
        if success:
            logger.info("✅ Successfully enabled agent triggers feature flag")
            
            # Verify the flag is now enabled
            is_now_enabled = await is_enabled("agent_triggers")
            if is_now_enabled:
                logger.info("✅ Verification: agent triggers feature flag is now enabled")
                return True
            else:
                logger.error("❌ Verification failed: agent triggers feature flag is still disabled")
                return False
        else:
            logger.error("❌ Failed to enable agent triggers feature flag")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error enabling agent triggers feature flag: {e}")
        return False


async def main():
    """Main function"""
    print("🚀 Enabling Agent Triggers Feature Flag...")
    print("=" * 50)
    
    success = await enable_agent_triggers()
    
    print("=" * 50)
    if success:
        print("✅ Agent triggers feature flag has been enabled successfully!")
        print("\nYou can now:")
        print("  • Create triggers for your agents")
        print("  • Set up automated agent execution")
        print("  • Configure webhooks, schedules, and integrations")
        print("\nThe feature will be available in the agent configuration interface.")
    else:
        print("❌ Failed to enable agent triggers feature flag.")
        print("Please check the logs for more details.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
