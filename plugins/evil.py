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
from random import choice


class Evil(BotPlugin):
    """Evil little bastard stuff"""

    __klug_items = ["einen Lolli", "einen Keks", "einen Orden",
                    "eine goldene Waschmaschine"]

    # Don't overuse the "cool" stuff!
    __legendaer_items = [("It's gonna be legend-... wait for it... and I hope you're \
not lactose intolerant because the second half of that word is DAIRY!", 1),
                         ("""Don't say that! You're too liberal with the \
word "legendary".""", 1),
                         ("It's gonna be legen... wait for it... dary!", 10)]
    __legendaer = [val for val, cnt in __legendaer_items for i in range(cnt)]

    @botcmd(split_args_with=None)
    def klug(self, msg, args):
        """Tell someone how smart he is"""
        if args:
            if len(args) != 1:
                return "Meine kleinen Schaltkreise koennen so viel Intelligenz \
nicht verkraften!"
            else:
                name = args[0]
                return "Kluges {0}! Hier hast du {1}!".format(
                    name, choice(self.__klug_items)
                )
        else:
            return "Du bist so Kluk! K - L - U - K!"

    @botcmd(split_args_with=None)
    def next(self, msg, args):
        """Everything done"""
        return u"Ein weiter zufriedener Kunde. NAECHSTER!"

    @botcmd(split_args_with=None)
    def armer(self, msg, args):
        """Poor person"""
        if len(args) == 1:
            return "Armes {0}. Brauchst du ein Taschentuch?".format(args[0])
        elif len(args) > 1:
            return "Braucht ihr Mitleid? Ich koennte welches vortaeuschen..."
        else:
            return "Oooh. Hast du dir weh getan?"

    @botcmd(split_args_with=None)
    def easy(self, msg, args):
        """That was easy"""
        return "Das war ja einfach..."

    @botcmd(split_args_with=None)
    def haha(self, msg, args):
        """gleefull laughter"""
        return "Ha-ha! (C Nelson Muntz)"

    @botcmd(split_args_with=None)
    def legendary(self, msg, args):
        """Do the Barney S."""
        return choice(self.__legendaer)
