from modules._module import Module
from utils.custom_print import print_info, print_error, print_ok
from utildata.dataset_options import Option
from utils.shodan_search import shodan_search
from utils.shell_options import ShellOptions
from os import getenv


class ShodanModule(Module):

    def __init__(self, information, opts=None, default_file_name="./files/shodan.txt"):
        # -----------name-----default_value--description--required?
        options = {
            "apishodan": Option.create(name="apishodan", required=True),
            "file": Option.create(name="file", value=default_file_name, required=True)
            }
        if opts:
            options.update(opts)
        # Constructor of the parent class
        super(ShodanModule, self).__init__(information, options)
        # Set Shodan key if exists in $HOME/.shodan/api_key and it doesn't have a global value.
        if not self.args["apishodan"]:
            try:
                home = getenv("HOME")
                shodan_key_path = home + "/.shodan/api_key"
                with open(shodan_key_path, "r") as f:
                    key = f.read().strip()
                    self.set_value(["apishodan", key])
            except:
                pass

    # This function must be always implemented, it is called by the run option
    def run(self): 
        pass

    def start(self, to_search):
        try:
            file_to_save = open(self.args["file"], "w+")
        except Exception as e:
            print_error(e)
            print_error("Module has not been launched")
            return

        data_collected = shodan_search(file_to_save, self.args["apishodan"], to_search)
        if data_collected:
            print_ok(f"Saving information in {self.args['file']}")

        file_to_save.close()
        