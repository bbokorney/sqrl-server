import os

from base64 import b64encode

def populate():
    user = User(username="squirrel")
    user.set_password(settings.SHARED_USER_PASSWORD)
    user.save()

    key_text = open("key.pub").read()
    SQRLUser.objects.get_or_create(user=user, identity_key=b64encode(key_text))

if __name__ == '__main__':
    print "Populating database."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sqrl.settings')
    from app.models import SQRLUser
    from django.contrib.auth.models import User
    from sqrl import settings
    populate()
