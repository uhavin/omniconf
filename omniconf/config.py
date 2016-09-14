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

from omniconf.exceptions import UnknownSettingError, UnconfiguredSettingError
from omniconf.setting import DEFAULT_REGISTRY as SETTINGS_REGISTRY


class ConfigRegistry(object):
    """
    A registry of Configured values for a SettingRegistry.
    """
    def __init__(self, settings_registry=None):
        global SETTINGS_REGISTRY
        if not settings_registry:
            self.settings = SETTINGS_REGISTRY
        else:
            self.settings = settings_registry
        self.registry = {}

    def set(self, key, value):
        """
        Configures the value for the given key. The value will be converted to the type defined in
        the Setting, by calling the type as a function with the value as the only argument.
        Trying to configure a value under an unknown key will result in an UnknownSettingError.
        """
        if not self.settings.has(key):
            raise UnknownSettingError("Trying to configure unregistered key {0}".format(key))
        setting = self.settings.get(key)
        self.registry[key] = setting.type(value)

    def has(self, key):
        """
        Checks if a value has been configured for the given key, or if a default value is present.
        """
        if key in self.registry:
            return True
        elif self.settings.has(key) and self.settings.get(key).default is not None:
            return True
        return False

    def get(self, key):
        """
        Returns the configured value for the given key, or the default value if the key was not
        configured.
        """
        if key in self.registry:
            return self.registry[key]
        elif self.settings.has(key) and self.settings.get(key).default is not None:
            return self.settings.get(key).default
        raise UnconfiguredSettingError("No value or default available for {0}".format(key))

    def unset(self, key):
        """
        Removes the value for a given key from the registry.
        """
        if key in self.registry:
            del self.registry[key]

DEFAULT_REGISTRY = ConfigRegistry()


def config(key, registry=None):
    """
    Retrieves the configured value for a given key. If no specific registry is specified, the
    value will be retrieved from the default ConfigRegistry.
    """

    global DEFAULT_REGISTRY
    if not registry:
        registry = DEFAULT_REGISTRY

    return registry.get(key)