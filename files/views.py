from django.http import JsonResponse
from django.conf import settings
import boto3
import json
import re
from .utils import s3_client

def versions(request):
    data = list(DUMMY_FILES_0.keys())
    if data:
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Version not found'}, status=404)


def version_files(request, version):
    data = DUMMY_FILES_0.get(version)
    if data:
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Version not found'}, status=404)


def files(request, filetype):
    data = filetype
    if data:
        return JsonResponse({}, status=200)
    else:
        return JsonResponse({'error': 'Version not found'}, status=404)

# NEW


def get_dashboard(request):
    return JsonResponse({}, status=204)


def get_files(subdirectories):
    file_information = []
    allowed_versions = []
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    if subdirectories and subdirectories[0] == 'patch':
        allowed_versions = settings.S3_ALLOWED_VERSIONS

    for subdirectory in subdirectories:
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=f"directory/{subdirectory}",
        )

        if "Contents" in response:
            for obj in response["Contents"]:
                file_key = obj["Key"]
                # key = [file_key] if any(version in file_key for version in allowed_versions) else []
                # if len(key) == 0: continue

                file_name = file_key.split("/")[-1]
                file_size = obj["Size"]
                upload_date = obj["LastModified"].strftime("%Y-%m-%d %H:%M:%S")

                if file_size == 0: continue

                presigned_url = s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": bucket_name, "Key": file_key},
                    ExpiresIn=3600
                )

                file_information.append({
                    "version": subdirectory,
                    "name": file_name,
                    "size": file_size,
                    "upload_date": upload_date,
                    "url": presigned_url
                })

    return JsonResponse({"files": file_information}, status=200)


def get_files_by_version(request, filetype, version):
    file_information = []
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    response = s3_client.list_objects_v2(
        Bucket=bucket_name,
        Prefix=f"directory/{version}/",
    )

    if "Contents" in response:
        for obj in response["Contents"]:
            file_key = obj["Key"]
            file_name = file_key.split("/")[-1]
            file_size = obj["Size"]
            upload_date = obj["LastModified"].strftime("%Y-%m-%d %H:%M:%S")

            if file_size == 0: continue

            presigned_url = s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": file_key},
                ExpiresIn=3600
            )

            file_information.append({
                "version": version,
                "name": file_name,
                "size": file_size,
                "upload_date": upload_date,
                "url": presigned_url
            })

    return JsonResponse({"files": file_information}, status=200)


def get_version_and_file(request, filetype):
    try:
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        response = s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix="directory/",
            Delimiter="/"
        )

        versions_all = [prefix["Prefix"] for prefix in response.get("CommonPrefixes", [])]
        version_patterns = {
            "install": re.compile(r"^\S+/([\d]+(?:\.[\d]+)*(?:[a-zA-Z_-]*\d*)?)/$"),
            "patch": re.compile(r"^\S+/(patch)/$"),
            "jdk": re.compile(r"^\S+/(java)/$"),
            "license": re.compile(r"^\S+/(license)/$")
        }
        allowed_versions = settings.S3_ALLOWED_VERSIONS
        if filetype == "install" and allowed_versions:
            pattern_str = r"^\S+/(" + "|".join(re.escape(ver) for ver in allowed_versions) + r")/$"
            version_pattern = re.compile(pattern_str)
        else:
            version_pattern = version_patterns.get(filetype, re.compile(r""))

        file_versions = [match.group(1) for path in versions_all if (match := version_pattern.match(path))]
        file_information = json.loads(get_files(file_versions).content)

        return JsonResponse({"versions": file_versions, "files": file_information["files"]})

    except Exception as e:
        return JsonResponse({"error": f"Fail to retrieve directories: {str(e)}"}, status=500)


def get_install_version_files(request):
    return


def get_file(request):
    file_key = request.GET.get("file_key")

    if not file_key:
        return JsonResponse({"error": "file_key is required"}, status=400)

    try:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        bucket_name = settings.AWS_STORAGE_BUCKET_NAME

        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": file_key},
            ExpiresIn=3600
        )

        return JsonResponse({"url": presigned_url})

    except Exception as e:
        return JsonResponse({"error": f"Fail to create Presigned URL: {str(e)}"}, status=500)


DUMMY_FILES_0 = {
    "v1.0": {
        "version": "v1.0",
        "files": [
            {"name": "file_linux_v1_0.txt", "size": 15360, "upload_date": "2024-08-13"},
            {"name": "file_windows_v1_0b.txt", "size": 20480, "upload_date": "2024-08-14"},
            {"name": "lena-cloud-linux_na_x86_64-1.3.3.0.tar.gz", "size": 20480, "upload_date": "2024-08-14"},
            {"name": "lena-cloud-win_na_x86_64-1.3.3.0.tar.gz", "size": 20480, "upload_date": "2024-08-14"},
            {"name": "lena-web-linux_na_x86_64-1.3.3.0.tar.gz", "size": 20480, "upload_date": "2024-08-14"},
            {"name": "file_windows_v1_0b.txt", "size": 20480, "upload_date": "2024-08-14"},
            {"name": "file_windows_v1_0b.txt", "size": 20480, "upload_date": "2024-08-14"},
            {"name": "file_windows_v1_0b.txt", "size": 20480, "upload_date": "2024-08-14"},
            {"name": "file_windows_v1_0b.txt", "size": 20480, "upload_date": "2024-08-14"},
            {"name": "file_windows_v1_0b.txt", "size": 20480, "upload_date": "2024-08-14"},
            {"name": "file_windows_v1_0b.txt", "size": 20480, "upload_date": "2024-08-14"},
            {"name": "file_windows_v1_0b.txt", "size": 20480, "upload_date": "2024-08-14"},
        ]
    },
    "v2.0": {
        "version": "v2.0",
        "files": [
            {"name": "file_v2_0.txt", "size": 30720, "upload_date": "2024-08-15"},
        ]
    },
}

DUMMY_FILES_1 = [
    {
        "name": "example_file_1.txt",
        "size": 15360,
        "upload_date": "2024-08-13",
        "version": "v1.0",
        "download_url": "http://localhost:8000/media/example_file_1.txt",
    },
    {
        "name": "example_file_2.jpg",
        "size": 204800,
        "upload_date": "2024-08-12",
        "version": "v2.0",
        "download_url": "http://localhost:8000/media/example_file_2.jpg",
    },
    {
        "name": "example_file_3.pdf",
        "size": 1258291,
        "upload_date": "2024-08-11",
        "version": "v1.5",
        "download_url": "http://localhost:8000/media/example_file_3.pdf",
    },
]