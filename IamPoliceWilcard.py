import json
import boto3
import botocore
import time


def lambda_handler(event, context):

    client = boto3.client('iam')
    policyArn = 'arn:aws:iam::<accountId>:policy/<policyname>'
    wildcard = '*'

    version = client.get_policy(
        PolicyArn=policyArn
    )
    getDefaultVersion = version['Policy']['DefaultVersionId']

    explicit = []

    for i in getDefaultVersion:
        version_number = i.isdigit()
        if (version_number == True):
            for j in range(0, int(i)):
                versions = 'v'+str(j+1)
                try:
                    if (versions != 'v5'):
                        describe = client.get_policy_version(
                            PolicyArn=policyArn,
                            VersionId=versions
                        )
                        check = describe["PolicyVersion"]["Document"]["Statement"]
                        version = describe["PolicyVersion"]["VersionId"]
                        for i in check:
                            action = i["Action"]
                            for i in action:
                                explicit.append(i)
                        find = [s for s in explicit if wildcard in s]
                        if (len(find) > 0):
                            try:
                                delete = client.delete_policy_version(
                                    PolicyArn=policyArn,
                                    VersionId=version
                                )
                                print("Deleted :",delete)
                            except:
                                pass
                            finally:
                                deletePolicy = client.delete_policy(
                                    PolicyArn=policyArn
                                )
                                print(
                                    "Deleted Policy cause of not following Rules", deletePolicy)
                        else:
                            print("Policy is following Rules according to Anirudh")
                except:
                    pass
