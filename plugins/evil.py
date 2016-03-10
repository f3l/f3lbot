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
from random import randrange


class Evil(BotPlugin):
    """Evil little bastard stuff"""

    __klug_items = ["einen Lolli", "einen Keks", "einen Orden",
                    "eine goldene Waschmaschine"]

    def get_klug_items(self):  # pragma: no cover
        index = randrange(0, len(self.__klug_items))
        return self.__klug_items[index]

    @botcmd(split_args_with=None)
    def klug(self, msg, args):
        """Tell someone how smart he is"""
        if args:
            name = args[0]
            return "Kluges {0}! Hier hast du {1}!".format(
                name, self.get_klug_items())
        else:
            return "Du bist so Kluk! K – L – U – K!"

    @botcmd(split_args_with=None)
    def next(self, msg, args):
        """Everything done"""
        return "Ein weiter zufriedener Kunde. NÄCHSTER!"

    @botcmd(split_args_with=None)
    def armer(self, msg, args):
        """Poor person"""
        if args:
            return "Armes {0}. Brauchst du ein Taschentuch?".format(args[0])
        else:
            return "Oooh. Hast du dir weh getan?"
