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
from f3lhelpers import dialog_test, dialog_contains_test, get_plugin


# noinspection PyClassHasNoInit,PyShadowingNames
class TestPkg:
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
            preamble="Foo!"
        )
        assert expected == result

    def test_query_aur(self, testbot):
        plugin = get_plugin(testbot, 'Pkg')
        result = plugin._Pkg__query_aur('x32edit', 'info')
        assert type(result) is dict and type(result['results']) is dict

    def test_parse_aur_multi(self, testbot):
        # Multiple returns
        plugin = get_plugin(testbot, 'Pkg')
        test_input = plugin._Pkg__query_aur('pheerai', 'msearch')
        result = plugin._Pkg__parse_aur_multi(test_input)
        assert type(result) is list \
            and type(result[1]) is dict \
            and type(result[1]["name"]) is str
        # Single return
        plugin = get_plugin(testbot, 'Pkg')
        test_input = plugin._Pkg__query_aur('x32edit', 'info')
        result = plugin._Pkg__parse_aur_single(test_input["results"])
        assert type(result) is dict \
            and type(result["name"]) is str

    # Here, the integration tests start: They are
    # __DEPENDENT ON OTHER SERVICES__
    # (Don't like it, but hey…)

    def test_aur_info(self, testbot):
        # Missing argument
        dialog_test(
            testbot,
            '!aur info',
            'Please specify a keyword.'
        )

        # With valid argument
        dialog_contains_test(
            testbot,
            '!aur info x32edit',
            'x32edit:    Remote control and programm \
Behringer X32 consoles'
        )

        # Valid argument, no result:
        dialog_test(
            testbot,
            '!aur info foobar_baz',
            'foobar_baz was not found, \
or something else went wrong. Sorry.'
        )

    def test_aur_search(self, testbot):
        # Missing argument
        dialog_test(
            testbot,
            '!aur search',
            'Please specify a keyword.'
        )

        # Valid argument + result:
        dialog_contains_test(
            testbot,
            '!aur search x32edit',
            ' matching packages found.\n'
        )

        # No search result:
        dialog_test(
            testbot,
            '!aur search foobarbaz',
            'No package matching your query found.'
        )

    def test_aur_maint(self, testbot):
        # Missing argument
        dialog_test(
            testbot,
            '!aur maint',
            'Please specify a keyword.'
        )

        # Valid argument + result
        dialog_contains_test(
            testbot,
            '!aur maint pheerai',
            ' packages maintained by pheerai found.\n'
        )

        # Valid argument, no result
        dialog_test(
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
        dialog_test(
            testbot,
            '!arch info',
            'Please specify a keyword.'
        )

        # Valid Argument, hit
        dialog_contains_test(
            testbot,
            '!arch info 0ad',
            'community/0ad: '
        )

        # Valid Argument, no hit
        dialog_test(
            testbot,
            '!arch info foobarbaz',
            'foobarbaz was not found, or something \
else went wrong. Sorry.'
        )

    def test_arch_search(self, testbot):
        # No Argument
        dialog_test(
            testbot,
            '!arch search',
            'Please specify a keyword.'
        )

        # Valid Argument, no hit
        dialog_contains_test(
            testbot,
            '!arch search 0ad',
            # Using the Messages, \t gets replaced.
            " matching packages found.\n"
        )

        # Valid arg, no result
        dialog_test(
            testbot,
            '!arch search foobarbaz',
            'No package matching your query found.'
        )

    def test_arch_maint(self, testbot):
        # No argument
        dialog_test(
            testbot,
            '!arch maint',
            'Please specify a keyword.'
        )
        # No Dialogtest, we want to map using in!
        dialog_contains_test(
            testbot,
            '!arch maint faidoc',
            ' packages maintained by faidoc found.\n'
        )
        # Single arg without match
        dialog_test(
            testbot,
            '!arch maint foobarbaz',
            'No packages maintained by foobarbaz found.'
        )

    def test_pkg_search(self, testbot):
        dialog_test(
            testbot,
            '!pkg search',
            'Please specify a keyword.'
        )
        dialog_contains_test(
            testbot,
            '!pkg search python-systemd',
            ' matching packages found.\n'
        )
        dialog_test(
            testbot,
            '!pkg search foobarbaz',
            'Sorry, no matching packages found.'
        )
