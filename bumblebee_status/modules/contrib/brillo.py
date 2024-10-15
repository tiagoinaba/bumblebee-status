# pylint: disable=C0111,R0903

"""Controls and displays the brightness of a display

The following executable is required:
    * brillo

Parameters:
    * brightness.step: The amount of increase/decrease on scroll in % (defaults to 2)
    * brightness.device_path: The device path (defaults to /sys/class/backlight/intel_backlight), can contain wildcards (in this case, the first matching path will be used); This is only used when brightness.use_acpi is set to true
    * brightness.use_acpi: If set to true, read brightness directly from the sys ACPI interface, using the device specified in brightness.device_path (defaults to false)

contributed by `tiagoinaba <https://github.com/tiagoinaba>`_ - many thanks!
"""

import subprocess
import core.module
import core.widget
import core.input
import util.format

class Module(core.module.Module):
    def __init__(self, config, theme):
        super().__init__(config, theme, core.widget.Widget(self.current_brightness))
        self.__executable = True

        events = [
            {
                "cmd": "brillo -A {}".format(self.parameter("increase", 5)),
                "button": core.input.WHEEL_UP,
            },
            {
                "cmd": "brillo -U {}".format(self.parameter("decrease", 5)),
                "button": core.input.WHEEL_DOWN,
            },
        ]

        for e in events:
            core.input.register(
                self,
                button=e["button"],
                cmd=e["cmd"],
            )

    def current_brightness(self, widgets):
        if self.__executable:
            out = subprocess.run(["brillo"], shell=True, stdout=subprocess.PIPE).stdout
            if not len(out):
                self.__executable = False
                return "brillo not found"
            return "{}%".format(util.format.asint(float(out.decode("utf-8").strip())))
