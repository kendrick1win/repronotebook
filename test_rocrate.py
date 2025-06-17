from repronotebook.manual_basic_ro_crate.manual_rocrate import generate_ro_crate
import os

# Get the parent directory where CS2900-Lab-1 is located
parent_dir = os.path.expanduser("~/workspace/MDDP")

# Test the function with CS2900-Lab-1
generate_ro_crate(os.path.join(parent_dir, "CS2900-Lab-1"), "Your Name") 