import sys
import local_search
import prior_optimization
import json
import os
import bo
from utility_functions import *
import json
from jsonschema import Draft4Validator, validators, exceptions


def optimize(parameters_file, black_box_function=None):

    try:
        bopro_pwd = os.environ['PWD']
        bopro_home = os.environ['BOPRO_HOME']
        os.chdir(bopro_home)
    except:
        bopro_home = "."
        bopro_pwd = "."

    if not parameters_file.endswith('.json'):
        _, file_extension = os.path.splitext(parameters_file)
        print("Error: invalid file name. \nThe input file has to be a .json file not a %s" %file_extension)
        raise SystemExit
    with open(parameters_file, 'r') as f:
        config = json.load(f)

    json_schema_file = 'scripts/schema.json'
    with open(json_schema_file, 'r') as f:
        schema = json.load(f)

    DefaultValidatingDraft4Validator = extend_with_default(Draft4Validator)
    try:
        DefaultValidatingDraft4Validator(schema).validate(config)
    except exceptions.ValidationError as ve:
        print("Failed to validate json:")
        print(ve)
        raise SystemExit

    # This handles the logger. The standard setting is that bopro always logs both on screen and on the log file.
    # In cases like the client-server mode we only want to log on the file.
    run_directory = config["run_directory"]
    if run_directory == ".":
        run_directory = bopro_pwd
        config["run_directory"] = run_directory
    log_file = config["log_file"]
    if log_file == "bopro_logfile.log":
        log_file = deal_with_relative_and_absolute_path(run_directory, log_file)
    sys.stdout = Logger(log_file)

    optimization_method = config["optimization_method"]


    if optimization_method == "local_search":
        local_search.main(config, black_box_function=black_box_function)
    else:
        bo.main(config, black_box_function=black_box_function)

    try:
        os.chdir(bopro_pwd)
    except:
        pass

    print("### End of the bopro script.")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        parameters_file = sys.argv[1]
    else :
        print("Error: only one argument needed, the parameters json file.")

    if parameters_file == "--help" or len(sys.argv) != 2:
        print("################################################")
        print("### Example: ")
        print("### cd bopro")
        print("### python3 scripts/bopro.py benchmarks/branin.json")
        print("################################################")
        exit(1)

    optimize(parameters_file)