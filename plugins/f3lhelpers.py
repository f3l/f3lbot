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

from errbot import BotPlugin, botcmd, utils


def chattername(msg):
    """Returns the Nick of the sender of a message"""
    if msg.type == 'groupchat':
        return msg.frm.resource  # pragma: no cover
    else:
        return msg.frm.nick


def dialogtest(bot, msg, exp):
    """Easy interface for tests if the form msg => reply
    Arguments:
        bot: A testbot instance
        msg: The message to pass to bot
        exp: Expected outcome
    """
    bot.push_message(msg)
    result = bot.pop_message()
    assert result == exp

def get_plugin(bot, plugin_name):
    plugin = bot.bot.plugin_manager.get_plugin_obj_by_name(plugin_name)
    if (plugin is None): # pragma: no cover
        raise ValueError("""Type of Plugin {} is None! \
Have you forgotten 'extra_plugin_dir="."'?""".format(plugin_name))
    else:
        return plugin
