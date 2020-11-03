import os
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute

class ChatMessage(Model):
    class Meta:
        table_name = 'chat-message-table'
        if 'ENV' in os.environ:
            host = 'http://dynamodb-local:8000'
        else:
            region = os.environ['REGION']
            host = os.environ['DYNAMODB_HOST']
    
    user = UnicodeAttribute(hash_key=True)
    timestamp = NumberAttribute(range_key=True, default=0)
    message = UnicodeAttribute()

    def as_dict(self):
        '''
        Takes the current model and reviews the attributes to then translate to a dict
        '''
        return { key: getattr(self, key) for key in self.get_attributes().keys() }

class ChatAudit(Model):
    class Meta:
        table_name = 'chat-audit-table'
        if 'ENV' in os.environ:
            host = 'http://dynamodb-local:8000'
        else:
            region = os.environ['REGION']
            host = os.environ['DYNAMODB_HOST']

    key = UnicodeAttribute(hash_key=True)
    value = NumberAttribute(default=0)
    timestamp = NumberAttribute(default=0)

    def as_dict(self):
        '''
        Takes the current model and reviews the attributes to then translate to a dict
        '''
        return { key: getattr(self, key) for key in self.get_attributes().keys() }

try:
    if not ChatMessage.exists():
        print('Creating chat message table...')
        ChatMessage.create_table(wait=True, billing_mode='PAY_PER_REQUEST')
    
    if not ChatAudit.exists():
        print('Creating chat audit table...')
        ChatAudit.create_table(wait=True, billing_mode='PAY_PER_REQUEST')
        
    try:
        ChatAudit.get('chat_count')
    except ChatAudit.DoesNotExist:
        chatcount = ChatAudit('chat_count')
        chatcount.save()
    except Exception as e:
        print('Failed to create chat_count')
        pass

except Exception as e:
    print('Failed to create table', e)