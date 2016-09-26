# F3LBot - ErrBot Plugins for use with f3l
# Copyright (C) 2015  The F3L-Team,
#                     Oliver Ruempelein <oli_r(at)fg4f.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from errbot import BotPlugin, botcmd
from urllib.parse import urlencode  # For UTF8 support
import requests


class Pkg(BotPlugin):
    """Search and query Arch-Repos via XMPP"""

    # Global Stuff
    #

    def __print_packages(self, results, repo=False, sep="/", preamb=""):
        """Convert parsed JSON from below into a printable form.

        results: Output of __parse_* from this module
        repo: (Bool) Whether the repo of the packages should be printed
        sep: Separator between repo and package
        preamb: A preamble string

        returns: String
        """
        pkgstrings = []
        if repo:
            for i in results:
                pkgstrings.append(i["repo"]+sep+i["name"]+":\t"+i["desc"])
        else:
            for i in results:
                pkgstrings.append(i["name"]+":\t"+i["desc"])
        return preamb + "\n".join(pkgstrings)

    # Aur-Stuff
    #

    query_key = "arg"

    def __query_aur(self, query, query_type):
        """Perform a single query on the AUR API.

        query: parameters
        query_type: one of "info", "search", "msearch"

        returns: dictionary containing the JSON-Data
        """
        query_handle = requests.get(
            "https://aur.archlinux.org/rpc.php?" + urlencode({
                "type": query_type,
                self.query_key: query,
            }, doseq=True)
        )
        return query_handle.json()

    def __parse_aur_multi(self, json):
        """Parse AUR-Jsonobject and prepare for print

        json: interpreted handle from __query_aur

        returns: Array of dicts with "name", "desc" and "repo"="aur"
        """
        retval = []
        for i in json['results']:
            retval.append(self.__parse_aur_single(i))
        return retval

    def __parse_aur_single(self, json):
        return {"name": json["Name"],
                "desc": json["Description"],
                "repo": "aur"}

    @botcmd
    def aur_info(self, msg, args):
        """Print Package description, if it exists

        msg: Message as passed by ErrBot
        args: Arguments as passed by ErrBot

        returns: String (either error or query result)
        """
        if args == "":
            return "Please specify a keyword."
        query_content = self.__query_aur(args, "info")
#        return query_content
        if query_content["resultcount"] == 1:
            # Evil hack: AUR parses this shit different if only one result...
            query_parsed = [self.__parse_aur_single(query_content["results"])]
            return self.__print_packages(query_parsed)
        else:
            return args + " was not found, or something else \
went wrong. Sorry."

    @botcmd
    def aur_search(self, msg, args):
        """Searches for AUR packages

        msg: Message as passed by ErrBot
        args: Arguments as passed by ErrBot

        returns: String (either error or query result)
        """
        if args == "":
            return "Please specify a keyword."
        query_content = self.__query_aur(args, "search")
        if query_content["resultcount"] == 0:
            return "No package matching your query found."
        else:
            query_parsed = self.__parse_aur_multi(query_content)
            return self.__print_packages(
                query_parsed,
                preamb=str(query_content["resultcount"]) +
                " matching packages found.\n"
            )

    @botcmd
    def aur_maint(self, msg, args):
        """Searches for AUR Maintainers

        msg: Message as passed by ErrBot
        args: Arguments as passed by ErrBot

        returns: String (either error or query result)
        """
        if args == "":
            return "Please specify a keyword."
        query_content = self.__query_aur(args, "msearch")
        if query_content["resultcount"] == 0:
            return "No packages maintained by " + args + " found."
        else:
            query_parsed = self.__parse_aur_multi(query_content)
            return self.__print_packages(
                query_parsed,
                preamb=str(query_content["resultcount"]) +
                " packages maintained by "+args+" found.\n"
            )

    # Arch-Stuff
    #

    def __query_arch(self, query, query_type):
        """Perform a single query on the Arch API.

        query: parameters
        query_type: one of "name", "q", "maintainer"

        returns: dictionary containing the JSON-Data
        """
        query_handle = requests.get(
            "https://www.archlinux.org/packages/search/json/?" + urlencode({
                query_type: query,
                "arch": "x86_64",
            }, doseq=True)
        )
        return query_handle.json()

    def __parse_arch_multi(self, json):
        """Parse AUR-Jsonobject and prepare for print

        json: interpreted handle from __query_aur

        returns: Array of dicts with "name", "desc" and "repo"="aur"
        """
        retval = []
        for i in json:
            retval.append({
                "name": i["pkgname"],
                "desc": i["pkgdesc"],
                "repo": i["repo"]
            })
        return retval

    @botcmd
    def arch_info(self, msg, args):
        """Print Package description, if it exists

        msg: Message as passed by ErrBot
        args: Arguments as passed by ErrBot

        returns: String (either error or query result)
        """
        if args == "":
            return "Please specify a keyword."
        query_content = self.__query_arch(args, "name")
        query_packages = query_content["results"]
        if len(query_packages) == 0:
            return args + " was not found, or something else \
went wrong. Sorry."
        else:
            query_packages = self.__parse_arch_multi(query_packages)
            return self.__print_packages(query_packages, repo=True)

    @botcmd
    def arch_search(self, msg, args):
        """Searches for Arch packages

        msg: Message as passed by ErrBot
        args: Arguments as passed by ErrBot

        returns: String (either error or query result)
        """
        if args == "":
            return "Please specify a keyword."
        query_content = self.__query_arch(args, "q")
        query_packages = query_content["results"]
        if len(query_packages) == 0:
            return "No package matching your query found."
        else:
            query_packages = self.__parse_arch_multi(query_packages)
            return self.__print_packages(
                query_packages,
                repo=True,
                preamb=str(len(query_packages)) + " matching packages found.\n"
            )

    @botcmd
    def arch_maint(self, msg, args):
        """Searches for ARCH Maintainers

        msg: Message as passed by ErrBot
        args: Arguments as passed by ErrBot

        returns: String (either error or query result)
        """
        if args == "":
            return "Please specify a keyword."
        query_content = self.__query_arch(args, "maintainer")
        query_packages = query_content["results"]
        if len(query_packages) == 0:
            return "No packages maintained by "+args+" found."
        else:
            query_packages = self.__parse_arch_multi(query_packages)
            return self.__print_packages(
                query_packages,
                preamb=str(len(query_packages)) +
                " packages maintained by "+args+" found.\n"
            )

    # Multi Stuff
    #
    # Fucking ugly...

    @botcmd
    def pkg_search(self, msg, args):
        """Search Arch-Repos + Aur.

        msg: Message as passed by ErrBot
        args: Arguments as passed by ErrBot

        returns: String (either error or query result)
        """
        if args == "":
            return "Please specify a keyword."
        res_parsed = []

        # First, query Arch
        query_content = self.__query_arch(args, "q")
        query_content = query_content["results"]
        if len(query_content) != 0:
            res_parsed += self.__parse_arch_multi(query_content)

        # Then, Aur
        query_content = self.__query_aur(args, "search")
        if query_content["resultcount"] != 0:
            res_parsed += self.__parse_aur_multi(query_content)

        if len(res_parsed) == 0:
            return "Sorry, no matching packages found."
        else:
            return self.__print_packages(
                res_parsed,
                repo=True,
                preamb=str(len(res_parsed)) + " matching packages found.\n"
            )
