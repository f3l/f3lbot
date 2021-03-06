# coding=utf-8
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

# noinspection PyUnresolvedReferences
from errbot.backends.test import testbot
from f3lhelpers import dialog_test, get_plugin


# noinspection PyClassHasNoInit,PyShadowingNames
class TestEvil:
    extra_plugin_dir = "."

    def test_klug(self, testbot):
        # empty
        dialog_test(
            testbot,
            '!klug',
            'Du bist so Kluk! K – L – U – K!'
        )
        # 1 arg:
        # Random, thus "in"!
        testbot.push_message('!klug pheerai')
        expected = 'Kluges pheerai! Hier hast du '
        result = testbot.pop_message()
        assert expected in result
        # 2 args:
        dialog_test(
            testbot,
            '!klug pheerai asdil1991',
            "Meine kleinen Schaltkreise können so viel Intelligenz \
nicht verkraften!"
        )

    def test_next(self, testbot):
        dialog_test(
            testbot,
            '!next',
            "Ein weiter zufriedener Kunde. NÄCHSTER!"
        )

    def test_armer(self, testbot):
        # empty
        dialog_test(
            testbot,
            '!armer',
            'Oooh. Hast du dir weh getan?'
        )
        # Nick specified
        dialog_test(
            testbot,
            '!armer pheerai',
            'Armes pheerai. Brauchst du ein Taschentuch?'
        )
        # Several nicks:
        dialog_test(
            testbot,
            '!armer pheerai asdil1991',
            'Braucht ihr Mitleid? Ich könnte welches vortäuschen…'
        )

    def test_easy(self, testbot):
        dialog_test(
            testbot,
            '!easy',
            'Das war ja einfach…'
        )

    def test_haha(self, testbot):
        dialog_test(
            testbot,
            '!haha',
            'Ha-ha! (© Nelson Muntz)'
        )

    def test_legendary(self, testbot):
        # Has random, thus manually
        plugin = get_plugin(testbot, 'Evil')
        testbot.push_message("!legendary")
        result = testbot.pop_message()
        expected = plugin._Evil__legendaer
        assert result in expected
