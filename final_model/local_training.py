import os
import subprocess


def main():
    version = '2.1'
    model_name = f'magic-autocomplete-{version}'
    output_dir = os.path.join(os.getcwd(), 'model', model_name)

    # windows
    subprocess.run(['python', '-m', 'main_package.scripts.task', f'--model-name={model_name}', '--num-epochs=60',
                    f'--output-dir={output_dir}', '--gcloud-training', ''])


if __name__ == "__main__":
    main()
