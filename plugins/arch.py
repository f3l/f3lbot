from errbot import BotPlugin, botcmd
from urllib.parse import urlencode # For UTF8 support
import requests

class Arch(BotPlugin):
	"""Search and query Arch by XMPP"""
	
	def __query_api(self,query,query_type):
		"""Perform a single query on the Arch API.

query: parameters
query_type: one of "info", "search", "msearch"

returns: dictionary containing the JSON-Data
"""
		query_handle = requests.get(
			"https://www.archlinux.org/packages/search/json/?" + urlencode({
				query_type: query
			},
			doseq=True)
		)
		return query_handle.json()
		
		
	@botcmd
	def arch_info(self,msg,args):
		"""Print Package description, if it exists"""
		if args=="":
			return "Please specify a keyword."
		query_content=self.__query_api(args,"name")
		if query_content["resultcount"]==1:
			query_package=query_content["results"]
			return query_package["Name"] + ":\n" + query_package["Description"]
		else:
			return args + " was not found, or something else went wrong. Sorry."
	
	@botcmd
	def arch_search(self,msg,args):
		"""Searches for Arch packages"""
		if args=="":
			return "Please specify a keyword."
		query_content=self.__query_api(args,"q")
		if query_content["resultcount"] == 0:
			return "No package matching your query found"
		else:
			query_str= str(query_content["resultcount"]) + " matching packages found.\n"
			for query_elem in query_content["results"]:
				query_str+= query_elem["Name"] + ":\t" + query_elem["Description"]+"\n"
			return query_str

	@botcmd
	def arch_maint(self,msg,args):
		"""Searches for ARCH Maintainers"""
		if args=="":
			return "Please specify a keyword."
		query_content=self.__query_api(args,"maintainer")
		if query_content["resultcount"] == 0:
			return "No packages maintained by "+args+" found."
		else:
			query_str= str(query_content["resultcount"]) + " packages maintained by "+args+" found.\n"
			for query_elem in query_content["results"]:
				query_str += query_elem["Name"] + ":\t" + query_elem["Description"]+"\n"
			return query_str
