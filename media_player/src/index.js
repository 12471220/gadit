function parseLrc(){
    /**
     * 解析歌词字符串,得到一个歌词对象数组
     * 单个歌词对象:
     * {time:开始时间, words:歌词内容}
     */
    splited=lrc.split('\n')
    for(let i in splited){
        let line=splited[i];
        parts=line.split(']');
        time=parts[0].substring(1);
        word=parts[1]
        console.log(time,word,'\n')

    }
    console.log(splited)

}

parseLrc()