class BotAutoreply(Bot):
    def can_process(self, main, message):
        text = message.message.replace('.', '{:}')
        if main.options.get('options.autoreply.strip', False):
            text = text.strip()
        if main.options.get('options.autoreply.lower', False):
            text = text.lower()
        replies = main.options.get('options.autoreply.replies', {})
        return text in replies

    def process(self, main, message):
        text = message.message.replace('.', '{:}')
        if main.options.get('options.autoreply.strip', False):
            text = text.strip()
        if main.options.get('options.autoreply.lower', False):
            text = text.lower()
        replies = main.options.get('options.autoreply.replies', {})
        reply = replies.get(text, None)
        if reply:
            random.seed(time.time())
            reply = random.choice(reply)
            reply = reply.replace('{<}', '[')
            reply = reply.replace('{>}', ']')
            reply = reply.replace('{group}', str(message.group))
            reply = reply.replace('{user}', str(message.user))
            reply = reply.replace('{id}', str(message.id))
            reply = reply.replace('{message}', message.message)
            message.send(main, reply)