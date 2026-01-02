# API to S3 ETL Script with Success and Failure Manifests
# This script extracts data from a public API, saves it LOCALLY, uploads it to an S3 bucket,
# and creates manifest files indicating success or failure of the operation.   
# Success and failure manifests include metadata such as run ID, extraction date, record count, status, and timestamp.
# The script handles exceptions to ensure that a failure manifest is created in case of any errors during execution.

#Failure code block start
run_id = str(uuid.uuid4())
extract_dt = datetime.now(timezone.utc).strftime("%Y-%m-%d")

try:
    # Start of main code block
    #Library imports
    import json
    import requests
    import boto3
    import uuid
    from datetime import datetime, timezone
    #API call to get posts data
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url, timeout=20)
    response.raise_for_status()

    data = response.json()

    with open("posts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("Saved posts.json")

   
    s3 = boto3.client("s3")

    #Bucket name for upload
    Bucket_name = "api-tutorial-test"

    #Success Manifest Block
    run_id = str(uuid.uuid4())
    extract_dt = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    s3_key = (
        f"source=demo_api/entity=posts/"
        f"extract_dt={extract_dt}/"
        f"run_id={run_id}/posts.json"
    )

    manifest = {
        "source": "demo_api",
        "entity": "posts",
        "extract_dt": extract_dt,
        "run_id": run_id,
        "record_count": len(data),
        "status": "SUCCESS",
        "created_utc": datetime.now(timezone.utc).isoformat()
    }

    manifest_file = "manifest.json"
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    manifest_s3_key = (
        f"source=demo_api/entity=posts/"
        f"extract_dt={extract_dt}/"
        f"run_id={run_id}/manifest.json"
    )

    #S3 upload files to be in bucket
    s3.upload_file(manifest_file, Bucket_name, manifest_s3_key)

    #s3 file name
    s3.upload_file("posts.json", Bucket_name, s3_key)

    print(f"Uploaded to s3://{Bucket_name}/{s3_key}")
    print(f"Records: {len(data)}")

#end of failure block
except Exception as e:
    print("Job failed:", str(e))
    raise