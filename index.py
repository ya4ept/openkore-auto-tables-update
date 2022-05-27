import os
import re
import glob
import argparse

from libs.helper import Helper
from libs.patches import Patches

class Index(Helper):
    def __init__(self, file):
        self.file = self.read_json(file)
        
        self.patch = Patches(server_name=self.file['server_name'], patch_info=self.file['patch_list'], patch_file=self.file['patch_download'])


    def run(self):
        old_patches_info = []
        # check old patches
        if os.path.exists(f"./patches/{self.file['server_name']}/{self.file['server_name']}.json"):
            old_patches_info = self.read_json(f"./patches/{self.file['server_name']}/{self.file['server_name']}.json")
        # check new patches
        new_patches_info = self.patch.get_patchinfo()
        print(f'[DEBUG][{self.file["server_name"]}][STEP 1] Patch list found [{len(old_patches_info)}/{len(new_patches_info)}]')
        
        # compare 2 list
        patches_files = [i for i in new_patches_info if i not in old_patches_info]
        if len(old_patches_info) == 0:
            patches_files = patches_files[-10:]
        
        # download different files
        for i in patches_files:
            if os.path.exists(f'./patches/{self.file["server_name"]}/downloaded/{i}'):
                continue

            if self.patch.get_patchfile(i):
                print(f'[DEBUG][{self.file["server_name"]}][STEP 2] Download {i} Success!')

        # check new file and replace
        lastest_files = {}
        for i in glob.glob(f"./patches/{self.file['server_name']}/downloaded/*"):
            if '.rgz' in i:
                data = self.patch.unpack_rgz(i)
                if len(data) > 0:
                    for file_rgz in data:
                        lastest_files[file_rgz] = i
            if '.gpf' in i:
                data = self.patch.unpack_gpf(i)
                if len(data) > 0:
                    for file_gpf in data:
                        lastest_files[file_gpf] = i

        # extract all new file
        for i in sorted(lastest_files):
            if not any(j in i for j in ['.txt', '.lua', '.lub', '.gat', '.gnd', '.rsw']):
                continue

            key = i
            value = lastest_files[key]
        
            base = re.findall(r'([^\/\\]+)$', key)[0]


            if '.rgz' in value:
                self.patch.unpack_rgz_file(value, key, base)

            if '.gpf' in value:
                self.patch.unpack_gpf_file(value, key, base)

            print(f'[DEBUG][{self.file["server_name"]}][STEP 3] Unpacked {base} -> {value} File Success!')

        

        for i in sorted(lastest_files):

            key = i
            value = lastest_files[key]

            if "iteminfo" in key.lower():
                if self.convert_iteminfo_lub_txt(key):
                    print(f'[DEBUG][{self.file["server_name"]}][STEP 4] Iteminfo to txt Success!')
                    break

        self.dump_json(f"./patches/{self.file['server_name']}/{self.file['server_name']}.json", new_patches_info)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='openkore auto tables update')
    parser.add_argument("--file", action="store", dest="file", required=True)
    results = parser.parse_args()
    Index(results.file).run()



