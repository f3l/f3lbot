from errbot import BotPlugin, botcmd
from urllib.parse import urlencode # For UTF8 support
import requests

class Aur(BotPlugin):
	"""Search and query AUR by XMPP"""

	query_key="arg"

	def __query_api(self,query,query_type):
		"""Perform a single query on the AUR API.

query: parameters
query_type: one of "info", "search", "msearch"

returns: dictionary containing the JSON-Data
"""
		query_handle = requests.get(
			"https://aur.archlinux.org/rpc.php?" + urlencode({
				"type": query_type,
				self.query_key: query
				}, doseq=True)
		)
		return query_handle.json()
		
		
	@botcmd
	def aur_info(self,msg,args):
		"""Print Package description, if it exists"""
		query_content=self.__query_api(args,"info")
		if query_content["resultcount"]==1:
			query_package=query_content["results"]
			return query_package["Name"] + ":\n" + query_package["Description"]
		else:
			return args + " was not found, or something else went wrong. Sorry."
	
	@botcmd
	def aur_search(self,msg,args):
		"""Searches for AUR packages"""
		return "Not implemented yet."

	@botcmd
	def aur_maint(self,msg,args):
		"""Searches for AUR Maintainers"""
		return "Not implemented yet."
	
