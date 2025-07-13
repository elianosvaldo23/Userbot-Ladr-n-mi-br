import asyncio
import logging
from pyrogram import Client
from pyrogram.errors import FloodWait, UserPrivacyRestricted, PeerFlood, UserNotMutualContact
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MemberTransferBot:
    def __init__(self):
        Config.validate()
        self.app = Client(
            Config.get_session_name(),
            api_id=Config.get_api_id(),
            api_hash=Config.get_api_hash(),
            phone_number=Config.get_phone_number()
        )
    
    async def transfer_members_simple(self, source_group, destination_group):
        """Simple member transfer with basic functionality"""
        try:
            await self.app.start()
            logger.info("Bot started successfully")
            
            # Get source group info
            source_chat = await self.app.get_chat(source_group)
            dest_chat = await self.app.get_chat(destination_group)
            
            logger.info(f"Source: {source_chat.title} ({source_chat.members_count} members)")
            logger.info(f"Destination: {dest_chat.title}")
            
            # Get members from source group
            members = []
            async for member in self.app.get_chat_members(source_group):
                if not member.user.is_bot and not member.user.is_deleted:
                    members.append(member.user)
            
            logger.info(f"Found {len(members)} valid members to transfer")
            
            # Transfer members
            success_count = 0
            for i, member in enumerate(members[:10]):  # Limit to first 10 for demo
                try:
                    await self.app.add_chat_members(destination_group, member.id)
                    success_count += 1
                    logger.info(f"Added {member.first_name} ({i+1}/{len(members[:10])})")
                    await asyncio.sleep(2)  # 2 second delay
                except Exception as e:
                    logger.warning(f"Failed to add {member.first_name}: {e}")
                    continue
            
            logger.info(f"Transfer completed: {success_count} members added successfully")
            
        except Exception as e:
            logger.error(f"Error during transfer: {e}")
        finally:
            await self.app.stop()

# Example usage function
async def demo_transfer():
    # This is a demo function - replace with actual group IDs
    bot = MemberTransferBot()
    
    # Example group IDs (replace with real ones)
    source = "@source_group"  # or group ID like -1001234567890
    destination = "@dest_group"  # or group ID like -1001234567890
    
    await bot.transfer_members_simple(source, destination)

if __name__ == "__main__":
    print("Telegram Member Transfer Bot")
    print("Make sure to configure your .env file first!")
    
    # For demo purposes - in real usage, get these from user input
    source_group = input("Enter source group username or ID: ").strip()
    destination_group = input("Enter destination group username or ID: ").strip()
    
    if source_group and destination_group:
        bot = MemberTransferBot()
        asyncio.run(bot.transfer_members_simple(source_group, destination_group))
    else:
        print("Please provide both source and destination groups")
