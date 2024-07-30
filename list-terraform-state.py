import os
import boto3
import subprocess
bucket_name = 'terraform-state-danny'
local_dir = './terraform_states'
os.makedirs(local_dir, exist_ok=True) # Create the local directory if it doesn't exist
s3 = boto3.client('s3') # Initialize S3 client
objects = s3.list_objects_v2(Bucket=bucket_name)  # Get the list of objects in the specified S3 bucket
state_files = [obj['Key'] for obj in objects.get('Contents', [])]  # Extract the keys of the objects (file names) into a list
all_resources = []  # Create an empty list to store the names of all resources  
# Download and list resources
for key in state_files:
    local_file = os.path.join(local_dir, os.path.basename(key))
    # Download state file
    s3.download_file(bucket_name, key, local_file)
    print(f"Resources in {key}:")
    result = subprocess.run(['terraform', 'state', 'list', '-state', local_file], stdout=subprocess.PIPE)
    resources = result.stdout.decode('utf-8').splitlines()
    all_resources.extend(resources)
    for resource in resources:
        print(resource)
    print("")
for i, resource in enumerate(all_resources, 1):
    print(f"{i}. {resource}")
print(f"\nTotal Number of Resources: {len(all_resources)}")
