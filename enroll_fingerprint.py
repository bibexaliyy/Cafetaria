from pyfingerprint.pyfingerprint import PyFingerprint
from cafeteria.models import Student
from django.contrib.auth.models import User

try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
    if not f.verifyPassword():
        raise ValueError("Incorrect Fingerprint Password")

    print('Waiting for finger...')
    while not f.readImage():
        pass

    f.convertImage(0x01)

    result = f.searchTemplate()
    positionNumber = result[0]

    if positionNumber >= 0:
        print('Fingerprint already exists!')
    else:
        f.createTemplate()
        positionNumber = f.storeTemplate()
        print(f'Fingerprint stored at position {positionNumber}')

        # Create Student Profile
        user = User.objects.create_user(username=f"student_{positionNumber}")
        student = Student.objects.create(user=user, fingerprint_id=positionNumber, school_category="Science")
        print(f"Student {user.username} registered.")

except Exception as e:
    print(f"Error: {e}")
