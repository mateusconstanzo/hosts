# hosts

Editing /etc/hosts can be tedious, so this tool makes it easier.

However, the great advantage of using **hosts** is that it allows the use of presets, so you have different mappings in different presets. Additionally, **hosts** does not touch any other lines in /etc/hosts, it only adds an additional layer.

**hosts** presets are files identical to /etc/hosts, with the difference that they're stored somewhere else. The names of active presets are stored in the **"/opt/hosts/presets/infra"** . Whenever you do something in **hosts**, the active presets are copied one by one to the end of your /etc/hosts file. They are placed between comments for later easy identification. This means that whatever lines you have in your /etc/hosts are left unchanged. It's really that simple.

## Commands

- **hosts show**
- **hosts enable [preset]**
- **hosts enable-all**
- **hosts disable [preset]**
- **hosts disable-all**
- **hosts actives**

#### Install

    git clone https://github.com/mateusconstanzo/hosts.git
    cd hosts
    chmod +x install.sh uninstall.sh
    sudo ./install.sh

#### Uninstall

    ./uninstall.sh
