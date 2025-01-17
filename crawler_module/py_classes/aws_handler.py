import boto3
import os


class AWSHandler:

    def __init__(self, bucket_name):
        self.region = "us-east-1"
        self.endpoint_url = "http://localhost:4566"
        self.s3_bucket = bucket_name
        self.s3_client = self._get_s3_client()

    def _get_s3_client(self):
        return boto3.client(
            "s3",
            endpoint_url=self.endpoint_url,
            aws_access_key_id="mock_access_key",
            aws_secret_access_key="mock_secret_key",
            region_name=self.region,
        )

    def upload_file_to_s3(self, local_path, s3_key):
        try:
            self.s3_client.upload_file(local_path, self.s3_bucket, s3_key)
            os.remove(local_path)
        except Exception as e:
            raise RuntimeError(f"Failed to upload file to S3: {e}")

    def download_file_from_s3(self, local_path, s3_key):
        try:
            self.s3_client.download_file(self.s3_bucket, s3_key, local_path)
        except Exception as e:
            raise RuntimeError(f"Failed to download file from S3: {e}")

    def get_object_content_from_s3(self, s3_key):
        try:
            response = self.s3_client.get_object(Bucket=self.s3_bucket, Key=s3_key)
            return response["Body"].read()
        except Exception as e:
            raise RuntimeError(f"Failed to get object content from S3: {e}")
