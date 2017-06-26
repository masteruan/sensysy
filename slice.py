result = 'value=34444444'
r = result
slices = [r[0:6], r[6:7], r[7:8], r[8:9], r[9:10], r[10:11], r[11:12], r[12:13], r[13:14]]

print(slices[1])
if slices[1] == "1":
    print ("neopixel bianco")
elif slices[1] == "2":
    print ("neopixel arancione")
elif slices[1] == '3':
    print ("neopixel rosso")
