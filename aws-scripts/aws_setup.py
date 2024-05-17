import boto3
import json

# Configuration
REGION = "us-east-2"
S3_BUCKET_NAME = "cloud-clicker-bucket-test"
EB_APP_NAME = "cloud-clicker-test"
EB_ENV_NAME = "cloud-clicker-env-test"
LOG_GROUP_NAME = "cloud-clicker-logs-test"
INSTANCE_PROFILE_NAME = "aws-elasticbeanstalk-ec2-role"
SERVICE_ROLE_NAME = "aws-elasticbeanstalk-service-role"

# Create AWS clients
s3_client = boto3.client("s3", region_name=REGION)
iam_client = boto3.client("iam")
eb_client = boto3.client("elasticbeanstalk", region_name=REGION)
logs_client = boto3.client("logs", region_name=REGION)


def create_s3_bucket():
    """Create an S3 bucket for storing the application data."""
    try:
        s3_client.create_bucket(
            Bucket=S3_BUCKET_NAME, CreateBucketConfiguration={"LocationConstraint": REGION}
        )
        print(f"S3 bucket {S3_BUCKET_NAME} created.")
    except Exception as e:
        print(f"Error creating S3 bucket: {e}")


def create_iam_roles():
    """Create the IAM roles required for the Elastic Beanstalk environment."""
    assume_role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": ["ec2.amazonaws.com", "elasticbeanstalk.amazonaws.com"]},
                "Action": "sts:AssumeRole",
            }
        ],
    }

    # Create instance profile role
    try:
        iam_client.create_role(
            RoleName=INSTANCE_PROFILE_NAME,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy_document),
        )
        iam_client.attach_role_policy(
            RoleName=INSTANCE_PROFILE_NAME,
            PolicyArn="arn:aws:iam::aws:policy/AWSElasticBeanstalkWebTier",
        )
        iam_client.attach_role_policy(
            RoleName=INSTANCE_PROFILE_NAME,
            PolicyArn="arn:aws:iam::aws:policy/AWSElasticBeanstalkMulticontainerDocker",
        )
        iam_client.attach_role_policy(
            RoleName=INSTANCE_PROFILE_NAME,
            PolicyArn="arn:aws:iam::aws:policy/AWSElasticBeanstalkWorkerTier",
        )
        iam_client.attach_role_policy(
            RoleName=INSTANCE_PROFILE_NAME,
            PolicyArn="arn:aws:iam::aws:policy/CloudWatchLogsFullAccess",
        )
        print(f"Instance profile role {INSTANCE_PROFILE_NAME} created and policies attached.")
    except Exception as e:
        print(f"Error creating instance profile role: {e}")

    # Create service role
    try:
        iam_client.create_role(
            RoleName=SERVICE_ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy_document),
        )
        iam_client.attach_role_policy(
            RoleName=SERVICE_ROLE_NAME,
            PolicyArn="arn:aws:iam::aws:policy/service-role/AWSElasticBeanstalkService",
        )
        print(f"Service role {SERVICE_ROLE_NAME} created and policy attached.")
    except Exception as e:
        print(f"Error creating service role: {e}")

    # Create instance profile
    try:
        iam_client.create_instance_profile(InstanceProfileName=INSTANCE_PROFILE_NAME)
        iam_client.add_role_to_instance_profile(
            InstanceProfileName=INSTANCE_PROFILE_NAME, RoleName=INSTANCE_PROFILE_NAME
        )
        print(f"Instance profile {INSTANCE_PROFILE_NAME} created and role added.")
    except Exception as e:
        print(f"Error creating instance profile: {e}")


def create_eb_application():
    """Create the Elastic Beanstalk application."""
    try:
        eb_client.create_application(
            ApplicationName=EB_APP_NAME, Description="Cloud Clicker Application"
        )
        print(f"Elastic Beanstalk application {EB_APP_NAME} created.")
    except Exception as e:
        print(f"Error creating Elastic Beanstalk application: {e}")


def create_eb_environment():
    """Create the Elastic Beanstalk environment."""
    try:
        eb_client.create_environment(
            ApplicationName=EB_APP_NAME,
            EnvironmentName=EB_ENV_NAME,
            SolutionStackName="64bit Amazon Linux 2023 v4.0.12 running Python 3.11",
            OptionSettings=[
                {
                    "Namespace": "aws:autoscaling:launchconfiguration",
                    "OptionName": "IamInstanceProfile",
                    "Value": INSTANCE_PROFILE_NAME,
                },
                {
                    "Namespace": "aws:elasticbeanstalk:environment",
                    "OptionName": "ServiceRole",
                    "Value": SERVICE_ROLE_NAME,
                },
            ],
        )
        print(f"Elastic Beanstalk environment {EB_ENV_NAME} created.")
    except Exception as e:
        print(f"Error creating Elastic Beanstalk environment: {e}")


def create_log_group():
    """Create a CloudWatch log group for storing logs."""
    try:
        logs_client.create_log_group(logGroupName=LOG_GROUP_NAME)
        print(f"CloudWatch log group {LOG_GROUP_NAME} created.")
    except Exception as e:
        print(f"Error creating CloudWatch log group: {e}")


def main():
    create_s3_bucket()
    create_iam_roles()
    create_eb_application()
    create_eb_environment()
    create_log_group()


if __name__ == "__main__":
    main()
