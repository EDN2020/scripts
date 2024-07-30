import os  # Import the os module for operating system functionalities
import boto3  # Import boto3 to interact with AWS services
import subprocess  # Import subprocess to run external processes
bucket_name = 'bidstrading-terraform-state-dev'  # Define the S3 bucket name where Terraform state files are stored
local_dir = './terraform_states'  # Define the local directory to save downloaded state files
os.makedirs(local_dir, exist_ok=True)  # Create the local directory if it doesn't exist
# Initialize S3 client
s3 = boto3.client('s3')  # Create an S3 client using boto3
# List state files
objects = s3.list_objects_v2(Bucket=bucket_name)  # Get the list of objects in the specified S3 bucket
state_files = [obj['Key'] for obj in objects.get('Contents', [])]  # Extract the keys of the objects (file names) into a list
# Initialize a list to store resources
all_resources = []  # Create an empty list to store the names of all resources
# Download and list resources
for key in state_files:  # Iterate over each state file
    local_file = os.path.join(local_dir, os.path.basename(key))  # Define the local file path
    # Download state file
    s3.download_file(bucket_name, key, local_file)  # Download the state file from S3 to the local file
    # List resources
    print(f"Resources in {key}:")  # Print header indicating the start of resource listing for a file
    # Run 'terraform state list' command on the downloaded state file
    result = subprocess.run(['terraform', 'state', 'list', '-state', local_file], stdout=subprocess.PIPE) 
    resources = result.stdout.decode('utf-8').splitlines()  # Decode and split the output into a list of resources
    all_resources.extend(resources)  # Add the resources to the all_resources list
    for resource in resources:  # Iterate over each resource
        print(resource)  # Print the resource name
    print("")  # Print a blank line for separation
# Print each resource with an index
for i, resource in enumerate(all_resources, 1):  # Enumerate resources starting from 1
    print(f"{i}. {resource}")  # Print the index and the resource name
# Print the total number of resources
print(f"\nTotal Number of Resources: {len(all_resources)}")  # Print the total count of resources
