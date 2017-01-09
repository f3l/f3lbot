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
from f3lhelpers import peer_account_name


class Give(BotPlugin):
    """Example: Hand out Beer"""

    def __evalto(self, args):
        """Count number of given names, seperated by 'and'

        Args:
        args: List of strings
        Returns:
        Integer with number of names
        """
        num = 1
        for i in range(1, len(args), 2):
            if args[i] == "and":
                num += 1
            else:
                break
        return num

    def __printargs(self, args):
        """Print args as string if given

        Args:
          args: List of strings
        Returns:
          String for in-sentence use.
        """
        if args:
            return " " + " ".join(args) + " "
        else:
            return " "

    def __printto(self, args, num):
        """Print user string, with users seperated by 'and'.

        Args:
          args: List of strings
          num: Numbers of names
        Returns:
          String for end-of-sentence-use
        """
        str = args[0]
        for i in range(2, 2*num, 2):
            str += " and " + args[i]
        return str

    @botcmd(split_args_with=None)
    def beer(self, msg, args):
        """Get beer from the cellar, optional specify properties"""
        return "/me goes to the cellar and returns, carrying a{}beer \
for {}.".format(self.__printargs(args),
                peer_account_name(msg))

    @botcmd(split_args_with=None)
    def beer_for(self, msg, args):
        """Get beer from the cellar, hand to someone else"""
        num = self.__evalto(args)
        return "/me goes to the cellar and returns, \
carrying a{}beer for {}.".format(
                        self.__printargs(args[2*num-1:]),
                        self.__printto(args, num),
                )

    @botcmd(split_args_with=None)
    def give(self, msg, args):
        """Give 'something' to yourself"""
        return "/me gives a{}to {}.".format(
            self.__printargs(args),
            peer_account_name(msg))

    @botcmd(split_args_with=None)
    def give_to(self, msg, args):
        """Give 'something' to 'someone'"""
        num = self.__evalto(args)
        return "/me gives{}to {}.".format(
                        self.__printargs(args[2*num-1:]),
                        self.__printto(args, num)
                )
