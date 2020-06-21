#PS2 rom unpacker
#находим модуль RESET в ROMDIR и по смещению определяем
#конец первого и начало второго модуля
#читаем второй модуль, который всегда является структурой ROMDIR
#где расположены размеры всех остальных модулей и их название
#to-do: implement 16bytes padding in parseROMDIR function
import os


def romOPEN(romfile): 
    print("Opening:" + romfile)
    romsize = os.path.getsize(romfile)
    #всегда 32мбит
    rom = open(romfile, 'rb')
    return rom

def findROMDIRSIZE( file , romsize ):
    #ROMDIR всегда за RESET
    #Размер ROMDIR = размер всей таблицы + 16 нулевых байтов
    i=0  #счетчик
    a=0  #первый байт R
    b=[] #остальные байты ESET
    d=[] #4 байта где указан размер в little-endian
    e=0  #Место в файле после RESET например 0x2705 для scph-10000
    f=0  #значение размера в big-endian
    g=0  #ROMDIR размер
    h=0  #начало ROMDIR (0x2700 для scph-10000)
    
    print("Searching for RESET module size")
    for i in range(0,romsize): #Проход по файлу
        a = file.read(1)
        
        if (a[0]==0x52):  #R
            b=list(file.read(4))
            if (b[0:] ==[0x45,0x53,0x45,0x54]): #ESET
                e=file.tell() #0x2705 для scph-10000
                h=e-5
                print("Found at:" + hex(h))
             
                f=parseSIZE(file,(e-5+10+2)) 

                #print("Little-endian:"+d.hex())
                print("RESET size:" +hex (f))
                print("Reset module ends at:" + hex(e-6))

                f=parseSIZE(file,(h+0x10+2+10))

                print("ROMDIR size:" +hex (f))


                #Возвращаем начало ROMDIR и его размер
                return h,f
                break
        a=[]
        b=[]

def parseSIZE (file, offset):
    file.seek((offset)) #переходим к байтам размера
    d=(file.read(4)) #читаем их
    f=int("0x"+ (d[::-1]).hex()  ,16) #меняем порядок байт
    return f
    
def parseROMDIR(file, romdir_location ):
    print('Modules:')
    #print('')
    i=0                 #Счетчик
    a = romdir_location #Чтобы меньше писать
    b=(((a[1])//16)-1)  #Число модулей
    modules = []        #Модули
    c=''
    cc=''
    #Название модуля для цикла
    d=0                 #Размер модуля для цикла
    e=0 #абсолютный offset для цикла
    temp=[]
    file.seek(a[0])
    for i in range (0,b):
        c=file.read(10)
        cc=c.decode('ascii')
        print(str(i)+'.'+(cc))
        file.seek(file.tell()+2)
        d=parseSIZE (file, file.tell())
        modules.append([cc,hex(e),hex(d)])
        e=e+d        
        
        
    return modules
        

def extractModule(romfile, modules, module_number ):
    #os.mkdir('modules')
    os.chdir('modules')
    romfile.seek(modules[module_number][1])
    print("Module:" + str(modules[module_number][0]) + " extracted")
    print("Offset:"+hex(modules[module_number][1]))
    print("Size:"+hex(modules[module_number][2]))
    print("Size decimal:"+str(modules[module_number][2]))
    module_out=romfile.read(modules[module_number][2])
    f = open(str(module_number), "wb")
    f.write(module_out)
    f.close()


###Не используется:
#structROMDIR = {'name':10,'ext':2,'size':4}
#Формат записей в ROMDIR

filename = 'rom.bin'
size=os.path.getsize(filename)
romfile=romOPEN(filename)
romdir_location = findROMDIRSIZE(romfile, size)
z=parseROMDIR(romfile, romdir_location)
print(z)
innum=input("Type module number to extract:")
extractModule(romfile, z, int(innum))
romfile.close()
