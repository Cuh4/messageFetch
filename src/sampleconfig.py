# //----------------------
# configuration
# //----------------------

# bot
token = "" # your bot's token

# message fetching
notifyInChannel = True # whether or not the bot sends a message in the desired channel upon fetching messages successfully
excludeMessagesWithAttachments = True # whether or not to include messages with attachments
excludeEmptyMessages = True # whether or not to exclude messages with no content (like a text-less message that only contains attachments, etc)

dumpFilePath = "" # folder path to dump file, e.g: "C:/path/to/folder" (empty string = working directory)
dumpFileName = "messages" # name of dump file. this will become "messages.json"

# !! rename this to "config.py" !!