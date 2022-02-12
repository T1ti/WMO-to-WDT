import sys
import os
import struct

try:
    droppedFile = sys.argv[1] #filepath
except IndexError:
    input("No file dropped. Press any key to exit.")

file_name_with_extension = os.path.basename(droppedFile)

split_tup = os.path.splitext(file_name_with_extension)

file_name = split_tup[0] # filename
file_extension = split_tup[1] # file extension

# print("File Name: ", file_name)
# print("File Extension: ", file_extension)

if file_extension != ".wmo":
    print('File dropped is not a .wmo')
    input()
    raise Exception('File dropped is not a .wmo') # todo : is there a way to keep the error message without closing window ? (using input for now)

upper_extents = [0.0, 0.0, 0.0]
lower_extents = [0.0, 0.0, 0.0]

# read data from WMO File
with open(droppedFile, "rb") as f:
    MVER = f.read(12)
    MOHD_magic = f.read(4)
    print(MOHD_magic)
    if MOHD_magic != b'DHOM':
        if MOHD_magic == b'PGOM':
            print('You dropped a WMO group file.(xxx_000.wmo). You must drop the WMO root file instead (xxx.wmo) ')
            input()
            raise Exception('You dropped a WMO group file.(xxx_000.wmo). You must drop the WMO root file instead (xxx.wmo) ')
        else:
            print('WMO file is corrupted or an invalid version (currently untested with WOTLK+)')
            input()
            raise Exception('WMO file is corrupted or an invalid version (currently untested with WOTLK+)')

    f.read(40) # skip useless header data
    # maybe read flags for mwmo data ? 

    # boundingbox1 = f.read(12)
    upperextent_3 = struct.unpack('f', f.read(4) )[0]
    upperextent_1 = struct.unpack('f', f.read(4) )[0]
    upperextent_2 = struct.unpack('f', f.read(4) )[0]

    lowerextent_3 = struct.unpack('f', f.read(4) )[0]
    lowerextent_1 = struct.unpack('f', f.read(4) )[0]
    lowerextent_2 = struct.unpack('f', f.read(4) )[0]

    upper_extents = [upperextent_1, upperextent_2, upperextent_3]
    lower_extents = [lowerextent_1, lowerextent_2, lowerextent_3]
    # print(upper_extents)
    # print(lower_extents)


print("Enter the WoW path of your WMO, eg 'World\wmo\Dungeon\AZ_Blackrock\Blackrock_lower_guild.wmo'")
WMO_WoW_path = input(">")
print("WMO WoW Path = " + WMO_WoW_path)

wdt_filepath = os.path.join( os.getcwd(), file_name + '.wdt') 

print("\nWritting WDT file to current folder (" + wdt_filepath + ")")

# write WDT
with open(wdt_filepath, "wb") as f:

    # MVER
    f.write(b'REVM') # magic
    f.write( struct.pack('I', 4) ) # byte_size
    f.write( struct.pack('I', 18) ) # version

    # MPHD
    f.write(b'DHPM') # magic
    f.write( struct.pack('I', 32) ) # byte_size
    f.write( struct.pack('I', 1) ) # flags, set flag 0x1
    f.write( struct.pack('I', 0) ) # unknown
    i = 0
    while i < 6:
        f.write( struct.pack('I', 0) ) # unused, 6x uint 32
        i += 1

    # MAIN
    f.write(b'NIAM') # magic
    f.write( struct.pack('I', 32768) ) # byte_size
    i = 1
    while i < 4097: #write 4096 chunks of 8 empty bytes
        f.write( b'\x00\x00\x00\x00\x00\x00\x00\x00' ) # flags and async id, always empty for our wdt.
        i += 1
    
    # MWMO
    filepath_lenght = len(WMO_WoW_path)
    f.write(b'OMWM') # magic
    f.write( struct.pack('I', filepath_lenght + 1 ) ) # byte_size, +1 for the padding
    f.write(str.encode(WMO_WoW_path))
    f.write(b'\x00') # empty byte padding

    # MODF
    f.write(b'FDOM') # magic
    f.write( struct.pack('I', 64) ) # byte_size
    f.write( b'\x00\x00\x00\x00\x00\x00\x00\x00' ) # ID and unique ID

    position = (0.0, 0.0, 0.0)
    for pos in position:
        f.write( struct.pack('f', pos) ) # position

    orientation = (0.0, 0.0, 0.0)
    for orient in orientation:
        f.write( struct.pack('f', orient) ) #orientation

    for upper_extent in upper_extents:
        f.write( struct.pack('f', upper_extent) ) # upper extents

    for lower_extent in lower_extents:
        f.write( struct.pack('f', lower_extent) ) # lower extents

    f.write( struct.pack('H', 0) ) # flags, 0 ?
    f.write( struct.pack('H', 0) ) # doodad set id, 0 ?
    f.write( struct.pack('H', 0) ) # name set id, 0 ?
    f.write( struct.pack('H', 0) ) # padding


print("Succesfully created WDT file " + file_name + '.wdt, Rename it to your map name if needed.' )

input("\nPress enter to close")

