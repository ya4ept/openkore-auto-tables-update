import re
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

    def unpack_rgz(self, filename):
        cmd = f"sudo perl ./tools/rgz.pl -l -v {filename}"
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        lines, error = process.communicate()
        process.wait()

        lines = lines.splitlines()
        lines.pop(0)

        output = {}
        for i in lines:
            if len(i) > 0:
                data = list(i.strip().decode('UTF-8', errors='ignore').split())
                output[data[2]] = data[1]
        return output


    def unpack_rgz_file(self, rgz, rgz_file, rgz_file_format_name):
        rgz_file = rgz_file.replace('\\\\', '\\')
        cmd = f"sudo perl ./tools/rgz.pl -x {rgz} {rgz_file} ./patches/{self.file['server_name']}/extracted/{rgz_file_format_name}"
        process = subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        lines, error = process.communicate()
        process.wait()
        return True


    def unpack_gpf(self, filename):
        cmd = f'sudo ./tools/grf_extract {filename}'
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        lines, error = process.communicate()
        process.wait()

        lines = lines.splitlines()
        lines.pop(0)
        lines.pop(0)

        output = {}

        for i in lines:
            if len(i) > 0:
                data = list(re.findall(r'(.*)\s\((\d+)\)', i.strip().decode('UTF-8', errors='ignore'))[0])
                output[data[0]] = data[1]
        return output

    def unpack_gpf_file(self, gpf, gpf_file, gpf_file_format_name):
        cmd = f'sudo ./tools/grf_extract {gpf} {gpf_file} ./patches/{self.file["server_name"]}/extracted/{gpf_file_format_name}'
        process = subprocess.Popen(cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        lines, error = process.communicate()
        process.wait()
        return True


    def convert_iteminfo_lub_txt(self) -> bool:
        cmd = f"sudo ./tools/lua32 ./tools/LUB_TO_TABLES/PARSE_ITEMINFO.lua ./patches/{self.file['server_name']}/extracted ./tables/{self.file['server_name']}"
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

        lines, error = process.communicate()
        process.wait()

        return True

