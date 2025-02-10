from pyfingerprint.pyfingerprint import PyFingerprint
from cafeteria.models import Student

try:
    f = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)

    print('Waiting for finger...')
    while not f.readImage():
        pass

    f.convertImage(0x01)

    result = f.searchTemplate()
    positionNumber = result[0]

    if positionNumber == -1:
        print('Fingerprint not recognized!')
    else:
        student = Student.objects.get(fingerprint_id=positionNumber)
        print(f'Authenticated: {student.user.username}')

except Exception as e:
    print(f"Error: {e}")
