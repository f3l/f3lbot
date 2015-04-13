from errbot import BotPlugin, botcmd, utils

class Beer(BotPlugin):
	"""Example: Hand out Beer"""

	def __printargs(self,args):
		if args:
			return " "+args+" "
		else:
			return " "
	
	@botcmd
	def beer(self,msg,args):
		"""Get beer from the cellar, optional specify properties"""
		return "/me goes to the cellar and returns, carrying a{}beer for {}.".format(self.__printargs(args),utils.get_sender_username(msg))
