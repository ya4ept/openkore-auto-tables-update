
import requests


class Patches:
    def __init__(self, server_name, patch_info, patch_file):
        self.server_name = server_name
        self.patch_info = patch_info
        self.patch_file = patch_file

    def get_patchinfo(self):
        resp = requests.get(self.patch_info)
        if resp.status_code == 200:
            patches = []
            for i in resp.text.splitlines():
                if not '//' in i and len(i) > 0:
                    data = i.split()
                    patches.append(data[1])
            return patches


    def get_patchfile(self, name):
        resp = requests.get(f"{self.patch_file}/{name}")
        if resp.status_code == 200:
            with open(f"./patches/{self.server_name}/downloaded/{name}", 'wb') as File:
                File.write(resp.content)
            return True
        return False