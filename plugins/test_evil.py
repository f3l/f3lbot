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
        # Nick specified
        testbot.push_message('!klug pheerai')
        expected = 'Kluges pheerai! Hier hast du einen '
        result = testbot.pop_message()
        assert expected in result
