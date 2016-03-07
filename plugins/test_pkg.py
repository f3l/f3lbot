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


class TestPkg(object):
    extra_plugin_dir = "."

    def test_print_packages(self, testbot):
        plugin = testbot.bot.get_plugin_obj_by_name('Pkg')
        expected1 = 'test1:\tJust testing'
        result1 = plugin._Pkg__print_packages(
            [
                {
                    'repo': 'test1',
                    'name': 'test1',
                    'desc': 'Just testing',
                }
            ]
        )
        expected2 = 'Foo!test1-test1:\tJust testing\ntest2-test2:\t\
Also just testing'
        result2 = plugin._Pkg__print_packages(
            [
                {
                    'repo': 'test1',
                    'name': 'test1',
                    'desc': 'Just testing',
                }, {
                    'repo': 'test2',
                    'name': 'test2',
                    'desc': 'Also just testing',
                }
            ],
            repo=True,
            sep="-",
            preamb="Foo!"
        )
        assert expected1 == result1 and expected2 == result2

    def test_query_aur(self, testbot):
        plugin = testbot.bot.get_plugin_obj_by_name('Pkg')
        result = plugin._Pkg__query_aur('x32edit', 'info')
        assert type(result) is dict and type(result['results']) is dict

    def test_parse_aur_multi(self, testbot):
        plugin = testbot.bot.get_plugin_obj_by_name('Pkg')
        input = plugin._Pkg__query_aur('pheerai', 'msearch')
        result = plugin._Pkg__parse_aur_multi(input)
        assert type(result) is list \
            and type(result[1]) is dict \
            and type(result[1]["name"]) is str

    def test_parse_aur_single(self, testbot):
        plugin = testbot.bot.get_plugin_obj_by_name('Pkg')
        input = plugin._Pkg__query_aur('x32edit', 'info')
        result = plugin._Pkg__parse_aur_single(input["results"])
        assert type(result) is dict \
            and type(result["name"]) is str

    def test_aur_info(self, testbot):
        testbot.push_message('!aur info x32edit')
        expected = 'x32edit:    Remote control and programm \
Behringer X32 consoles'
        result = testbot.pop_message()
        assert expected in result

    def test_aur_search(self, testbot):
        testbot.push_message('!aur search x32edit')
        expected1 = '1 matching packages found.\n\
x32edit:    Remote control and programm \
Behringer X32 consoles'
        result1 = testbot.pop_message()
        testbot.push_message('!aur search beets')
        assert expected1 in result1

    def test_aur_maint(self, testbot):
        testbot.push_message('!aur maint pheerai')
        expected = 'packages maintained by pheerai found.\n'
        result = testbot.pop_message()
        assert expected in result

    def test_query_arch(self, testbot):
        plugin = testbot.bot.get_plugin_obj_by_name('Pkg')
        result = plugin._Pkg__query_arch('name', '0ad')
        assert type(result) is dict \
            and result["valid"] is True \
            and type(result["results"]) is list \
            and type(result["results"][0]) is dict

    def test_parse_arch_multi(self, testbot):
        plugin = testbot.bot.get_plugin_obj_by_name('Pkg')
        input = plugin._Pkg__query_arch('name', '0ad')
        result = plugin._Pkg__parse_arch_multi(input["results"])
        assert type(result) is list \
            and type(result[0]) is dict \
            and type(result[0]["name"]) is str

    def test_arch_info(self, testbot):
        testbot.push_message('!arch info 0ad')
        expected = 'community/0ad:  Cross-platform, 3D and \
historically-based real-time strategy game'
        result = testbot.pop_message()
        assert expected in result

    def test_arch_search(self, testbot):
        testbot.push_message('!arch search 0ad')
        # Using the Messages, \t gets replaced.
        expected = "1 matching packages found.\n\
community/0ad:  Cross-platform, 3D and historically-based \
real-time strategy game"
        result = testbot.pop_message()
        assert expected in result

    def test_arch_maint(self, testbot):
        testbot.push_message('!arch maint pheerai')
        expected = 'No packages maintained by pheerai found.'
        result = testbot.pop_message()
        assert expected in result

    def test_pkg_search(self, testbot):
        testbot.push_message('!pkg search python-systemd')
        expected = '2 matching packages found.\n\
extra/python-systemd:   Python bindings for systemd\n\
aur/python-systemd-git: Systemd python bindings'
        result = testbot.pop_message()
        assert expected == result
