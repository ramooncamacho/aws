import json
import os
import boto3

client = boto3.client('ecs')

def lambda_handler(event, context):

    cluster = os.environ['CLUSTER']
    service = os.environ['SERVICE']
    
    message = f'The recycle process from {service} service of {cluster} cluster was initiated successfully.'
    
    describe_service = client.describe_services(
        cluster=cluster,
        services=[
            service,
        ]
    )
    
    rolloutStates = []
    
    for deployment in describe_service['services'][0]['deployments']:
        rolloutStates.append(deployment['rolloutState'])
    
    if len(rolloutStates) == 1 and rolloutStates[0] == 'COMPLETED':
        update_service = client.update_service(
            cluster=cluster, 
            service=service, 
            forceNewDeployment=True
        )
        print(update_service)
    else:
        message = 'There is a rollout in progress. Wait a minute, then try again.'
    
    print(message)
    return message