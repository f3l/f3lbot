from errbot import BotPlugin, botcmd, utils, re_botcmd
import re


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
for {}.".format(
                        self.__printargs(args),
                        utils.get_sender_username(msg),
                )

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
                        utils.get_sender_username(msg)
                )

    @botcmd(split_args_with=None)
    def give_to(self, msg, args):
        """Give 'something' to 'someone'"""
        num = self.__evalto(args)
        return "/me gives{}to {}.".format(
                        self.__printargs(args[2*num-1:]),
                        self.__printto(args, num)
                )

    @re_botcmd(pattern=r"(^| )b(i|e)er?( |$)",
               prefixed=False,
               flags=re.IGNORECASE)
    def listen_beer(self, msg, match):
        """Did Someone mention Beer?"""
        return "We DO have beer, just tell me with !beer"
