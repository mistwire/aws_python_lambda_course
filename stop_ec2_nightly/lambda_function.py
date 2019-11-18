import boto3

# Define standard entry point:
def lambda_handler(event, context):

    # Get list of all regions in AWS:
    ec2_client = boto3.client('ec2')
    # Use list comprehension to describe regions:
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]

    # Iterate over each region
    for region in regions:
        ec2 = boto3.resource('ec2', region_name=region)

        print("Region:", region)

        # Skip stopped instances:
        instances = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name',
                      'Values': ['running']}])

        # Stop the instances
        for instance in instances:
            instance.stop()
            print('Stopped instance: ', instance.id)
