import os
from paths import get_sub_dir

# set environ for optest
os.environ['optest_config_data_path'] = get_sub_dir('Data')
