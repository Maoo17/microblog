sudo touch ansible/aws_keys.yml
sudo echo “aws_access_key: $AWS_ACCESS_KEY” > ansible/aws_keys.yml
sudo echo “aws_secret_key: $AWS_SECRET_KEY” >> ansible/aws_keys.yml
sudo echo “aws_security_token: $AWS_SECURITY_TOKEN” >> ansible/aws_keys.yml