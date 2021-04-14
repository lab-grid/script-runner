# script-runner

Enables the deployment of a script as an API protected by pluggable authentication
(only `auth0` or `none` currently supported). Script runner relies on a configuration
file (`config.json`) to specify the command that should be executed when a task is
started. Script runner exposes an API with two main endpoints:

- `POST /task` - Start new task
- `GET  /task/{id}` - Check task status/get results

Arguments to the script command can be passed via the request path, query, or JSON
body.

Script runner relies on two running containers:

- Server - Responsible for responding to API requests and validating auth headers.
- Worker - Responsible for running the script whenever a new task is started.

Script runner is built for running scripts that take a long period of time and uses
worker nodes from above to launch jobs. Communication between the server and worker
nodes happens through a Redis instance allowing multiple script invocations to be
running simultaneously


## Configuration

Script runner can be configured through a special file called `config.json`:

```
{
    "command": [ ... ],
    "inputs": {
        "path_args": [ ... ],
        "query_args": [ ... ],
        "body_args": [ ... ]
    },
    "outputs": {
        "results": {
            "kind": "file",
            "format": "csv",
            "input_path": ...,
            "remapped_columns": [ ... ]
        },
        "attachments": [ ... ]
    }
}
```

### Command

The command used to launch run the desired script is specified through the `"command": [ ... ]`
field. Specify each argument as a separate string. Parameters from the request path, query, or
body can be used in the command by prefixing the parameter name with a `$` sign:

```
    "command": [ "/scripts/my_script.sh", "regular-arg-1", "$THIS_ARGUMENT_COMES_FROM_REQUEST" ]
```

### Inputs

Parameters used in the script command are specified in the `"inputs": { ... }` field. The name of the
variable for use in the command definition above is set by the `"env_var_name": "..."` field. First,
select whether or not you would like to have the parameter specified in the request path, query, or body.

![image](https://user-images.githubusercontent.com/1199079/114761896-f417b300-9d15-11eb-9aa0-c498ae727eaa.png)

Path parameters are defined using regular expressions (https://www.w3schools.com/python/python_regex.asp)

```
...

"path_args": [
    {
        "env_var_name": "BASESPACE_ID",
        "path_regex": "([^/]+)",
        "path_regex_match_group": 1
    }
],

...
```

Query parameters are defined by specifying the query parameter name:

```
...

"query_args": [
    {
        "env_var_name": "SEASON",
        "query_var_name": "season"
    }
],

...
```

Body parameters are defined by specifying a JSONPath query (https://jsonpath.com/):

```
...

"body_args": [
    {
        "env_var_name": "CITY",
        "body_jsonpath": "$.address.city"
    }
],

...
```

### Outputs

The JSON data returned by the script-runner API can be configured in the `"outputs"` section.

Script-runner reads a main file that can be either in a JSON or CSV file format to parse and
send back as JSON under the `"results"` field. Script-runner also supports an `"attachments"`
field that base64-encodes requested files into the JSON object response.

For example, the following config:

```
"outputs": {
    "results": {
        "kind": "file",
        "format": "csv",
        "input_path": "LIMS_results.csv",
        "remapped_columns": [
            {
                "output_name": "plateIndex",
                "input_name": "Plate_384_Number",
                "skip_list": ["NA"]
            }
        ]
    },
    "attachments": [
        "*.pdf",
        "LIMS_results.csv"
    ]
}
```

Could produce the following output:

```
{
    "id": "168af779-a72e-4dec-a2e3-36240cad5973",
    "status": "ready",
    "attachments": {
        "results-n1a54tmd.pdf": "JVBERi0xLjUKJdDUxdgKNiAwI...",
        ...
    },
    "results": [
        {
            "plateIndex": "1",
            "plateCell": "A01",
            "marker1": "CATCTGTATC",
            "marker2": "ATGAGACTTG",
            "classification": "failed: low S2 & RPP30"
        },
        ...
    ]
}
```


## Usage

To get a script-runner API setup and running:

1. Build a docker container with your script and script-runner installed.

   ```
   FROM python
   
   pip install script-runner-api
   
   # Install your script here
   COPY ./my_script.sh /app/my_script.sh
   
   # ...
   ```
   
2. Setup your `config.json` file. See `Configuration` section for more information.
3. Deploy a worker and a server to your desired environment. We have provided some started
   [terraform](https://terraform.io/) modules
   ([AWS](https://github.com/lab-grid/terraform-aws-ecs-script-runner),
   [Azure](https://github.com/lab-grid/terraform-azurerm-container-instances-script-runner))
   + [examples](https://github.com/lab-grid/script-runner/tree/main/terraform) to help get started.
