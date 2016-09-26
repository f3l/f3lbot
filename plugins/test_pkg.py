# F3LBot - ErrBot Plugins for use with f3l
# Copyright (C) 2015  The F3L-Team,
#                     Oliver Ruempelein <oli_r(at)fg4f.de>
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
from f3lhelpers import dialogtest, get_plugin


class TestPkg(object):
    extra_plugin_dir = "."

    def test_print_packages(self, testbot):
        plugin = get_plugin(testbot, 'Pkg')
        # Single package
        expected = 'test1:\tJust testing'
        result = plugin._Pkg__print_packages(
            [
                {
                    'repo': 'test1',
                    'name': 'test1',
                    'desc': 'Just testing',
                }
            ]
        )
        assert expected == result
        # Multi packages
        expected = 'Foo!test1-test1:\tJust testing\ntest2-test2:\t\
Also just testing'
        result = plugin._Pkg__print_packages(
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
        assert expected == result

    def test_query_aur(self, testbot):
        plugin = get_plugin(testbot, 'Pkg')
        result = plugin._Pkg__query_aur('x32edit', 'info')
        assert type(result) is dict and type(result['results']) is dict

    def test_parse_aur_multi(self, testbot):
        # Multiple returns
        plugin = get_plugin(testbot, 'Pkg')
        input = plugin._Pkg__query_aur('pheerai', 'msearch')
        result = plugin._Pkg__parse_aur_multi(input)
        assert type(result) is list \
            and type(result[1]) is dict \
            and type(result[1]["name"]) is str
        # Single return
        plugin = get_plugin(testbot, 'Pkg')
        input = plugin._Pkg__query_aur('x32edit', 'info')
        result = plugin._Pkg__parse_aur_single(input["results"])
        assert type(result) is dict \
            and type(result["name"]) is str

    # Here, the "ugly unit tests" start: They are
    # __DEPENDENT ON OTHER SERVICES__
    # (Don't like it, but hey...)

    def test_aur_info(self, testbot):
        # Missing argument
        dialogtest(
            testbot,
            '!aur info',
            'Please specify a keyword.'
        )

        # With valid argument
        dialogtest(
            testbot,
            '!aur info x32edit',
            'x32edit:    Remote control and programm \
Behringer X32 consoles'
        )

        # Valid argument, no result:
        dialogtest(
            testbot,
            '!aur info foobar_baz',
            'foobar_baz was not found, \
or something else went wrong. Sorry.'
        )

    def test_aur_search(self, testbot):
        # Missing argument
        dialogtest(
            testbot,
            '!aur search',
            'Please specify a keyword.'
        )

        # Valid argument + result:
        dialogtest(
            testbot,
            '!aur search x32edit',
            '1 matching packages found.\n\
x32edit:    Remote control and programm \
Behringer X32 consoles'
        )

        # No search result:
        dialogtest(
            testbot,
            '!aur search foobarbaz',
            'No package matching your query found.'
        )

    def test_aur_maint(self, testbot):
        # Missing argument
        dialogtest(
            testbot,
            '!aur maint',
            'Please specify a keyword.'
        )

        # Valid argument + result
        dialogtest(
            testbot,
            '!aur maint pheerai',
            '4 packages maintained by pheerai found.\n\
x32edit:    Remote control and programm Behringer X32 consoles\n\
python-pytest-pep8: pytest plugin to check PEP8 requirements.\n\
xprofile:   A tool to manage and automatically apply xrandr configurations.\n\
mergerfs:   Another FUSE union filesystem'
        )

        # Valid argument, no result
        dialogtest(
            testbot,
            '!aur maint foobarbaz',
            'No packages maintained by foobarbaz found.'
        )

    def test_query_arch(self, testbot):
        plugin = get_plugin(testbot, 'Pkg')
        result = plugin._Pkg__query_arch('name', '0ad')
        assert type(result) is dict \
            and result["valid"] is True \
            and type(result["results"]) is list \
            and type(result["results"][0]) is dict

    def test_parse_arch_multi(self, testbot):
        plugin = get_plugin(testbot, 'Pkg')
        result = plugin._Pkg__query_arch('name', '0ad')
        result2 = plugin._Pkg__parse_arch_multi(result["results"])
        assert type(result2) is list \
            and type(result2[0]) is dict \
            and type(result2[0]["name"]) is str

    def test_arch_info(self, testbot):
        # No argument
        dialogtest(
            testbot,
            '!arch info',
            'Please specify a keyword.'
        )

        # Valid Argument, hit
        dialogtest(
            testbot,
            '!arch info 0ad',
            'community/0ad:  Cross-platform, 3D and \
historically-based real-time strategy game'
        )

        # Valid Argument, no hit
        dialogtest(
            testbot,
            '!arch info foobarbaz',
            'foobarbaz was not found, or something \
else went wrong. Sorry.'
        )

    def test_arch_search(self, testbot):
        # No Argument
        dialogtest(
            testbot,
            '!arch search',
            'Please specify a keyword.'
        )

        # Valid Argument, no hit
        dialogtest(
            testbot,
            '!arch search 0ad',
            # Using the Messages, \t gets replaced.
            "1 matching packages found.\n\
community/0ad:  Cross-platform, 3D and historically-based \
real-time strategy game"
        )

        # Valid arg, no result
        dialogtest(
            testbot,
            '!arch search foobarbaz',
            'No package matching your query found.'
        )

    def test_arch_maint(self, testbot):
        # No argument
        dialogtest(
            testbot,
            '!arch maint',
            'Please specify a keyword.'
        )
        # No Dialogtest, we want to map using in!
        testbot.push_message('!arch maint faidoc')
        expected = ' packages maintained by faidoc found.\n\
cinnamon'
        result = testbot.pop_message()
        assert expected in result
        # Single arg without match
        dialogtest(
            testbot,
            '!arch maint foobarbaz',
            'No packages maintained by foobarbaz found.'
        )

    def test_pkg_search(self, testbot):
        dialogtest(
            testbot,
            '!pkg search',
            'Please specify a keyword.'
        )
        dialogtest(
            testbot,
            '!pkg search python-systemd',
            '2 matching packages found.\n\
extra/python-systemd:   Python bindings for systemd\n\
aur/python-systemd-git: Systemd python bindings'
        )
        dialogtest(
            testbot,
            '!pkg search foobarbaz',
            'Sorry, no matching packages found.'
        )
