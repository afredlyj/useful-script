#! /bin/sh

# redis monitor demo on mac.

function checkServerAlive()
{
port=`grep ^port redis.conf|awk '{print $2}'`
if [[ `lsof -Pni4|grep LISTEN|grep $port|wc -l` -gt 0 ]]
then
 return 1;
else
 # server down, try to restart, and send email here
 return -1;
fi
}

function alertMemoryUsage()
{
echo $0, $1, $2
maxmemory=$1;
memoryused=$2;
alertmemory=$((1073741824 - 1024 * 1024 * 1024))
echo "alert memory :"$alertmemory
echo "maxmemory :"$maxmemory
echo "memoryused :"$memoryused
if [[ $alertmemory -le $memoryused ]]
then
echo "send email here";
elif [[ $maxmemory -le $memoryused ]]
then
echo "send email here, and then try to clear cache";
fi
echo "end of alert";
}

function checkMemoryUsage()
{
maxmemory=`grep ^maxmemory redis.conf|awk '{print $2}'|sed 's/G//'`;
maxmemoryinbytes=$(($maxmemory * 1024 * 1024 * 1024));
memoryused=`src/redis-cli info|grep used_memory:|awk -F':' '{print $2}'|sed 's///'`;
alertMemoryUsage $maxmemoryinbytes $memoryused;
}

checkServerAlive;
if [[ $? -eq 1 ]]
then
checkMemoryUsage;
fi
