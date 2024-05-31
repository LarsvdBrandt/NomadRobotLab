# NOMAD Oasis Customization Repository 

This folder contains the NOMAD Oasis source code with code changes to enhance the access control for the RobotLab. 

## code changes:
Code changes on upload API:
```
.\nomad\app\v1\routers\uploads.py
```

Updated code:
```
def is_user_upload_viewer(upload: Upload, user: Optional[User]):
    if user is None:
        return False

    if user.is_admin:
        return True

    if user.user_id in upload.writers:
        return True
    
    if user.user_id in upload.reviewers:
        return True

    return False

def is_user_upload_writer(upload: Upload, user: User):
    if user.is_admin:
        return True

    if user.user_id in upload.writers:
        return True

    group_ids = get_group_ids(user.user_id)
    if not set(group_ids).isdisjoint(upload.writer_groups):
        return True

    return False
```

## Rebuild docker image
To rebuild the docker image, go into the root directory of the source code where the docker file is located and run the following command:
```
docker build -t <image-name>:<image-tag> .
```

After succesfully building the image, go to the docker compose folder in root directory of Git repository. 
```
..\..\docker-compose\nomad-oasis\docker-compose.yaml
```

Add the new image to the app and worker in the docker-compose.yaml and the following command:
```
run docker-compose up -d
```