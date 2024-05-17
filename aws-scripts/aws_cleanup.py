import boto3
import json
import time

# Configuration
REGION = "us-east-2"
S3_BUCKET_NAME = "cloud-clicker-bucket-test"
EB_APP_NAME = "cloud-clicker-test"
EB_ENV_NAME = "cloud-clicker-env-test"
LOG_GROUP_NAME = "cloud-clicker-logs-test"
INSTANCE_PROFILE_NAME = "aws-elasticbeanstalk-ec2-role"
SERVICE_ROLE_NAME = "aws-elasticbeanstalk-service-role"

# Create AWS clients
s3_client = boto3.client('s3', region_name=REGION)
iam_client = boto3.client('iam')
eb_client = boto3.client('elasticbeanstalk', region_name=REGION)
logs_client = boto3.client('logs', region_name=REGION)


def delete_s3_bucket():
    try:
        # Delete all objects from the S3 bucket
        bucket = boto3.resource('s3').Bucket(S3_BUCKET_NAME)
        bucket.objects.all().delete()
        
        # Delete the S3 bucket
        s3_client.delete_bucket(Bucket=S3_BUCKET_NAME)
        print(f'S3 bucket {S3_BUCKET_NAME} deleted.')
    except Exception as e:
        print(f'Error deleting S3 bucket: {e}')


def delete_iam_roles():
    try:
        # Detach policies from instance profile role
        attached_policies = iam_client.list_attached_role_policies(RoleName=INSTANCE_PROFILE_NAME)['AttachedPolicies']
        for policy in attached_policies:
            iam_client.detach_role_policy(RoleName=INSTANCE_PROFILE_NAME, PolicyArn=policy['PolicyArn'])

        # Delete instance profile role
        iam_client.delete_role(RoleName=INSTANCE_PROFILE_NAME)
        print(f'Instance profile role {INSTANCE_PROFILE_NAME} deleted.')
    except Exception as e:
        print(f'Error deleting instance profile role: {e}')
    
    try:
        # Detach policies from service role
        attached_policies = iam_client.list_attached_role_policies(RoleName=SERVICE_ROLE_NAME)['AttachedPolicies']
        for policy in attached_policies:
            iam_client.detach_role_policy(RoleName=SERVICE_ROLE_NAME, PolicyArn=policy['PolicyArn'])

        # Delete service role
        iam_client.delete_role(RoleName=SERVICE_ROLE_NAME)
        print(f'Service role {SERVICE_ROLE_NAME} deleted.')
    except Exception as e:
        print(f'Error deleting service role: {e}')
    
    try:
        # Remove role from instance profile
        iam_client.remove_role_from_instance_profile(InstanceProfileName=INSTANCE_PROFILE_NAME, RoleName=INSTANCE_PROFILE_NAME)
        # Delete instance profile
        iam_client.delete_instance_profile(InstanceProfileName=INSTANCE_PROFILE_NAME)
        print(f'Instance profile {INSTANCE_PROFILE_NAME} deleted.')
    except Exception as e:
        print(f'Error deleting instance profile: {e}')


def delete_eb_environment():
    try:
        # Terminate Elastic Beanstalk environment
        eb_client.terminate_environment(EnvironmentName=EB_ENV_NAME)
        print(f'Terminating Elastic Beanstalk environment {EB_ENV_NAME}. Waiting for it to be deleted...')
        
        # Wait for the environment to terminate
        waiter = eb_client.get_waiter('environment_terminated')
        waiter.wait(EnvironmentNames=[EB_ENV_NAME])
        print(f'Elastic Beanstalk environment {EB_ENV_NAME} terminated.')
    except Exception as e:
        print(f'Error terminating Elastic Beanstalk environment: {e}')


def delete_eb_application():
    try:
        # Delete Elastic Beanstalk application
        eb_client.delete_application(ApplicationName=EB_APP_NAME)
        print(f'Elastic Beanstalk application {EB_APP_NAME} deleted.')
    except Exception as e:
        print(f'Error deleting Elastic Beanstalk application: {e}')


def delete_log_group():
    try:
        # Delete CloudWatch log group
        logs_client.delete_log_group(logGroupName=LOG_GROUP_NAME)
        print(f'CloudWatch log group {LOG_GROUP_NAME} deleted.')
    except Exception as e:
        print(f'Error deleting CloudWatch log group: {e}')


def delete_all_resources():
    delete_s3_bucket()
    delete_eb_environment()
    delete_eb_application()
    delete_log_group()
    delete_iam_roles()


if __name__ == '__main__':
    delete_all_resources()