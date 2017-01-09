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

from errbot import BotPlugin, botcmd
from f3lhelpers import peer_account_name
import json


class Cite():
    def __init__(self, id=0, cite="",
                 added="", addedby="",
                 changed="", changedby=""):
        self.id = id
        self.cite = self.__needsdecode(cite)
        self.added = self.__needsdecode(added)
        self.addedby = self.__needsdecode(addedby)
        self.changed = self.__needsdecode(changed)
        self.changedby = self.__needsdecode(changedby)

    @staticmethod
    def json_to_cite(jsoncite):
        return Cite(**jsoncite)

    @staticmethod
    def __needsdecode(tstr):
        if type(tstr) is bytes:
            return tstr.decode("utf-8")
        else:
            return tstr

    def __str__(self):
        if self.id == 0:
            return "No such cite. Please check your index or report to admin."
        else:
            return "\n{cite}\n(added by {addedby})"\
                .format(cite=self.cite,
                        addedby=self.addedby)

    def __repr__(self):
        return """Cite(id: {id},
cite: {cite},
added: {added},
addedby: {addedby},
changed: {changed},
changedby: {changedby})""".format(id=self.id,
                                  cite=self.cite,
                                  added=self.added,
                                  addedby=self.addedby,
                                  changed=self.changed,
                                  changedby=self.changedby)

    def __getitem__(self, key):
        if key == "id":
            return self.id
        elif key == "cite":
            return self.cite
        elif key == "added":
            return self.added
        elif key == "addedby":
            return self.addedby
        elif key == "changed":
            return self.changed
        elif key == "changedby":
            return self.changedby
        else:
            raise KeyError


class CiteSqlite():
    """SQLite3-Wrapper for F3LBot and F3LCites-System
    Usually returns (arrays of) dicts of the form
      {"id": 1, "cite": "Foo", "addedby": "Guy",
       "added": "1970-01-01", "changedby": "Guy2",
       "changed": "1970-01-02"}"""
    import sqlite3
    from random import randint
    __q_prepareDB = """CREATE TABLE IF NOT EXISTS cites(
    id INTEGER PRIMARY KEY ASC AUTOINCREMENT, cite TEXT NOT NULL,
    added TEXT DEFAULT (date('now')), addedby TEXT);
    CREATE TABLE IF NOT EXISTS changes(
    id INTEGER PRIMARY KEY ASC AUTOINCREMENT, citeid INTEGER UNSIGNED,
    changed TEXT DEFAULT (date('now')), changedby TEXT);
    CREATE VIEW IF NOT EXISTS mergecites AS SELECT
    cites.id, cites.cite, cites.added, cites.addedby,
    changes.changed, changes.changedby FROM cites
    LEFT JOIN changes ON cites.id = changes.citeid;
    CREATE VIEW IF NOT EXISTS showcites AS SELECT
    id, cite, added, addedby, MAX(changed), changedby FROM mergecites
    GROUP BY id;"""
    __q_randomCite = "SELECT * FROM showcites ORDER BY added DESC LIMIT ?, 1"
    __q_getCite = "SELECT * FROM showcites WHERE id==?"
    __q_addCite = "INSERT INTO cites (cite, addedby) VALUES (?,?)"
    __q_countRecords = "SELECT COUNT(*) FROM cites"

    def __init__(self, dbname=":memory:"):
        self.conn = self.sqlite3.connect(dbname, check_same_thread=False)
        self.conn.text_factory = str
        self.db = self.conn.cursor()
        self.db.executescript(self.__q_prepareDB)
        self.conn.commit()

    def get_random_cite(self):
        self.db.execute(self.__q_countRecords)
        records = self.db.fetchone()
        if records and len(records) == 1:
            randrecord = self.randint(0, records[0] - 1)
            self.db.execute(self.__q_randomCite, str(randrecord))
            answer = self.db.fetchone()
            if answer:
                # Extract Infos from reply
                return Cite(
                    id=answer[0],
                    cite=answer[1],
                    added=answer[2],
                    addedby=answer[3],
                    changed=answer[4],
                    changedby=answer[5]
                )
        else:
            return Cite()

    def get(self, index):
        self.db.execute(self.__q_getCite, str(index))
        answer = self.db.fetchone()
        print(answer)
        if answer and len(answer) == 6:
            # Extract Infos from reply
            return Cite(
                id=answer[0],
                cite=answer[1],
                added=answer[2],
                addedby=answer[3],
                changed=answer[4],
                changedby=answer[5]
            )
        else:
            return Cite

    def add_cite(self, cite, name):
        self.db.execute(self.__q_addCite, (cite, name))
        self.conn.commit()
        return "Added Cite"


class JsonCiteAPI(BotPlugin):
    """Connector to the F3LCites Json API."""
    import requests
    f3lcites_host = "localhost"
    f3lcites_port = "8888"
    f3lcites_base_url = "api/"

    def __init__(self):
        self.full_base_url = \
            "http://" + self.f3lcites_host \
            + ":" + self.f3lcites_port \
            + "/" + self.f3lcites_base_url
        self.getUrl = self.full_base_url + "get"
        self.addUrl = self.full_base_url + "add"

    def get_random_cite(self):
        reply = requests.get(self.getUrl)
        if reply.status_code == 200:
            return Cite.json_to_cite(reply.json())
        else:
            return Cite()

    def get(self, index):
        reply = requests.get(self.getUrl + "/" + str(index))
        print(reply.status_code)
        if reply.status_code == 200:
            return Cite.json_to_cite(reply.json())
        else:
            return Cite()

    def add_cite(self, cite, name):
        payload = {"author": name, "cite": cite}
        reply = requests.post(self.addUrl, json=payload)
        if reply.status_code == 200:
            internal_json = reply.json()
            return internal_json["message"]
        else:
            return "Adding failed."


class CiteAPI(BotPlugin):
    """API to the F3LCite system"""
    # Uncomment this to use sqlite
    # dbname = "/home/oliver/.f3lcites.db"
    # db = JsonCiteSqlite(dbname)
    db = JsonCiteAPI()

    def __get_element(self, index):
        """Get a single element."""
        cite = self.db.get(index)
        if cite and cite["id"] != 0:
            return str(cite)
        else:
            return "Invalid index: {}".format(cite["id"] if cite else None)

    def __random_cite(self):
        """Return a random quote"""
        cite = self.db.get_random_cite()
        if cite and cite["id"] != 0:
            return cite
        else:
            return "Invalid index"

    # noinspection PyUnusedLocal
    @botcmd(split_args_with=None)
    def cite_random(self, msg, args):
        """Get random cite from DB"""
        return self.__random_cite()

    # noinspection PyUnusedLocal
    @botcmd(split_args_with=None)
    def cite_get(self, msg, args):
        """Get msg with given index from DB"""
        if len(args) != 1:
            return "Invalid usage. This command takes exactly one parameter"
        # If the argument is no int, the following fails
        try:
            index = int(args[0])
            return self.__get_element(index)
        except ValueError:  # pragma: no cover
            return "This command takes one integer only. Have you specified \
an existing index?"

    @botcmd()
    def cite_add(self, msg, args):
        """Insert quote into DB"""
        if not args:
            return "Invalid usage. You must add a quote"
        else:
            quote = args.replace("\r\n", " – ")\
                        .replace("\r", " – ")\
                        .replace("\n", " – ")\
                        .encode("utf-8")
            added = self.db.add_cite(quote, peer_account_name(msg))
            return added
            # if added == 1:
            #     return "Sucessfully added the quote"
            # else: # pragma: no cover
            #     return "Seems like something went wrong"
