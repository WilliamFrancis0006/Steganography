import codecs
import sys

try:
    
    if(sys.argv[1] == "-b"):
        METHOD = "BIT"
    elif(sys.argv[1] == "-B"):
        METHOD = "BYTE"
    else:
        print("First parsed argument must be -b or -B.")
        sys.exit()

    if(sys.argv[2] == "-s"):
        TYPE = "STORE"
    elif(sys.argv[2] == "-r"):
        TYPE = "RETRIEVE"
    else:
        print("Second parsed argument must be -s or -r.")
        sys.exit()

    if(sys.argv[3][:2] ==  "-o"):
        OFFCHECK = sys.argv[3][2:]
        if(OFFCHECK == ""):
            print("Third parsed argument must be -o<val>. Please include a numeric value")
            sys.exit()
        else:
            OFFSET = int(OFFCHECK) 
    else:
        print("Third parsed argument must be -o<val>.")
        sys.exit()

    if(sys.argv[4][:2] == "-i"):
        INTCHECK = sys.argv[4][2:]
        if(INTCHECK == ""):
            print("Fourth parsed argument must be -i<val>. Please include a numeric value.")
            sys.exit()
        else:
            INTERVAL = int(INTCHECK)
    else:
        print("Fourth parsed argument must be -i<val>.")
        sys.exit()

    if(sys.argv[5][:2] == "-w"):
        WFILE = sys.argv[5][2:]
        if(WFILE == ""):
            print("Fifth parsed argument must be -w<val>. Please include a numeric value.")
            sys.exit()
        else:
            wf = open(WFILE, "rb")
            wnohex = list(wf.read())
            wdata = []
            for w in wnohex:
                wdata.append(hex(ord((w)))[2:])
    else:
        print("Fifth parsed argument must be -w<val>.")
        sys.exit()

    if(TYPE == "STORE"):
        if(sys.argv[6][:2] == "-h"):
            HFILE = sys.argv[6][2:]
            if(HFILE == ""):
                print("Sixth parsed argument must be -h<val>. Please include a numeric value.")
                sys.exit() 
            else:
                hf = open(HFILE, "rb")
                hnohex = list(hf.read())
                hhex = hex(hnohex)    # hex() = python 3 function converts int to hex (im not sure if it is in an integer format, need to remove space or \n  
                hdata = []
                for h in hhex:
                    hdata.append(h[2:])
                endList = ['\x00', '\xff', '\x00', '\x00', '\xff', '\x00']
                eList = ['00', 'ff', '00', '00', 'ff', '00']
                hdata.extend(eList)

        else:
            print("Sixth parsed argument must be -h<val> if type is store (-s).")
            sys.exit()
except:
    print("Be sure to use this format: python steg.py -(bB) -(sr) -o<val> [-i<val>] -w<val> [-h<val>]")
    sys.exit()


data = []


if(METHOD == "BIT"):
    if(TYPE == "STORE"):
        k = 0
        for i in endList:
            endList[k] = ord(i)
            k += 1

        i = OFFSET
        j = 0
        while( j < len(hdata)):
            for l in range(8):
                wdata &= 0b11111110
                wdata[i] |= ((hidden_bytes[j] & 0b10000000) >> 7)
                hdata[j] = hdata[j] << 1
                i += INTERVAL
            j += 1
        
        m = 0
        for l in wdata:
            hdata[m] = chr(l)
            sys.stdout.write(hdata[m])
            m += 1
        
    elif(TYPE == "RETRIEVE"):
        i = OFFSET
        j = 0
        endList = []
        sent = ['\x00', '\xff', '\x00', '\x00', '\xff', '\x00']
        m = 0
        for i in sent:
            sent[m] = ord(i)

        while(endList != sent):
            hdata.append(0b0)
            for l in range(8):
                hdata[i] <<= 1
                lsb = wdata[i] & 1
                hdata = (hdata[j] & 0b11111110) | lsb
                i += INTERVAL
            if(hdata >= 6):
                endList = hdata[-6:]
            j += 1

        z = 0
        for x in hdata:
            hdata[z] = chr(i)
            system.out.write(hdata[z])


    else:
        print("A horrible error occured with the second parsed argument. Exiting...")
        sys.exit()


elif(METHOD == "BYTE"):
    if(TYPE == "STORE"):
        i = 0
        while(i < len(hdata)):
            wdata[OFFSET] = hdata[i]
            OFFSET += INTERVAL
            i += 1

        wbyte = []
        for k in range(0, len(wdata), 2):
            wbyte.append(chr(int(wdata[k], 16)))
        for l in wbyte:
            sys.stdout.write(l) # this needs to be in bytes but idk how to make this work
                                # byte() python function??
        wf.close()
        hf.close()

    elif(TYPE == "RETRIEVE"):
        endList = []
        i = 0
        sent = ['00', 'ff', '00', '00', 'ff', '00']
        hdata = []
        while(endList != sent):
            # when this hits the buffer (00 ff 00 00 ff 00) it needs to stop
            # a seperate while statement? ( while buffer is not (00 ff 00 00 ff 00) )
            hdata.append(wdata[OFFSET])
            OFFSET += INTERVAL
            i += 1
            if(len(hdata) >= 6):
                endList = hdata[-6]

        for l in data:
            sys.stdout.write(chr(l)) # this also needs to be in bytes
        wf.close()              # byte() python function??                

    else:
        print("A horrible error has occured with the second parsed argument. Exiting...")
        sys.exit()

else:
    print("A horrible error has occurred.")
    sys.exit()
