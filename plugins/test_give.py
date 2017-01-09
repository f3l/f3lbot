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

from errbot.backends.test import testbot
from f3lhelpers import dialog_test, get_plugin


class TestGive(object):
    extra_plugin_dir = "."

    def test_evalto(self, testbot):
        plugin = get_plugin(testbot, 'Give')
        expected = [1, 3]
        result = [
            plugin._Give__evalto(['asdil1991']),
            plugin._Give__evalto(['asdil1991', 'and', 'pheerai',
                                  'and', 'asdil12', 'cool', 'büchenbacher'])
        ]
        assert result == expected

    def test_printargs(self, testbot):
        plugin = get_plugin(testbot, 'Give')
        expected = [" ", " 1 2 3 "]
        result = [plugin._Give__printargs([]),
                  plugin._Give__printargs(["1", "2", "3"])]
        assert result == expected

    def test_printto(self, testbot):
        plugin = get_plugin(testbot, 'Give')
        expected = ['asdil1991', 'asdil1991 and pheerai and asdil12']
        result = [plugin._Give__printto(["asdil1991"], 1),
                  plugin._Give__printto(["asdil1991", "and", "pheerai",
                                         "and", "asdil12"], 3)]
        assert expected == result

    def test_beer_1(self, testbot):
        dialog_test(
            testbot,
            '!beer',
            '/me goes to the cellar and returns, carrying a beer \
for None.'
        )
        dialog_test(
            testbot,
            '!beer cool büchenbacher',
            '/me goes to the cellar and returns, carrying a cool \
büchenbacher beer for None.'
        )

    def test_beer_for_1(self, testbot):
        dialog_test(
            testbot,
            '!beer for asdil1991',
            '/me goes to the cellar and returns, carrying a beer \
for asdil1991.'
        )

    def test_beer_for_2(self, testbot):
        dialog_test(
            testbot,
            '!beer for asdil1991 and pheerai and asdil12 \
cool Büchenbacher',
            '/me goes to the cellar and returns, carrying a \
cool Büchenbacher beer for asdil1991 and pheerai and asdil12.'
            )

    def test_give(self, testbot):
        dialog_test(
            testbot,
            '!give',
            '/me gives a to None.'
        )
        dialog_test(
            testbot,
            '!give sweet chocolate',
            '/me gives a sweet chocolate to None.'
        )

    def test_give_to(self, testbot):
        # give to 1 person
        dialog_test(
            testbot,
            '!give to asdil1991',
            '/me gives to asdil1991.'
        )
        # Give to multiple persons
        dialog_test(
            testbot,
            '!give to asdil1991 and pheerai and asdil12 \
salty gulasch',
            '/me gives salty gulasch to asdil1991 and pheerai \
and asdil12.'
            )
