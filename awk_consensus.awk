#!/usr/bin/awk
FILENAME=$1

BEGIN {
    da_count = 0
    relay_count = 0
}


/^contact/ {
    $1 = ""
    DAs[da_count, "contact"] = $0

}

/^dir-source/ {
    DAs[da_count,"nickname"] = $2
    DAs[da_count,"fingerprint"] = $3
    DAs[da_count, "ip1"] = $4
    DAs[da_count, "ip2"] = $5
    da_count++
}

#Relay Line 'r'
/^r [A-z]+/ {
    RELAYs[relay_count, "nickname"] = $2
    RELAYs[relay_count, "ip"] = $7
}

#Relay Line 's'
/^s [A-z]+/ {
    $1 = ""
    RELAYs[relay_count, "flags"] = $0
}

/^p [A-z]+/ {
    $1 = ""
    RELAYs[relay_count, "exit_policy"] = $0
    relay_count++
}




END {

it = 0
print "DAs\n"
for (i=0;i<da_count;i++){
    printf("[%d] %s\n\tIP: %s\n\tContact:%s\n",i+1, DAs[i, "nickname"], DAs[i, "ip1"], DAs[i, "contact"])
}

#print "\nRELAYS\n"
#for (i=0;i<relay_count;i++){
#    printf("[%d] %s\n\tIP: %s\n\tFlags:%s\n\tExit Policy:%s\n",i+1, RELAYs[i, "nickname"], RELAYs[i, "ip"], RELAYs[i, "flags"], RELAYs[i, "exit_policy"])
#}



}
