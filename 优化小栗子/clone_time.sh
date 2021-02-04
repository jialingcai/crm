starttime=`date +'%Y-%m-%d %H:%M:%S'`
echo $starttime

#执行程序
git clone https://github.com/ApolloAuto/apollo.git

endtime=`date +'%Y-%m-%d %H:%M:%S'`
start_seconds=$(date --date="$starttime" +%s);
echo $start_seconds
end_seconds=$(date --date="$endtime" +%s);

echo "本次运行时间： "$((end_seconds-start_seconds))"s"
