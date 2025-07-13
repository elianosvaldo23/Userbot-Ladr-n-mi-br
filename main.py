import asyncio
import logging
from pyrogram import Client
from pyrogram.errors import FloodWait, UserPrivacyRestricted, PeerFlood, UserNotMutualContact
from config import Config
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TelegramUserBot:
    def __init__(self):
        Config.validate()
        self.app = Client(
            Config.get_session_name(),
            api_id=Config.get_api_id(),
            api_hash=Config.get_api_hash(),
            phone_number=Config.get_phone_number()
        )
    
    async def get_group_members(self, group_id):
        """Get all members from a group"""
        members = []
        try:
            async for member in self.app.get_chat_members(group_id):
                if not member.user.is_bot and not member.user.is_deleted:
                    members.append(member.user)
            logger.info(f"Found {len(members)} members in source group")
            return members
        except Exception as e:
            logger.error(f"Error getting members: {e}")
            return []
    
    async def add_member_to_group(self, group_id, user_id):
        """Add a single member to a group"""
        try:
            await self.app.add_chat_members(group_id, user_id)
            logger.info(f"Successfully added user {user_id} to group")
            return True
        except FloodWait as e:
            logger.warning(f"FloodWait: sleeping for {e.value} seconds")
            await asyncio.sleep(e.value)
            return False
        except UserPrivacyRestricted:
            logger.warning(f"User {user_id} has privacy restrictions")
            return False
        except PeerFlood:
            logger.error("Too many requests, peer flood detected")
            return False
        except UserNotMutualContact:
            logger.warning(f"User {user_id} is not a mutual contact")
            return False
        except Exception as e:
            logger.error(f"Error adding user {user_id}: {e}")
            return False
    
    async def transfer_members(self, source_group, destination_group, delay=2):
        """Transfer members from source group to destination group"""
        logger.info(f"Starting member transfer from {source_group} to {destination_group}")
        
        # Get members from source group
        members = await self.get_group_members(source_group)
        
        if not members:
            logger.error("No members found in source group")
            return
        
        successful_transfers = 0
        failed_transfers = 0
        
        for member in members:
            try:
                success = await self.add_member_to_group(destination_group, member.id)
                
                if success:
                    successful_transfers += 1
                    logger.info(f"Added {member.first_name} ({member.id}) - Success: {successful_transfers}")
                else:
                    failed_transfers += 1
                
                # Add delay to avoid rate limiting
                await asyncio.sleep(delay)
                
            except Exception as e:
                logger.error(f"Unexpected error with user {member.id}: {e}")
                failed_transfers += 1
                continue
        
        logger.info(f"Transfer completed. Successful: {successful_transfers}, Failed: {failed_transfers}")
    
    async def get_group_info(self, group_id):
        """Get information about a group"""
        try:
            chat = await self.app.get_chat(group_id)
            logger.info(f"Group: {chat.title} - Members: {chat.members_count}")
            return chat
        except Exception as e:
            logger.error(f"Error getting group info: {e}")
            return None
    
    async def start(self):
        """Start the userbot"""
        await self.app.start()
        logger.info("Userbot started successfully")
    
    async def stop(self):
        """Stop the userbot"""
        await self.app.stop()
        logger.info("Userbot stopped")

async def main():
    userbot = TelegramUserBot()
    
    try:
        await userbot.start()
        
        # Example usage - replace with actual group IDs or usernames
        source_group = input("Enter source group ID or username: ").strip()
        destination_group = input("Enter destination group ID or username: ").strip()
        
        # Get group information
        await userbot.get_group_info(source_group)
        await userbot.get_group_info(destination_group)
        
        # Confirm before proceeding
        confirm = input("Do you want to proceed with member transfer? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            # Set delay between requests (recommended: 2-5 seconds)
            delay = int(input("Enter delay between requests in seconds (recommended 2-5): ") or "2")
            
            await userbot.transfer_members(source_group, destination_group, delay)
        else:
            logger.info("Transfer cancelled by user")
    
    except KeyboardInterrupt:
        logger.info("Process interrupted by user")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        await userbot.stop()

if __name__ == "__main__":
    asyncio.run(main())
