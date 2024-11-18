from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message

class Hyp:
    @staticmethod
    async def hyp(matcher: Matcher, event: GroupMessageEvent, arg: Message = CommandArg()):
        command = str(event.get_message()).strip()
        args = str(arg).strip()[1:]
        await matcher.finish(command+args)


        
    
hyp = Hyp()