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
from f3lhelpers import dialogtest, get_plugin
import redis


class TestCite(object):
    """Test the Cite-plugin"""
    extra_plugin_dir = "."
    # This must match the dbKey from cites.py.
    # Don't test on system that are in production!
    dbKey = "Cites"
    db = redis.StrictRedis(host='localhost', port=6379, db=0)

    def test_prepare(self):
        if (self.db.zcard != 0):
            self.db.zremrangebyrank(self.dbKey, 0, -1)

    # First: Remove the key! (Can't be in init, because then things aren't run)
    def test_dblen(self, testbot):
        plugin = get_plugin(testbot, 'Cite')
        assert(plugin.dblen == 0)
        self.db.zadd(self.dbKey,
                     1,
                     "Foo")
        assert(plugin.dblen == 1)

    # Content of DB: "Foo"
    def test_get_element(self, testbot):
            plugin = get_plugin(testbot, 'Cite')
            # 1st: index out of bounds
            assert(plugin._Cite__get_element(-1) == "Invalid index")
            assert(plugin._Cite__get_element(1) == "Invalid index")
            # 3rd: Index in bounds
            assert(plugin._Cite__get_element(0) == "Foo")

    # Content of DB: "Foo"
    def test_get_random_cite(self, testbot):
            plugin = get_plugin(testbot, 'Cite')
            # 1st: get random (here: only) quote
            assert(plugin._Cite__random_cite() == "Foo")
            # 2nd: Empty DB
            self.db.zremrangebyrank(self.dbKey, 0, -1)
            assert(plugin._Cite__random_cite() == "No cites in DB")

    # Content of DB: None
    def test_cite_add(self, testbot):
        dialogtest(testbot, "!cite add", "Invalid usage. You must add a quote")
        dialogtest(testbot,
                   "!cite add Foo\nBar",
                   "Sucessfully added the quote")

    def test_cite_get(self, testbot):
        dialogtest(testbot,
                   "!cite get",
                   "Invalid usage. This command takes exactly one parameter")
        dialogtest(testbot, "!cite get 1", "Foo – Bar")
        dialogtest(testbot, "!cite get a", "This command takes one integer only")
        dialogtest(testbot, "!cite random", "Foo – Bar")
