# Copyright (c) 2016 Cyso < development [at] cyso . com >
#
# This file is part of omniconf, a.k.a. python-omniconf .
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library. If not, see
# <http://www.gnu.org/licenses/>.

from omniconf.backends.configobj import ConfigObjBackend
from omniconf.config import ConfigRegistry
from omniconf.setting import SettingRegistry
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import nose.tools

CONFIGOBJ_FILE = """
foo=bar

[section]
bar=baz

[[subsection]]
baz=foo
"""

CONFIGS = [
    ("foo", "bar", None),
    ("section.bar", "baz", None),
    ("section.subsection.baz", "foo", None),
    ("", None, KeyError),
    ("section", {"bar": "baz", "subsection": {"baz": "foo"}}, None),
    ("unknown", None, KeyError)
]


def test_configobj_backend_autoconfigure():
    prefix = "testconf"
    settings = SettingRegistry()
    settings.add(ConfigObjBackend.autodetect_settings(prefix)[0])
    conf = ConfigRegistry(setting_registry=settings)

    backend = ConfigObjBackend.autoconfigure(conf, prefix)
    nose.tools.assert_is(backend, None)

    conf.set("{0}.configobj.filename".format(prefix), "bar")
    backend = ConfigObjBackend.autoconfigure(conf, prefix)
    nose.tools.assert_is_instance(backend, ConfigObjBackend)


def test_configobj_backend_get_value():
    for key, value, sideeffect in CONFIGS:
        yield _test_get_value, key, value, sideeffect


def _test_get_value(key, value, sideeffect):
    backend = ConfigObjBackend(StringIO(CONFIGOBJ_FILE))
    if sideeffect:
        with nose.tools.assert_raises(sideeffect):
            backend.get_value(key)
    else:
        nose.tools.assert_equal(backend.get_value(key), value)
