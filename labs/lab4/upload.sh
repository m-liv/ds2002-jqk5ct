#!/bin/bash

# Positional arguments
file=$1
bucket=$2
expiration=$3
path="s3://$bucket"

# Upload file to specified bucket
aws s3 cp $file $path

# Set presign to specified expiration seconds
aws s3 presign --expires-in $expiration "$path/$file"

