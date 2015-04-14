from errbot import BotPlugin, btcmd

class Aur(BotPlugin):
	"""Search and query AUR by XMPP"""
	
	@botcmd
	def aur_info(self,msg,args):
		"""Print Package description, if it exists"""
		return "Not implemented yet."

	@botcmd
	def aur_search(self,msg,args):
		"""Searches for AUR packages"""
		return "Not implemented yet."

	@botcmd
	def aur_maint(self,msg,args):
		"""Searches for AUR Maintainers"""
		return "Not implemented yet."
