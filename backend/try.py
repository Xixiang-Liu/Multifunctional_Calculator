import os.path as osp
import os

up_dir_path = ".."
print(os.listdir(up_dir_path))

resources_dir_path = osp.join(up_dir_path, "resources/temp")
print(os.listdir(resources_dir_path))
