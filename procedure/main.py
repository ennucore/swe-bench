import json
import typer
from scripts import make_test_spec  # Adjust import based on your project structure

app = typer.Typer()

def load_swebench_instances(json_file_path: str):
    with open(json_file_path, 'r') as file:
        instances = json.load(file)
    return instances

@app.command()
def get_test_spec_for_instance(json_file_path: str, instance_index: int):
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
    typer.echo("Setup Script:")
    typer.echo(test_spec.setup_script)
    typer.echo("Prompt:")
    typer.echo(test_spec.prompt)
    typer.echo("Eval Script:")
    typer.echo(test_spec.eval_script)

if __name__ == "__main__":
    app()
