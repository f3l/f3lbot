from errbot.backends.test import testbot, push_message, pop_message
from errbot import plugin_manager


class TestPkg(object):
    extra_plugin_dir = "."

    def test_print_packages(self, testbot):
        plugin = plugin_manager.get_plugin_obj_by_name('Pkg')
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
        plugin = plugin_manager.get_plugin_obj_by_name('Pkg')
        result = plugin._Pkg__query_aur('x32edit', 'info')
        assert type(result) is dict and type(result['results']) is dict

    def test_parse_aur_multi(self, testbot):
        plugin = plugin_manager.get_plugin_obj_by_name('Pkg')
        input = plugin._Pkg__query_aur('pheerai', 'msearch')
        result = plugin._Pkg__parse_aur_multi(input)
        assert type(result) is list \
            and type(result[1]) is dict \
            and type(result[1]["name"]) is str

    def test_parse_aur_single(self, testbot):
        plugin = plugin_manager.get_plugin_obj_by_name('Pkg')
        input = plugin._Pkg__query_aur('x32edit', 'info')
        result = plugin._Pkg__parse_aur_single(input["results"])
        assert type(result) is dict \
            and type(result["name"]) is str

    def test_aur_info(self, testbot):
        push_message('!aur info x32edit')
        expected = 'x32edit:\tRemote control and programm \
Behringer X32 consoles'
        result = pop_message()
        assert expected in result

    def test_aur_search(self, testbot):
        push_message('!aur search x32edit')
        expected1 = '1 matching packages found.\n\
x32edit:\tRemote control and programm \
Behringer X32 consoles'
        result1 = pop_message()
        push_message('!aur search beets-a')
        expected2 = '2 matching packages found.\n\
beets-artistcountry-git:\tBeets plugin to retrieve the country of \
an artist from MusicBrainz.\n\
beets-alternatives-git:\tBeets plugin to manage multiple versions of \
your audio files.'
        result2 = pop_message()
        assert expected1 in result1 and expected2 in result2

    def test_aur_maint(self, testbot):
        push_message('!aur maint pheerai')
        expected = '2 packages maintained by pheerai found.\n\
chordii:\tProgram for generating guitar chord music sheets \
from text files\n\
x32edit:\tRemote control and programm Behringer X32 consoles'
        result = pop_message()
        assert expected == result

    def test_query_arch(self, testbot):
        plugin = plugin_manager.get_plugin_obj_by_name('Pkg')
        result = plugin._Pkg__query_arch('name', '0ad')
        assert type(result) is dict \
            and result["valid"] == True \
            and type(result["results"]) is list \
            and type(result["results"][0]) is dict

    def test_parse_arch_multi(self, testbot):
        plugin = plugin_manager.get_plugin_obj_by_name('Pkg')
        input = plugin._Pkg__query_arch('name', '0ad')
        result = plugin._Pkg__parse_arch_multi(input["results"])
        assert type(result) is list \
            and type(result[0]) is dict \
            and type(result[0]["name"]) is str

    def test_arch_info(self, testbot):
        push_message('!arch info 0ad')
        expected = 'community/0ad:\tCross-platform, 3D and \
historically-based real-time strategy game'
        result = pop_message()
        assert expected in result

    def test_arch_search(self, testbot):
        push_message('!arch search 0ad')
        expected = '1 matching packages found.\n\
community/0ad:\tCross-platform, 3D and historically-based \
real-time strategy game'
        result = pop_message()
        assert expected in result

    def test_arch_maint(self, testbot):
        push_message('!arch maint pheerai')
        expected = 'No packages maintained by pheerai found.'
        result = pop_message()
        assert expected in result

    def test_pkg_search(self, testbot):
        push_message('!pkg search 0ad')
        expected = '2 matching packages found.\n\
community/0ad:\tCross-platform, 3D and historically-based \
real-time strategy game\n\
aur/0ad-git:\tCross-platform, 3D and historically-based real-time \
strategy game'
        result = pop_message()
        assert expected in result
