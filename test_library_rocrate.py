from repronotebook.ro_crate_library.library_rocrate import generate_ro_crate_with_library
import os

parent_dir = os.path.expanduser("~/workspace/MDDP")

generate_ro_crate_with_library(os.path.join(parent_dir, "CS2900-Lab-1"), "Hugh")