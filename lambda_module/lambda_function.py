import boto3
import os
import json
from botocore.exceptions import ClientError
from lambda_module.py_package.graph_builder import WeightGraphBuilder
from lambda_module.py_package.graph_exporter import PickleGraphExporter
from lambda_module.py_classes.text_analyzer import TextAnalyzer

s3_client = boto3.client("s3")


def lambda_handler(event, context):
    response = s3_client.list_objects_v2(Bucket="lgex-download-bucket")
    object_keys = [obj["Key"] for obj in response.get("Contents", [])]

    download_paths = []
    for key in object_keys:
        local_path = f"/tmp/{os.path.basename(key)}"
        print(f"Downloading {key} from lgex-download-bucket to {local_path}")

        try:
            s3_client.download_file("lgex-download-bucket", key, local_path)
            download_paths.append(local_path)
        except ClientError as e:
            print(f"Could not download {key}: {e}")

    analyzer = TextAnalyzer()
    graph_builder = WeightGraphBuilder()
    graph_exporter = PickleGraphExporter()

    words = analyzer.extract_words_by_length_from(download_paths, [3, 4, 5])
    new_graph = graph_builder.build_graph(words)

    local_graph_path = "/tmp/lgex_graph.pkl"
    graph_exporter.export_graph(new_graph, local_graph_path)

    upload_key = "lgex_graph.pkl"
    s3_client.upload_file(local_graph_path, "lgex-app-bucket", upload_key)

    print(f"Batch triggered. Processed {len(object_keys)} files from lgex-download-bucket.")
    print(f"Graph rebuilt and uploaded to lgex-app-bucket/{upload_key}.")

    return {
        "statusCode": 200,
        "body": f"Processed {len(object_keys)} files from lgex-download-bucket."
    }
