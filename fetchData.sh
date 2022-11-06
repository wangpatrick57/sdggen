#!/bin/bash  
  
url='http://alitrip.oss-cn-zhangjiakou.aliyuncs.com/TraceData'

mkdir data
cd data

mkdir MSCallGraph
# mkdir Node
# mkdir MSResource
# mkdir MSRTQps

cd ../MSCallGraph
for((i=0;i<=144;i++));  
do
    fname="MSCallGraph_${i}.tar.gz"
    if [[ -f "$fname" ]]; then
	echo "using existing $fname..."
    else
	command="curl ${url}/MSCallGraph/MSCallGraph_${i}.tar.gz -o MSCallGraph_${i}.tar.gz"
	${command}
    fi
done 

: '
cd Node
command="curl ${url}/node/Node.tar.gz -o Node.tar.gz"
${command}

cd ../MSRTQps
for((i=0;i<=24;i++));  
do   
	command="curl ${url}/MSRTQps/MSRTQps_${i}.tar.gz -o MSRTQps_${i}.tar.gz"
	${command}
done 

cd ../MSResource
for((i=0;i<=11;i++));  
do   
	command="curl ${url}/MSResource/MSResource_${i}.tar.gz -o MSResource_${i}.tar.gz"
	${command}
done 
'
