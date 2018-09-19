import os

PRESET_STRING = "### hosts - Preset {:s} "
PRESET_STRING_END = "### END hosts - Preset {:s} "

#HOSTS_FILE="/etc/hosts"
HOSTS_FILE="/home/mateusconstanzo/hosts"
PRESETS_FOLDER="/home/mateusconstanzo/presets"

class Presets():

    def get(self):

        presets = []
        for preset in os.listdir(PRESETS_FOLDER):
            presets.append(preset)

        return presets

    def show(self):

        for preset in self.get():
            print preset

    def check(self, preset):

        if preset in self.get():
            print "Tem sim"
        else:
            print "Tem nao"

    def active(self, preset):

        with open(PRESETS_FOLDER + "/" + preset ) as f:
            lines = f.readlines()
            lines = [x.strip() + "\n" for x in lines]

        return lines

    def active_all(self):

        for preset in self.get():
            Host().add_preset(preset)

    def get_content_wihout_preset(self, preset):

        content = []
        
        with open(HOSTS_FILE) as f:

            is_preset_block =  False

            for row in f.readlines():

                if PRESET_STRING.format(preset) in row:
                    is_preset_block = True

                elif PRESET_STRING_END.format(preset) in row:
                    is_preset_block = False

                else:

                    if not is_preset_block:
                        content.append(row)

        return content

class Host:

    def remove_preset(self, preset):

        content = Presets().get_content_wihout_preset(preset)

        with open(HOSTS_FILE,"wb") as f:
            f.writelines(content)

    def add_preset(self, preset):
        
        preset_content = Presets().active(preset)

        content = Presets().get_content_wihout_preset(preset)
                
        with open(HOSTS_FILE,"wb") as f:
            f.writelines(content)
            f.write(PRESET_STRING.format(preset) + "\n")
            f.writelines(preset_content)
            f.write(PRESET_STRING_END.format(preset) + "\n")

Presets().show()
Presets().check("infra")
Presets().active_all()