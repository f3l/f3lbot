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

from errbot.backends.test import testbot, push_message, pop_message
from errbot import plugin_manager


class TestGive(object):
    extra_plugin_dir = "."

    def test_evalto(self, testbot):
        plugin = plugin_manager.get_plugin_obj_by_name('Give')
        expected = [1, 3]
        result = [
            plugin._Give__evalto(['asdil1991']),
            plugin._Give__evalto(['asdil1991', 'and', 'pheerai',
                                  'and', 'asdil12', 'cool', 'büchenbacher'])
        ]
        assert result == expected

    def test_printargs(self, testbot):
        plugin = plugin_manager.get_plugin_obj_by_name('Give')
        expected = [" ", " 1 2 3 "]
        result = [plugin._Give__printargs([]),
                  plugin._Give__printargs(["1", "2", "3"])]
        assert result == expected

    def test_printto(self, testbot):
        plugin = plugin_manager.get_plugin_obj_by_name('Give')
        expected = ['asdil1991', 'asdil1991 and pheerai and asdil12']
        result = [plugin._Give__printto(["asdil1991"], 1),
                  plugin._Give__printto(["asdil1991", "and", "pheerai",
                                         "and", "asdil12"], 3)]
        assert expected == result

    def test_beer_1(self, testbot):
        push_message('!beer')
        expected = '/me goes to the cellar and returns, carrying a beer \
for gbin.'
        result = pop_message()
        assert expected in result

    def test_beer_2(self, testbot):
        push_message('!beer cool büchenbacher')
        expected = '/me goes to the cellar and returns, carrying a cool \
büchenbacher beer for gbin.'
        result = pop_message()
        assert expected in result

    def test_beer_for_1(self, testbot):
        push_message('!beer for asdil1991')
        expected = '/me goes to the cellar and returns, carrying a beer \
for asdil1991.'
        result = pop_message()
        assert expected in result

    def test_beer_for_2(self, testbot):
        push_message('!beer for asdil1991 and pheerai and asdil12 \
cool Büchenbacher')
        expected = '/me goes to the cellar and returns, carrying a \
cool Büchenbacher beer for asdil1991 and pheerai and asdil12.'
        result = pop_message()
        assert expected in result

    def test_give_1(self, testbot):
        push_message('!give')
        expected = '/me gives a to gbin.'
        result = pop_message()
        assert expected in result

    def test_give_2(self, testbot):
        push_message('!give sweet chocolate')
        expected = '/me gives a sweet chocolate to gbin.'
        result = pop_message()
        assert expected in result

    def test_give_to_1(self, testbot):
        push_message('!give to asdil1991')
        expected = '/me gives to asdil1991.'
        result = pop_message()
        assert expected in result

    def test_give_to_2(self, testbot):
        push_message('!give to asdil1991 and pheerai and asdil12 \
salty gulasch')
        expected = '/me gives salty gulasch to asdil1991 and pheerai \
and asdil12.'
        result = pop_message()
        assert expected in result

    def test_listen_beer(self, testbot):
        push_message('Ich trinke ein kühles Bier')
        expected = 'We DO have beer, just tell me with !beer'
        result = pop_message()
        assert expected in result
