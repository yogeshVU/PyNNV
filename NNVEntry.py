import argparse
from NNV import NNVExec

# Create the parser
my_parser = argparse.ArgumentParser(description='NNV Program Executable')
# Add the arguments
my_parser.add_argument('--json', required=True)
my_parser.add_argument('--inputdir',required=True)
my_parser.add_argument('--config')

# Execute the parse_args() method
args = my_parser.parse_args()
template_param_json = args.json
input_dir = args.inputdir

config_file = None
config_file = args.config

print(template_param_json)
print(config_file)
print(input_dir)
if config_file is not None:
    NNVExec(template_param_json,input_dir,config_file=config_file)
else:
    NNVExec(template_param_json, input_dir)
