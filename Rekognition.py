import boto3
import botocore
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
from io import BytesIO


def detect_labels(photo, bucket):
    """Run Rekognition detect_labels on an S3 object after validating access.

    This function performs an S3 head_object check, determines the bucket region,
    creates a Rekognition client in that region, and then calls DetectLabels.
    It raises the original exception after printing a clearer diagnostic message.
    """
    s3_client = boto3.client('s3')

    # Verify the object exists and is accessible
    try:
        s3_client.head_object(Bucket=bucket, Key=photo)
    except botocore.exceptions.ClientError as e:
        code = e.response.get('Error', {}).get('Code')
        message = e.response.get('Error', {}).get('Message')
        print(f"S3 access error ({code}): {message}")
        print("Check: bucket name, object key (case-sensitive), region, and IAM permissions (s3:GetObject).")
        raise

    # Determine the bucket region and create Rekognition client in that region
    try:
        loc = s3_client.get_bucket_location(Bucket=bucket).get('LocationConstraint')
        region = loc if loc else 'us-east-1'
    except botocore.exceptions.ClientError as e:
        print("Unable to determine bucket region:", e)
        raise

    rek_client = boto3.client('rekognition', region_name=region)

    try:
        response = rek_client.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
            MaxLabels=10)
    except botocore.exceptions.ClientError as e:
        print("Rekognition API error:", e)
        print("Ensure Rekognition and S3 are in compatible regions and the calling credentials have Rekognition access.")
        raise

    print('Detected labels for ' + photo)
    print()

    # Print label information
    for label in response.get('Labels', []):
        print("Label:", label.get('Name'))
        print("Confidence:", label.get('Confidence'))
        print()

    # Load the image from S3 (use resource for streaming)
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, photo)
    img_data = obj.get()['Body'].read()
    img = Image.open(BytesIO(img_data))

    # Display the image
    plt.imshow(img)
    ax = plt.gca()

    # Plot bounding boxes
    for label in response.get('Labels', []):
        for instance in label.get('Instances', []):
            bbox = instance.get('BoundingBox', {})
            left = bbox.get('Left', 0) * img.width
            top = bbox.get('Top', 0) * img.height
            width = bbox.get('Width', 0) * img.width
            height = bbox.get('Height', 0) * img.height

            rect = patches.Rectangle((left, top), width, height, linewidth=1, edgecolor='r', facecolor='none')
            ax.add_patch(rect)

            label_text = f"{label.get('Name')} ({round(label.get('Confidence',0),2)}%)"
            plt.text(left, max(top - 10, 0), label_text, color='r', fontsize=8, bbox=dict(facecolor='white', alpha=0.7))

    plt.show()

    return len(response.get('Labels', []))

def main():
    photo = 'image_file_name'
    bucket = 'bucket_name'
    label_count = detect_labels(photo, bucket)
    print("Labels detected:", label_count)

if __name__ == "__main__":
    main()
