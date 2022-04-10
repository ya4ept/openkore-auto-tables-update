import json
import subprocess

class Helper:

    def read_json(self, file):
        with open(file, "r") as File:
            data = json.load(File)
            return data

    def dump_json(self, file, data):
        with open(file, "w") as File:
            json.dump(data, File)
        return True

    def convert_iteminfo_lub_txt(self) -> bool:
        cmd = f"sudo ./tools/lua32 ./tools/LUB_TO_TABLES/PARSE_ITEMINFO.lua ./patches/{self.file['server_name']}/extracted ./tables/{self.file['server_name']}"
        print(cmd)
		process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

        lines, error = process.communicate()
        process.wait()

        return True

