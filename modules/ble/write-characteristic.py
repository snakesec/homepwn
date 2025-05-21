from utils.ble import BLE
from time import sleep
from modules._module import Module
from utils.custom_print import print_info, print_error, print_ok
from utils.check_root import is_root
from utils.shell_options import ShellOptions
from utildata.dataset_options import Option


class HomeModule(Module):

    def __init__(self):
        information = {"Name": "BLE write a characteristic",
                       "Description": "This module allows you to write content encoded in the feature specified by the UUID. The feature must be writable to proceed.",
                       "privileges": "root",
                       "OS": "Linux",
                       "Author": "@josueencinar"}

        # -----------name-----default_value--description--required?
        options = {"bmac": Option.create(name="bmac", required=True),
                   "uuid": Option.create(name="uuid",  required=True, description='Specific UUID for a characteristic'),
                   "type": Option.create(name="type", value="random", required=True, description='Device addr type'),
                   "data": Option.create(name="data", value="Pwned", required=True, description="Data to write"),
                   "encode": Option.create(name="encode",  required=True, description='Choose data encode'),
                   "wait": Option.create(name="wait", value=0, required=True, description='seconds to wait connected after writing'),
                   "iface": Option.create(name="iface", value=0, description='Ble iface index (default to 0 for hci0)')
                   }

        # Constructor of the parent class
        super(HomeModule, self).__init__(information, options)

    # Autocomplete set option with values    
    def update_complete_set(self):
        s_options = ShellOptions.get_instance()
        s_options.add_set_option_values("encode", ["ascii", "hex"])
        s_options.add_set_option_values("type", ["random", "public"])

    # This function must be always implemented, it is called by the run option
    @is_root
    def run(self):
        bmac = self.args["bmac"]
        data = self._transform_data(self.args["encode"], self.args["data"])
        try:
            iface = int(self.args["iface"])
        except:
            iface = 0
        if not data:
            return

        attempt = 1
        success = False
        ble_device = BLE(bmac, self.args["type"], iface)
        while attempt <= 5 and not success:
            print_info(f"Trying to connect {bmac}. (Attempt: {attempt})")
            try:
                ble_device.connect()
                success = True
            except KeyboardInterrupt:
                print_info("Interrupted... exit run")
                return 
            except:
                attempt += 1
        if not success:
            print_error("Failed to connect")
            return
        ble_device.write_data(data, self.args["uuid"])
        try:
            sleep(int(self.args["wait"]))
        except:
            sleep(2)
            
        ble_device.disconnect()

    def _transform_data(self, encode, data):
        if encode == "hex":
            try:
                data = bytes.fromhex(data.replace("0x",""))
            except:
                print_error("Bad Hexadecimal value check it")
                data = None 
        else:
            data = data.encode()
        return data