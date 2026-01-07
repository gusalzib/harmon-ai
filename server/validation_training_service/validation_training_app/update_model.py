import gitlab
import yaml
import os

GITLAB_URL = "https://git.chalmers.se"
GITLAB_TOKEN = os.getenv("GITLAB_ACCESS_TOKEN")
PROJECT_ID = "courses/dit826/2025/team3"
BRANCH = "main"
FILE_PATH = "cloud-deploy/prediction.yaml"

def update_model(modelName):
    gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_TOKEN)
    project = gl.projects.get(PROJECT_ID)

    yaml_file = project.files.get(FILE_PATH, ref=BRANCH)
    yaml_content = yaml_file.decode()
    # Use safe_load_all to handle multiple documents (Deployment + Service)
    yaml_docs = list(yaml.safe_load_all(yaml_content))

    for doc in yaml_docs:
        if doc.get('kind') == 'Deployment':
            containers = doc['spec']['template']['spec']['containers']
            
            # We assume the first container is the one we want to update
            env_vars = containers[0]['env']
            
            # Loop through existing variables to find MODEL_NAME
            for env in env_vars:
                if env['name'] == 'MODEL_NAME':
                    print(f"Updating MODEL_NAME from '{env['value']}' to '{modelName}'")
                    env['value'] = modelName
                    break
            break

    # Convert the list of documents back to a multi-document YAML string
    new_yaml_str = yaml.dump_all(yaml_docs, default_flow_style=False, sort_keys=False)

    commit_data = {
            'branch': BRANCH,
            'commit_message': f"Update MODEL_NAME to {modelName} [update_model]",
            'actions': [
                {
                    'action': 'update',
                    'file_path': FILE_PATH,
                    'content': new_yaml_str
                }
            ]
        }
    # 5. Push to GitLab
    project.commits.create(commit_data)
