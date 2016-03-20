# F3LBot – ErrBot Plugins for use with f3l
# Copyright (C) 2015  The F3L-Team,
#                     Oliver Rümpelein <oli_r(at)fg4f.de>
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
from random import randint
import redis


class Cite(BotPlugin):
    """API to the F3LCite system"""

    db = redis.StrictRedis(host='localhost', port=6379, db=0)
    dbKey = "Cites"

    @property
    def dblen(self):
        """Returns the number of elements in the ordered set"""
        return self.db.zcard(self.dbKey)

    def __get_element(self, index):
        """Get a single element.

Checks, if index lies within range, and whether the key is valid
"""
        if (0 <= index) and (index < self.dblen):
            reply = self.db.zrange(self.dbKey, index, index)
            if (len(reply) == 1):
                return reply[0].decode("utf-8")
            elif (len(reply) == 0):
                return "No quote with this key found"
            else:
                self.log.error("DB corrupted, key used multiple times!")
                return "Something went horribly wrong!"
        else:
            return "Invalid index"

    def __random_cite(self):
        """Return a random quote"""
        zlen = self.db.zcard(self.dbKey)
        if (zlen == 0):
            return "No cites in DB"
        else:
            # randint has inclusive end!
            ranIndex = randint(0, zlen-1)
            return self.__get_element(ranIndex)

    @botcmd(split_args_with=None)
    def cite_random(self, msg, args):
        """Get random cite from DB"""
        return self.__random_cite()

    @botcmd(split_args_with=None)
    def cite_get(self, msg, args):
        """Get msg with given index from DB"""
        if (len(args) != 1):
            return "Invalid usage. This command takes exactly one parameter"
        index = int(args[0])
        if not type(index) is int:
            return "This command takes one integer only"
        else:
            return self.__get_element(index - 1)

    @botcmd()
    def cite_add(self, msg, args):
        """Insert quote into DB"""
        if not args:
            return "Invalid usage. You must add a quote"
        else:
            quote = args.replace("\r\n", " – ")\
                        .replace("\r", " – ")\
                        .replace("\n", " – ")\
                        .encode("utf-8")
            added = self.db.zadd(self.dbKey,
                                 self.dblen,
                                 quote)
            if added == 1:
                return "Sucessfully added the quote"
            else:
                return "Seems like something went wrong"
