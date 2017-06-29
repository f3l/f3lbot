The suite of plugins used for F3Ls XMPP Bot have been moved to [F3L Git](https://git.f3l.de/f3lbot). There won't be any further development in this repo :exclamation:

# F3LBot #

A collection of ErrBot-Extensions made for F3L.

## Installation ##

The proposed way of running F3LBot is using a python virtualenv.
You need `errbot` as well as `sleekxmpp` installed and running,
and might need to set an extra plugin directory until this is set up
to be a real errbot plugin.

The following systemd `.service` works for me:

```systemd
[Unit]
Description=Runs f3lbot continuously
After=network.target

[Service]
Type=forking
User=<errbot user>
Group=<errbot group>
Environment=VIRTUAL_ENV="<path to virtualenv>"
Environment=PATH="$VIRTUAL_ENV/bin:$PATH"
ExecStart="${VIRTUAL_ENV}/bin/errbot -c <path to config> --daemon
RestartSec=5
Restart=always

[Install]
WantedBy=multi-user.target
```

If you haven't got an installation of [f3lcites][f3lcites] you might
want to disable the cites-plugin, or change `CiteAPI` to use
`CiteSqlite` instead of `JsonCiteAPI`

## Implemented ##

* Give: beer, beer for user, give, give to user, listen for "beer"
* Pkg:
  * aur: package search, package info, maintainer info
  * arch: package search, package info, maintainer info
  * pkg: package search

## Planned ##

* F3L-Service Overview, status
* F3L-Gitlab webhook
* Pkg: rewrite

[f3lcites]: https://github.com/f3l/f3lcites
