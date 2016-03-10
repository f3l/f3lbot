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


class TestEvil(object):
    extra_plugin_dir = "."

    def test_klug(self, testbot):
        # empty
        testbot.push_message('!klug')
        expected = 'Du bist so Kluk! K – L – U – K!'
        result = testbot.pop_message()
        print(result)
        assert expected == result

    def test_klug_nick(self, testbot):
        # Nick specified
        testbot.push_message('!klug pheerai')
        expected = 'Kluges pheerai! Hier hast du '
        result = testbot.pop_message()
        assert expected in result

    def test_next(self, testbot):
        expected = "Ein weiter zufriedener Kunde. NÄCHSTER!"
        testbot.push_message('!next')
        result = testbot.pop_message()
        assert expected == result

    def test_armer(self, testbot):
        # empty
        testbot.push_message('!armer')
        expected = 'Oooh. Hast du dir weh getan?'
        result = testbot.pop_message()
        print(result)
        assert expected == result

    def test_armer_nick(self, testbot):
        # Nick specified
        testbot.push_message('!armer pheerai')
        expected = 'Armes pheerai. Brauchst du ein Taschentuch?'
        result = testbot.pop_message()
        assert expected in result
