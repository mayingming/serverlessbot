# serverlessbot

First of all, you will need an AWS account
Create a S3 bucket in your account, and make it public access.
And then go to the IAM, create or modify a role, copy the arn to the serverless.yml, just under the attribute "role". 
Under your role permission, attach administratoraccess, awslambdaexecute, after that, you will need to add an inline policy, a json like this:
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ExampleStmt",
            "Action": [
                "s3:*"
            ],
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::{yourbucketname}/*"
            ]
        }
    ]
}
Then deploy it and you are good to go!
