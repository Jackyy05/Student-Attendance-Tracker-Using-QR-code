from MyQR import myqr
import os
import base64

f = open('students.txt', 'r')
line = f.read().split('\n')
print(line)

for i in range(0, len(line)):
    data = line[i].encode()
    name = base64.b64encode(data)
    version, level, qr_name = myqr.run(
        str(name),
        level='H',
        version=1,

        # For Background
        colorized=True,
        contrast=1.0,
        brightness=1.0,
        save_name=str(line[i]+'.bmp'),
        save_dir=os.getcwd()
    )
