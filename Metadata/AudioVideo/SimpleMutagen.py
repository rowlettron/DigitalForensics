import mutagen
import pprint
import os
import inspect

os.system('cls')

pp = pprint.PrettyPrinter(indent=4)

info = mutagen.File("C:\\Projects\\Python\\DigitalForensics\\EmbeddedMetaData\\Walk Like An Egyptian.mp3")

print(info.filename)
print(info.info)

#for i in inspect.getmembers(info):
#    # Ignores anything starting with underscore 
#    # (that is, private and protected attributes)
#    if not i[0].startswith('_'):
#        # Ignores methods
#        if not inspect.ismethod(i[1]):
#            print(i)

#vars(info)

#dir(info)

#pp.pprint(info)


print("#################################################################################################################")

#print(info.text)

