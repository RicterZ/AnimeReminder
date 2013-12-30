var carousel = {
    next: function() {
        $(".active").prev().removeClass("next");
        $(".active").addClass("next");
        $(".active").next().length==0?$(".main-schedule-item")[0].className+=" active":$(".active").next().addClass("active");
        $(".next").removeClass("active");
        $(".active").removeClass("left");
        $(".active").next().length==0?$(".main-schedule-item")[0].className+=" left":$(".active").next().addClass("left");
        setTimeout(function(){
           $(".weekday").text(weekDict[$(".main-schedule-item").index($(".active"))]);
            $(".next").removeClass("next");
            $(".active").prev().length==0?$(".main-schedule-item")[6].className+=" next":$(".active").prev().addClass("next");
        }, 600);
    },
    prev: function() {
        $(".left").removeClass("left");
        $(".active").addClass("left");
        $(".next").addClass("active");
        $(".next").removeClass("next");
        setTimeout(function(){
            $(".left").removeClass("active");
            $(".weekday").text(weekDict[$(".main-schedule-item").index($(".active"))]);
            $(".active").prev().length==0?$(".main-schedule-item")[6].className+=" next":$(".active").prev().addClass("next");
        }, 600);
    }
}

weekDict = {
    0: '星期天',
    1: '星期一',
    2: '星期二',
    3: '星期三',
    4: '星期四',
    5: '星期五',
    6: '星期六',
}