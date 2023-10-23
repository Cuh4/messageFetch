# //----------------------
# main
# //----------------------

# // ---- Imports
import discord
import json
import asyncio

import config
from src import helpers

# // ---- Variables
# configurables
channel_id = int(helpers.prettyprint.query("Channel ID: "))
amount_to_fetch = int(helpers.prettyprint.query("Message Count: "))

# intents
intents = discord.Intents.default()
intents.message_content = True

# bot
client = discord.Client(
    intents = intents
)

# // ---- Functions
async def fetchMessages(channel: discord.TextChannel, amountToFetch: int, excludeMessagesWithAttachments: bool = False, excludeEmptyMessages: bool = False) -> list[discord.Message]:
    messages = []

    async for message in channel.history(limit = amountToFetch):
        if excludeMessagesWithAttachments and len(message.attachments) != 0:
            continue
        
        if excludeEmptyMessages and message.content == "":
            continue
        
        messages.append(message)
            
    return messages

async def closeBot(delay: int = 0):
    await asyncio.sleep(delay)
    await client.close()

# // ---- Main
# // events
@client.event
async def on_ready():
    # notify
    helpers.prettyprint.success(f"{helpers.utils.formattedName(client.user)} is up.")
    
    # get channel
    try:
        channel = client.get_channel(channel_id)
        
        if channel is None:
            raise Exception("Channel was not found by the bot.")
    except Exception as e:
        # failed to get channel, so notify
        helpers.prettyprint.error(f"Failed to retrieve desired channel. Error: {str(e)}")
        
        # close
        return await closeBot(4)
    
    # notify
    helpers.prettyprint.info(f"Fetching {amount_to_fetch} messages from {channel.name}.")
    
    # fetch messages
    try:
        messages = await fetchMessages(channel, amount_to_fetch, config.excludeMessagesWithAttachments, config.excludeEmptyMessages)
    except Exception as e:
        # failed, so notify
        helpers.prettyprint.error(f"Failed to fetch messages. Error: {str(e)}")
        
        if config.notifyInChannel:
            await channel.send(
                embed = helpers.embeds.failure("Failed to fetch messages.")
            )
        
        # close
        return await closeBot(4)
    
    # dump
    slash = "/" if config.dumpFilePath != "" else ""
    path = f"{config.dumpFilePath}{slash}{config.dumpFileName}.json"

    with open(path, "w") as f:
        f.write(json.dumps(
            obj = [message.content for message in messages],
            indent = 5
        ))
        
    # notify progress
    helpers.prettyprint.success(f"Dumped {len(messages)} messages from {channel.name} into {path}.")
        
    if config.notifyInChannel:
        await channel.send(
            embed = helpers.embeds.success(f"Fetched `{len(messages)}` messages from {helpers.utils.channelMention(channel)}. Dumped to `{path}`.")
        )
    
    # close bot after completion
    helpers.prettyprint.warn("Completed!")
    return await closeBot(4)
    
# // run
client.run(config.token, log_handler = None)