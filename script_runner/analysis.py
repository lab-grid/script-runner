import base64
from script_runner.config import settings
import csv
import glob
import json
import re
import tempfile
import traceback
import os
import shutil
import subprocess
from celery import Celery
from distutils.dir_util import copy_tree
import jsonpath_ng


# Celery ----------------------------------------------------------------------

celery = Celery(
    'swabseq-analysis-celery',
    backend=os.environ.get('CELERY_RESULT_BACKEND', None),
    broker=os.environ.get('CELERY_BROKER_URL', None),
)

# celery.conf.update(app.config)


# Analysis --------------------------------------------------------------------

def result_is_valid(result, skip_lists):
    for name, values in skip_lists.items():
        col_value = result.get(name, None)
        if col_value is None or col_value in values:
            return False
    return True

def b64encode_file(filepath):
    with open(filepath, "rb") as input_file:
        return base64.b64encode(input_file.read()).decode('utf-8')

def read_csv_as_dict_list(filepath, filter_fn=None):
    with open(filepath, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        if filter_fn is None:
            filter_fn = lambda x: True
        return [x for x in csv_reader if filter_fn(x)]

def read_json_file(filepath):
    with open(filepath, "r") as json_file:
        return json.load(json_file)

def rename_fields(original, fields):
    return {
        new_field: original[original_field]
        for new_field, original_field
        in fields.items()
        if original_field in original
    }

def replace_env_vars(input, env_vars):
    for name, value in env_vars.items():
        input = input.replace(f"${name}", value)
        # input = input.replace(f"${{{name}}}", value)
    return input

def build_command(rundir, request_path, request_query_params, request_body):
    env_vars = {'RUNDIR': rundir}
    for path_arg in settings.inputs.path_args:
        path_match = re.match(path_arg.path_regex, request_path)
        path_match_group = path_arg.path_regex_match_group if path_arg.path_regex_match_group else 0
        if path_match:
            env_vars[path_arg.env_var_name] = path_match.group(path_match_group)
    for query_arg in settings.inputs.query_args:
        query_arg_values = request_query_params.get(query_arg.query_var_name, "")
        if len(query_arg_values) == 1:
            env_vars[query_arg.env_var_name] = query_arg_values[0]
        elif len(query_arg_values) > 1:
            env_vars[query_arg.env_var_name] = query_arg_values
    for body_arg in settings.inputs.body_args:
        jsonpath_expression = jsonpath_ng.parse(body_arg.body_jsonpath)
        env_vars[body_arg.env_var_name] = jsonpath_expression.find(request_body)
    return [
        replace_env_vars(command_arg, env_vars)
        for command_arg
        in settings.command
    ]

def build_response(rundir, status='ready'):
    attachments = {}
    for attachment_glob in settings.outputs.attachments:
        for attachment in glob.glob(f"{rundir}/{attachment_glob}"):
            attachments[os.path.basename(attachment)] = b64encode_file(attachment)

    response = {
        'status': status,
        'attachments': attachments,
    }

    # TODO: Add input args to response as keys.

    if settings.outputs.results.format == 'csv':
        response['results'] = read_csv_as_dict_list(os.path.join(rundir, settings.outputs.results.input_path))
        if settings.outputs.results.remapped_columns is not None:
            remapped_columns = {}
            skip_lists = {}
            for remapped_column in settings.outputs.results.remapped_columns:
                remapped_columns[remapped_column.output_name] = remapped_column.input_name
                skip_lists[remapped_column.output_name] = set(remapped_column.skip_list) if remapped_column.skip_list is not None else set()
            results = []
            for row in response['results']:
                result = rename_fields(row, remapped_columns)
                if result_is_valid(result, skip_lists):
                    results.append(result)
            response['results'] = results
    elif settings.outputs.results.format == 'json':
        response['results'] = read_json_file(os.path.join(rundir, settings.outputs.results.input_path))

    return response

def do_script(rundir, request_path, request_query_params, request_body):
    os.makedirs(os.path.join(rundir, "out"))

    script_args = build_command(rundir, request_path, request_query_params, request_body)
    subprocess.check_call(script_args)
    return build_response(rundir, status='ready')

def log_disk_usage(path = None):
    if path is None:
        path = os.getcwd()
    stat = shutil.disk_usage(path)
    print(f"Disk usage statistics for '{path}':")
    print(stat)

def copy_command_rundir_base(rundir):
    if settings.command_rundir_base:
        print(f"Copying base files from {settings.command_rundir_base}")
        try:
            copy_tree(settings.command_rundir_base, rundir)
        except Exception as ex:
            print(f"Failed to copy command_base_dir ({settings.command_rundir_base}) to {rundir}")
            print(traceback.format_exc())

@celery.task()
def run_script(request_path, request_query_params, request_body):
    try:
        command_rundir = settings.command_rundir if settings.command_rundir is not None else os.getcwd()

        # Run R script and zip results to generate temp file
        if settings.debug:
            # If we're in debug mode, don't delete the work directory
            rundir = tempfile.TemporaryDirectory(prefix="results-", dir=command_rundir).name
            copy_command_rundir_base(rundir)
            log_disk_usage()
            try:
                return do_script(rundir, request_path, request_query_params, request_body)
            finally:
                log_disk_usage()
        else:
            with tempfile.TemporaryDirectory(prefix="results-", dir=command_rundir) as rundir:
                copy_command_rundir_base(rundir)
                log_disk_usage()
                try:
                    return do_script(rundir, request_path, request_query_params, request_body)
                finally:
                    log_disk_usage()
    except Exception as ex:
        ex_str = traceback.format_exc()
        print(ex_str)
        return {
            'status': 'failed',
            'error': ex_str,
        }
