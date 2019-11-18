# AWS Lambda function for creating a snapshot of every volume of an EC2 instance that has the key/value tag of backup/True


from datetime import datetime

import boto3


def lambda_handler(event, context):

    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
               for region in ec2_client.describe_regions()['Regions']]

    for region in regions:

        print(f'Instances in EC2 Region {region}:')
        # Setup ec2 resource object for each region in the iteration:
        ec2 = boto3.resource('ec2', region_name=region)

        instances = ec2.instances.filter(
            Filters=[
                {'Name': 'tag:backup', 'Values': ['True']}
            ]
        )

        # ISO 8601 timestamp, i.e. 2019-01-31T14:01:58
        timestamp = datetime.utcnow().replace(microsecond=0).isoformat()

        for i in instances.all():
            for v in i.volumes.all():

                desc = f'Backup of {i.id}, volume {v.id}, created {timestamp}'
                print(desc)

                snapshot = v.create_snapshot(Description=desc)

                print(f"Created snapshot: {snapshot.id} by CFW woot woot yeah!")

lambda_handler()

