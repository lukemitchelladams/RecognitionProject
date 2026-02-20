# AWS Rekognition Image Labeling

A Python script that uses AWS Rekognition to detect and visualize labels (objects, scenes, and concepts) in images stored on Amazon S3.

## Overview

This script performs the following operations:
1. Validates access to an S3 image object
2. Detects labels in the image using AWS Rekognition
3. Displays the image with bounding boxes and confidence scores for detected objects
4. Returns the count of detected labels

## Dependencies

- `boto3` - AWS SDK for Python
- `botocore` - Low-level interface to AWS services
- `matplotlib` - Plotting and visualization library
- `Pillow (PIL)` - Image processing library

Install dependencies with:
```bash
pip install boto3 botocore matplotlib Pillow
```

## Prerequisites

1. **AWS Account** with configured credentials
2. **IAM Permissions** - The credentials must have:
   - `s3:GetObject` permission for S3
   - `rekognition:DetectLabels` permission for Rekognition
3. **S3 Bucket** containing your image files
4. **Rekognition Access** enabled in your AWS account

## Setup

### AWS Credentials

Configure your AWS credentials using one of these methods:
- AWS CLI: `aws configure`
- Environment variables: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
- AWS credentials file: `~/.aws/credentials`
- IAM roles (if running on EC2 or Lambda)

## Usage

### Basic Usage

```python
from Rekognition import detect_labels

# Detect labels in an image
label_count = detect_labels('image_file_name', 'bucket_name')
print(f"Detected {label_count} labels")
```

### Command Line

Edit the `main()` function with your S3 bucket and image file name, then run:
```bash
python Rekognition.py
```

## Function Reference

### `detect_labels(photo, bucket)`

Detects labels in an image stored on S3 and visualizes results.

**Parameters:**
- `photo` (str): The S3 object key (file name/path) of the image
- `bucket` (str): The S3 bucket name

**Returns:**
- `int`: Number of labels detected

**Raises:**
- `botocore.exceptions.ClientError`: If S3 access fails or Rekognition API error occurs

**Process:**
1. Verifies S3 object exists and is accessible
2. Determines the S3 bucket region
3. Creates a Rekognition client in the appropriate region
4. Calls DetectLabels API (max 10 labels)
5. Prints detected labels and confidence scores
6. Downloads image from S3 and displays with bounding boxes
7. Overlays label names and confidence percentages on the visualization

## Output

The script displays:
- Label names detected in the image
- Confidence scores (0-100%) for each label
- Visual bounding boxes around detected objects
- Label annotations with confidence percentages

## Error Handling

The script provides diagnostic messages for common issues:
- **S3 Access Errors**: Checks bucket name, object key (case-sensitive), region, and IAM permissions
- **Region Mismatch**: Automatically detects bucket region and creates Rekognition client accordingly
- **Rekognition Errors**: Provides guidance on region compatibility and IAM permissions

## Example

```python
# Detect labels in a product image
label_count = detect_labels('products/smartphone.jpg', 'my-image-bucket')
# Output:
# Detected labels for products/smartphone.jpg
# 
# Label: Electronics
# Confidence: 99.5
# 
# Label: Phone
# Confidence: 98.2
# ...
```

## Notes

- Maximum of 10 labels returned per image (configurable in the `MaxLabels` parameter)
- Rekognition client is created in the same region as the S3 bucket
- Supports all image formats recognized by AWS Rekognition (JPEG, PNG, GIF, BMP)
- Image is displayed using matplotlib; close the window to continue execution

## License

This script uses AWS services. Refer to AWS pricing for Rekognition and S3 usage costs.
