
#after run this code it will generate image to be run ""filexr.img
f=open("fileImage.img", "wb")
f.write(bytearray([0xeb ,0x3c,0x90]))  #-->magic bit like MBR
f.write('TEXTCODE' .encode('asci'))     #--> manufacturer name 
f.write(bytearray([0x00,0x02]))
f.write(bytearray([0x01]))
f.write(bytearray([0x01 ,0x00]))
f.write(bytearray([0x01]))
f.write(bytearray([0x10 ,0x00]))
f.write(bytearray([0x00,0x20]))
f.write(bytearray([0xf8]))
f.write(bytearray([0x20,0x00]))

f.write(bytearray([0,0,0,0,0,0,0,0]))
f.write(bytearray([0x00,0x00,0x00,0x00]))
f.write(bytearray([0x80,0]))

f.write(bytearray([0x29]))
f.write(bytearray([0x41,0x42,0x43,0x44]))

f.write('TEXTDIR' .encode('asci'))
f.write('FAT16' .encode('asci'))


for i in range (0, ox1c0):
    f.write(bytearray([0]))

f.write(bytearray([0x20,0x00]))

f.write(bytearray([0xf8,0xff,0xff,0xff]))

f.write(bytearray([0x80]*8192))
f.write(bytearray([0x80]*512))

for i in range (8192):
    f.write(bytearray([0x80]*512))

f.close()