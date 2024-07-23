function getTime(times){
    parts=times.split(":");
    period=Number(parts[0])*60+Number(parts[1]);
    return period;
}
function parseLrc(lrc){
    /**
     * 解析歌词字符串,得到一个歌词对象数组
     * 单个歌词对象:
     * {time:开始时间, words:歌词内容}
     */
    let res=[];
    splited=lrc.split('\n')
    for(let i in splited){
        let line=splited[i];
        if(line!=''){
            parts=line.split(']');
            times=parts[0].substring(1);
            word=parts[1];
            time=getTime(times);
            res.push({time,word});
        }
    }
    return res;
}
function appendToContainer(lrc_obj){
    lrc_container=document.getElementById('lrc_container');
    for(i in lrc_obj){
        list=document.createElement('li');
        list.innerText=lrc_obj[i].word;
        lrc_container.appendChild(list);
    }
}
function Play(lrc_obj){
    //设计成click 事件触发play事件 xxxx不对!!!
    audioPlayer=document.getElementById('audioPlayer');
    lrc_container=document.getElementById('lrc_container');

    audioPlayer.addEventListener('timeupdate',function(){
        let musicTime=audioPlayer.currentTime;
        // console.log('current time:', musicTime);
        for(i in lrc_obj){
            if(lrc_obj[i].time>musicTime)
                break;
        }
        // console.log(lrc_obj[i-1].time,musicTime);
        //high light the liric!!
        uls=lrc_container.children;
        // if(i-1){
        // no!!! if user slip the bar, i-1 didn't work..
        //     uls[i-2].classList.remove('active')
        // } 
        for(j in lrc_obj){
            uls[j].classList.remove('active')
        }
        uls[i-1].classList.add('active')

        if(i>8){
            let move=-30*(i-8)
            console.log(i,move)
            lrc_container.style.transform=`translate(0,${move}px)`
        }else{
            lrc_container.style.transform='translate(0,0)'
        }
        
    })
}

(function doit(){
    lrc_obj=parseLrc(LRC);
    appendToContainer(lrc_obj);
    Play(lrc_obj);
})();
