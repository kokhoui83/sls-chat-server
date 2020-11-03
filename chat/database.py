from datetime import datetime
from chat.models import ChatMessage, ChatAudit

def retrieveChat(user, lastupdate):
    chats = []
    for chat in ChatMessage.scan(ChatMessage.timestamp > lastupdate):
        chats.append(chat.as_dict())

    return chats

def createChat(user, message):
    MAX_CHAT = 20
    try:
        timestamp = int(datetime.utcnow().timestamp())
        chat = ChatMessage(user, timestamp=timestamp, message=message)
        chat.save()
    except Exception as e:
        print('Failed to save chat', e)
        raise Exception('Failed to create chat')

    incrementCount()

    total = ChatMessage.count(user)

    if total > MAX_CHAT:
        for oldchat in ChatMessage.query(user, limit = total - MAX_CHAT):
            try:
                oldchat.delete()
                decrementCount()
            except Exception as e:
                print('Failed to delete old chat', e)
                pass

    return chat.as_dict()

def getChatCount():
    try:
        chatcount = ChatAudit.get('chat_count')
        return chatcount.as_dict()
    except Exception as e:
        print('Failed to get chat count', e)
        raise e

def incrementCount():
    try:
        chatcount = ChatAudit.get('chat_count')
        chatcount.update(actions=[
            ChatAudit.value.set(ChatAudit.value + 1),
            ChatAudit.timestamp.set(int(datetime.utcnow().timestamp()))
        ])
    except Exception as e:
        print('Failed to update chat count', e)
        pass

def decrementCount():
    try:
        chatcount = ChatAudit.get('chat_count')
        chatcount.update(actions=[
            ChatAudit.value.set(ChatAudit.value - 1),
            ChatAudit.timestamp.set(int(datetime.utcnow().timestamp()))
        ])
    except Exception as e:
        print('Failed to update chat count', e)
        pass