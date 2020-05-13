
def get_upload_path(instance, filename):
    return "user_{id}/{file}".format(id=instance.user.id, file=filename)
