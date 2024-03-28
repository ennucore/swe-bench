import json
import typer
from scripts import make_test_spec  # Adjust import based on your project structure

app = typer.Typer()

def load_swebench_instances(json_file_path: str):
    with open(json_file_path, 'r') as file:
        instances = json.load(file)
    return instances

@app.command()
def get_test_spec_for_instance(json_file_path: str, instance_index: int, script_type: str):
    """
    Generate a test spec for a specific SWEBench instance identified by index.
    """
    instances = load_swebench_instances(json_file_path)
    try:
        instance = instances[instance_index]
    except IndexError:
        typer.echo(f"No instance found at index {instance_index}.")
        raise typer.Exit(code=1)

    test_spec = make_test_spec(instance)
    if script_type == "setup":
        typer.echo(test_spec.setup_script)
    elif script_type == "eval":
        typer.echo(test_spec.eval_script)
    elif script_type == 'correct_patch':
        print(instance['patch'])
    elif script_type == 'repo':
        print(instance['repo'].split('/')[-1])
    elif script_type == 'issue':
        print(instance['problem_statement'])
    else:
        print(test_spec)

if __name__ == "__main__":
    app()
