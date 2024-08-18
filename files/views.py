from django.http import JsonResponse


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