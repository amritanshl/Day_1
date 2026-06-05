import boto3
from botocore.exceptions import ClientError
import os

s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')

BUCKET_NAME = "tsample-bucket-amrit-new1"
LOCAL_FILE_PATH = "scraped_market_data.csv"
CLOUD_OBJECT_KEY = "vault/ecommerce/daily_scrape.csv"

def execute_cloud_storage_pipeline():
    print("=== STARTING AWS S3 BOTO3 AUTOMATION LIFECYCLE ===")

    # ==========================================
    # ACTION 1: CREATE THE CLOUD BUCKET
    # ==========================================
    try:
        print(f"\n[Action] Creating globally unique bucket: '{BUCKET_NAME}'...")
        
        # We use the client to issue a creation request
        # Note: If you are using a region outside us-east-1, you must provide a LocationConstraint parameter
        s3_client.create_bucket(Bucket=BUCKET_NAME)
        print(f" Success: Bucket '{BUCKET_NAME}' is active in Amazon data centers.")
        
    except ClientError as e:
        # Check if the bucket name error is due to name conflicts
        if e.response['Error']['Code'] == 'BucketAlreadyExists':
            print("Failure: Name conflict! That exact name is already taken by someone else on Earth.")
            return
        else:
            print(f" Critical Error: {e}")
            return

    # ==========================================
    # ACTION 2: UPLOAD LOCAL FILE AS S3 OBJECT
    # ==========================================
    try:
        print(f"\n[Action] Uploading '{LOCAL_FILE_PATH}' to S3 as object key: '{CLOUD_OBJECT_KEY}'...")
        
        # Instantiate a reference to our new target Bucket object mapping layer
        bucket = s3_resource.Bucket(BUCKET_NAME)
        
        # Execute upload_file: (Local Source Path, Target S3 Key String)
        bucket.upload_file(Filename=LOCAL_FILE_PATH, Key=CLOUD_OBJECT_KEY)
        print("✅Success: Local text data stream successfully synchronized to AWS Cloud disk.")
        
    except Exception as e:
        print(f" Upload Failed: {str(e)}")

    # ==========================================
    # ACTION 3: LIST FILES INSIDE THE BUCKET
    # ==========================================
    print(f"\n[Action] Listing objects inside bucket '{BUCKET_NAME}':")
    try:
        # Loop over the collection of all object reference summaries inside the bucket mapping
        for obj_summary in bucket.objects.all():
            print(f" Object Found -> Key: {obj_summary.key} | Storage Scale: {obj_summary.size} bytes")
    except Exception as e:
        print(f" Listing Failed: {str(e)}")

    # ==========================================
    # ACTION 4: DOWNLOAD OBJECT BACK TO LOCAL DISK
    # ==========================================
    downloaded_filename = "downloaded_from_cloud.csv"
    try:
        print(f"\n[Action] Downloading object '{CLOUD_OBJECT_KEY}' back to local system space...")
        
        # Target the explicit object key directly from the bucket handle
        bucket.download_file(Key=CLOUD_OBJECT_KEY, Filename=downloaded_filename)
        
        print(f"✅ Success: File pulled from cloud and written locally to '{downloaded_filename}'")
        
        # Print out downloaded file contents to verify it is uncorrupted
        with open(downloaded_filename, 'r') as f:
            print(f"📝 Contents of verified file:\n{f.read().strip()}")
            
    except Exception as e:
        print(f"❌ Download Failed: {str(e)}")

if __name__ == "__main__":
    execute_cloud_storage_pipeline()