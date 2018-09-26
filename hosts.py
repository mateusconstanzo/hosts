import argparse
import os
import abc

PRESET_STRING = "### hosts - Preset {:s} "
PRESET_STRING_END = "### END hosts - Preset {:s} "

HOSTS_FILE="/etc/hosts"
PRESETS_FOLDER="/opt/hosts/presets"

MESSAGES = {
    "ACTIVE" : "### Preset enables",
    "SHOW" : "### Presets",
    "ENABLE_ALL" : "### All presets enabled",
    "DISABLE_ALL" : "### All presets disabled",
    "ITEM_ENABLE" : "# {:s} # enable",
    "ITEM" : "# {:s}",
    "NOT_FOUND" : "### Preset not found",
    "DISABLED" : "### Disable",
    "ENABLED" : "### Enabled",
}

class Preset:

    def __init__(self, name):
        self.name = name
        self.content = self.get_content()

    def get_content(self):

        with open(PRESETS_FOLDER + "/" + self.name ) as f:
            lines = f.readlines()
            lines = [x.strip() + "\n" for x in lines]

        return lines

class Presets:

    def __init__(self):
        self.presets = self._get_all()
        self.host = Host()

    def show(self):

        print MESSAGES["SHOW"]

        actives = self._get_actives()

        for preset in self.presets:

            message = "ITEM"

            if preset in actives:
                message = "ITEM_ENABLE"

            print MESSAGES[message].format(preset.name)

    def actives(self):

        print MESSAGES["ACTIVE"]

        for preset in self._get_actives():
            print MESSAGES["ITEM"].format(preset.name)

    def disable(self, preset_name):
        try:

            preset = self._get(preset_name)

            self.host.remove(preset)

            print MESSAGES["DISABLED"]
            print MESSAGES["ITEM"].format(preset.name)

        except:
            print MESSAGES["NOT_FOUND"]


    def disable_all(self):

        for preset in self.presets:
            self.host.remove(preset)

        print MESSAGES["DISABLE_ALL"]


    def enable(self, preset_name):
        try:

            preset = self._get(preset_name)

            self.host.add(preset)

            print MESSAGES["ENABLED"]
            print MESSAGES["ITEM"].format(preset.name)

        except:
            print MESSAGES["NOT_FOUND"]

    def enable_all(self):

        for preset in self.presets:
            self.host.add(preset)

        print MESSAGES["ENABLE_ALL"]

    def _get(self, name):

        for preset in self.presets:
            if name == preset.name:
                return preset

        raise Exception('Preset not found')

    def _get_actives(self):

        content = self.host.get_content()

        presets = []
        for preset in self.presets:

            if  PRESET_STRING.format(preset.name) in content:
                presets.append(preset)

        return presets

    def _get_all(self):

        presets = []
        for preset in os.listdir(PRESETS_FOLDER):
            presets.append(Preset(preset))

        return presets

class Host:

    def remove(self, preset):

        content = self._get_content_wihout_preset(preset)

        with open(HOSTS_FILE,"wb") as f:
            f.writelines(content)

    def add(self, preset):

        content = self._get_content_wihout_preset(preset)
                
        with open(HOSTS_FILE,"wb") as f:
            f.writelines(content)
            f.write(PRESET_STRING.format(preset.name) + "\n")
            f.writelines(preset.get_content())
            f.write(PRESET_STRING_END.format(preset.name) + "\n")

    def get_content(self):

        with open(HOSTS_FILE) as f:
            return f.read()

    def _get_content_wihout_preset(self, preset):

        content = []
        
        with open(HOSTS_FILE) as f:

            is_preset_block =  False

            for row in f.readlines():

                if PRESET_STRING.format(preset.name) in row:
                    is_preset_block = True

                elif PRESET_STRING_END.format(preset.name) in row:
                    is_preset_block = False

                else:

                    if not is_preset_block:
                        content.append(row)

        return content

class Command:

    __metaclass__ = abc.ABCMeta

    def __init__(self, subparsers, command):
        self.parse = subparsers.add_parser(command)
        self.parse.set_defaults(func=self.call)

    @abc.abstractmethod
    def call():
        pass

class ShowCommand(Command):

    COMMAND = 'show'

    def __init__(self, subparsers):
        super(ShowCommand, self).__init__(subparsers, self.COMMAND)

    @staticmethod
    def call(args):
        Presets().show()

class ActivesCommand(Command):

    COMMAND = 'actives'

    def __init__(self, subparsers):
        super(ActivesCommand, self).__init__(subparsers, self.COMMAND)

    @staticmethod
    def call(args):
        Presets().actives()

class EnableAllCommand(Command):

    COMMAND = 'enable-all'

    def __init__(self, subparsers):
        super(EnableAllCommand, self).__init__(subparsers, self.COMMAND)

    @staticmethod
    def call(args):
        Presets().enable_all()

class EnableCommand(Command):

    COMMAND = 'enable'

    def __init__(self, subparsers):
        super(EnableCommand, self).__init__(subparsers, self.COMMAND)
        self.parse.add_argument('preset')

    @staticmethod
    def call(args):
        Presets().enable(args.preset)

class DisableCommand(Command):

    COMMAND = 'disable'

    def __init__(self, subparsers):
        super(DisableCommand, self).__init__(subparsers, self.COMMAND)
        self.parse.add_argument('preset')

    @staticmethod
    def call(args):
        Presets().disable(args.preset)

class DisableAllCommand(Command):

    COMMAND = 'disable-all'

    def __init__(self, subparsers):
        super(DisableAllCommand, self).__init__(subparsers, self.COMMAND)

    @staticmethod
    def call(args):
        Presets().disable_all()

def commands(subparsers):
    ShowCommand(subparsers)
    EnableCommand(subparsers)
    EnableAllCommand(subparsers)
    DisableCommand(subparsers)
    DisableAllCommand(subparsers)
    ActivesCommand(subparsers)

parser = argparse.ArgumentParser()
parser.add_argument('--version', action='version', version='1.0.0')
commands(parser.add_subparsers())

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)