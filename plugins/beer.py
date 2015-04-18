from errbot import BotPlugin, botcmd, utils, re_botcmd
import re

class Beer(BotPlugin):
	"""Example: Hand out Beer"""

	def __printargs(self,args):
		if args:
			return " "+" ".join(args)+" "
		else:
			return " "
	
	@botcmd(split_args_with=None)
	def beer(self,msg,args):
		"""Get beer from the cellar, optional specify properties"""
		return "/me goes to the cellar and returns, carrying a{}beer for {}.".format(self.__printargs(args),utils.get_sender_username(msg))
	
	# @re_botcmd(pattern=r"(^| )b(i|e)er?( |$)", prefixed=False, flags=re.IGNORECASE)
	# def listen_beer(self,msg,match):
	# 	"""Did Someone mention Beer?"""
	# 	return "We DO have beer, just tell me with !beer"

	@botcmd(split_args_with=None)
	def beer_for(self,msg,args):
		"""Get beer from the cellar, hand to someone else"""
		return "/me goes to the cellar and returns, carrying a{}beer for {}.".format(self.__printargs(args[1:]),args[0])
	
