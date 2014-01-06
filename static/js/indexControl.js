var indexControl = {
    _this: this,
    returnData: {},
    cookieDict: {id: '', session: '', email: ''},
    imgurl: 'http://images.movie.xunlei.com/submovie_img/',
    __init__: function() {
        this.cookie();
        var _this = this;
        if (this.cookieDict.id && this.cookieDict.session) {
            $.ajax({
                type: "POST",
                url: '/check',
                data: _this.cookieDict,
                dataType: "json",
                success: function(data){
                    if (data.status == 200) {
                        $(".reg-login").hide();
                        $(".myself").show();
                    }
                }
            })
        };
    },
    cookie: function() {
        var cookie = document.cookie.replaceAll(' ','').split(';');
        for (var i=0;i<cookie.length;i++) {
            var arr = cookie[i].split("=");
            if (arr[0]=='id')
                this.cookieDict.id = arr[1];
            if (arr[0]=='session')
                this.cookieDict.session = arr[1];
            if (arr[0]=='email')
                this.cookieDict.email = arr[1];
        }
    },
    checkData: function(data, callback) {
        callback(data.status == 200?data.data:false);
    },
    getData: function(url, callback, errortag) {
        var _this = this;
        $.ajax({
            type: "GET",
            url: url,
            dataType: "json",
            data: {hash: Math.random()},
            success: function(data){
                _this.checkData(data, callback);
            },
            error: function() {
                //_this.checkData(_this.returnData, callback);
                $(errortag).html("<p style='display:block;margin:0 auto;text-align:center'>可能是服务器抽了Q^q</p>");
            }
        })
    },
    indexHander: function(updateData) {
        var animeImageUrl = 'http://images.movie.xunlei.com/submovie_img/';
        var animeUrl = 'http://data.movie.kankan.com/movie/';
        var ul = $(".main-update-container");
        var j = 0;
        if (updateData) {
            for (var i=0;i<updateData.length;i++) {
                if (i == updateData.length / 2) 
                    j = 1;
                var m = updateData[i].animeid;
                var url = animeImageUrl+m[0]+m[1]+'/'+m+'/'+updateData[i].episode+'_1_150x85.jpg';
                $('<li class="main-update-item"><img class="update-img" src="'+url+'" onerror=this.src="./static/img/ar.jpg" /><p class="update-title"><a href="/data/'+updateData[i].animeid+'">'+updateData[i].name+'</a></p><p class="update-title">更新到 <span class="episode">'+updateData[i].episode+'</span> 集</p></li>').appendTo(ul[j]);
            };
        };
        $(".update-load").hide();
        carousel.__init__();
    },
    scheduleHandler: function(updateData) {
        var animeImageUrl = 'http://images.movie.xunlei.com/submovie_img/';
        updateData = updateData.update_list;
        if (updateData) {
            for (var i=0;i<updateData.length;i++) {
                var m = updateData[i].url.split('/')[4];
                var url = animeImageUrl+m[0]+m[1]+'/'+m+'/'+'1_1_150x85.jpg';
                $('<li class="update-schedule-item"><img class="update-img" src="'+url+'" onerror=this.src="./static/img/ar.jpg" /><p class="update-title"><a href="/data/'+updateData[i].url.substr(35)+'">'+updateData[i].name+'</a></p><p class="update-title">'+updateData[i].time+' 更新</p></li>').appendTo($(".update-schdele-container")[updateData[i].week]);
            }
        }
        $(".weekday").show();
        $(".schedule-load").hide();
    },
    loginHandler: function() {
        $(".login-error").hide();
        $(".login-ok").text("正在登录~");
        $(".login-ok").show();
        var loginUrl = '/login';
        if ($(".login")[0][0].value == "" || $(".login")[0][1].value == "") {
            $(".login-ok").hide();
            $(".login-error").text("要填上邮箱和密码0.0");
            $(".login-error").show();
            return;
        }
        $.ajax({
            type: "POST",
            url: loginUrl,
            data: {u: $(".login")[0][0].value, p: $(".login")[0][1].value},
            dataType: "json",
            success: function(data){
                if (data.status != 200) {
                    $(".login-ok").hide();
                    $(".login-error").text(data.message);
                    $(".login-error").show();
                } else {
                    $(".login-ok").text("登陆成功wwww!");
                    $(".login-ok").show();
                    location.href = '/user';
                }
            },
            error: function() {
                $(".login-error").text("登录失败QAQ!");
                $(".login-error").show();
            }
        })
    },
    regHandler: function() {
        $(".reg-error").hide();
        $(".reg-ok").text("正在注册~~");
        $(".reg-ok").show();
        var regUrl = '/reg';
        if ($(".reg")[0][0].value == "" || $(".reg")[0][1].value == "" || $(".reg")[0][2].value == "") {
            $(".reg-ok").hide();
            $(".reg-error").text("要填上邮箱和密码0.0");
            $(".reg-error").show();
            return;
        };
        if ($(".reg")[0][1].value != $(".reg")[0][2].value) {
            $(".reg-ok").hide();
            $(".reg-error").text("两次输入的密码不一样啦");
            $(".reg-error").show();
            return;
        };
        $.ajax({
            type: "POST",
            url: regUrl,
            data: {u: $(".reg")[0][0].value, p: $(".reg")[0][1].value},
            dataType: "json",
            success: function(data){
                if (data.status != 200) {
                    $(".reg-ok").hide();
                    $(".reg-error").text(data.message);
                    $(".reg-error").show();
                } else {
                    $(".reg-ok").text("注册成功wwww!");
                    $(".reg-ok").show();
                    location.href = '/user';
                }
            },
            error: function() {
                $(".reg-error").text("发生了很奇怪的事情");
                $(".reg-error").show();
            }
        })
    },
    myHandlerCheck: function() {
        var _this = this;
        this.cookie();
        $.ajax({
            type: "POST",
            url: '/check',
            data: _this.cookieDict,
            dataType: "json",
            success: function(data){
                console.log(data.status);
                if (data.status != 200) {
                    location.href = '/';
                } else {
                    _this.getUserData(function(data){
                        console.log(data);
                        if (localStorage.getItem("email") != data.data.email) {
                            console.log('e');
                            localStorage.setItem("email", data.data.email);
                        };
                        if (localStorage.getItem("unread") != data.data.unread) {
                            console.log('u');
                            localStorage.setItem("unread", data.data.unread);
                        };
                        if (localStorage.getItem("subscription") != JSON.stringify(data.data.subscription)) {
                            console.log('s');
                            localStorage.setItem("subscription", JSON.stringify(data.data.subscription));
                        };
                        _this.userSetData();
                        $(".my-load").hide();
                    });
                }
            },
            error: function() {
                location.href = '/';
            }
        })
    },
    getUserData: function(callback, needSet){
        $.ajax({
            type: "GET",
            url: '/my',
            data: {hash: Math.random()},
            dataType: "json",
            async: true,
            success: function(data){
                if (data.status != 200) {
                    $(".subscript-container").text(data.message);
                } else {
                    if (needSet) {
                        localStorage.setItem("subscription", JSON.stringify(data.data.subscription));
                        localStorage.setItem("email", data.data.email);
                        localStorage.setItem("unread", data.data.unread);
                    };
                    callback(data);
                }
            },
            error: function() {
                $(".subscript-container").text("可能是服务器抽了Q^q");
            }
        });
    },
    myHandler: function() {
        if (localStorage.getItem("subscription")==null || localStorage.getItem("subscription")==undefined) {
            this.getUserData(this.userSetData, true);
        } else {
            this.userSetData();
        }
    },
    userSetData: function(){
        $(".subscript-container").html('<img class="load my-load" src="./static/img/01.gif" />');
        var _this = this,
            emailDic = {0: 'close', 1: 'open'},
            email = LittleUrl.decode(_this.cookieDict.email),
            overdic = function(status, read, aid) {
                return status==1?'<span class="anime-info'+read+'" data-animeid="'+aid+'">已完结</span>':'<span class="anime-info'+read+'" data-animeid="'+aid+'">更新中</span>'};
        $(".my-email").text(email);
        eval('var subscription = ' + localStorage.getItem("subscription"));
        $(".unread-num").text(localStorage.getItem("unread"));
        $(".button-option").addClass(emailDic[localStorage.getItem("email")]);
        for (var i=0;i<subscription.length;i++) {
            var url = subscription[i].id.toString().substring(0,2) + '/' + subscription[i].id + '/' + subscription[i].episode + '_1_150x85.jpg';
            var read = subscription[i].isread==1?" unread-sub":" read-sub";
            var info = overdic(subscription[i].isover, read, subscription[i].id);
            $('<div class="anime-item"><a class="icon del-anime icon-del" href="##" data-animeid="'+subscription[i].id+'">╳</a><p class="anime-title">'+info+'<a class="anime-title-a" href="/data/'+subscription[i].id+'">'+subscription[i].name+'</a></p><img class="anime-img" onerror=this.src="./static/img/ar.jpg" src="'+_this.imgurl+url+'" /><p class="anime-epi">更新到 '+subscription[i].episode+' 集</p><p class="watch">已经看到 <span class="watchepi">'+subscription[i].watch+'</span><input data-animeid="'+subscription[i].id+'" value="'+subscription[i].watch+'" type="text" class="anime-epi-input hidden" /> 集</p></div>').appendTo(".subscript-container");
        };
        $(".watchepi").click(function(){
            $(this).addClass('hidden');
            $(this).next().removeClass('hidden');
        });
        $(".anime-epi-input").blur(function(){
            $(this).addClass('hidden');
            $(this).prev().removeClass('hidden');
            if (_this.epiEdit(this.attributes['data-animeid'].nodeValue, $(this)[0].value)) {
                $(this).prev().text($(this)[0].value);
            } else {
                $(this)[0].value=$(this).prev().text();
            }
        });
        $(".anime-info").click(function(){
        if (this.className == "anime-info unread-sub") {
            if (_this.highlight(this.attributes['data-animeid'].nodeValue, 'del')) {
                    $(this).addClass("read-sub");
                    $(this).removeClass("unread-sub");
                    $(".unread-num").text(parseInt($(".unread-num").text())-1);
                    localStorage.setItem("unread", parseInt($(".unread-num").text()));
                }
            } else {
                if (_this.highlight(this.attributes['data-animeid'].nodeValue, 'add')) {
                    $(this).addClass("unread-sub");
                    $(this).removeClass("read-sub");
                    $(".unread-num").text(parseInt($(".unread-num").text())+1);
                    localStorage.setItem("unread", parseInt($(".unread-num").text()));
                }
            }
        });
        $(".del-anime").click(function(){
            if (_this.del(this.attributes['data-animeid'].nodeValue)) {
                localStorage.removeItem("subscription");
                $(this).parent().hide();
            }
        });
    },
    emailReminderSet: function(status) {
        var bool;
        $.ajax({
            type: "GET",
            url: '/email_reminder_set',
            data: {enable: status, hash: Math.random()},
            dataType: "json",
            async: false,
            success: function(data){
                bool = data.status==200?true:false;
            },
            error: function() {
                bool = false;
            }
        });
        return bool;
    },
    epiEdit: function(aid, epi) {
        var bool;
        $.ajax({
            type: "GET",
            url: '/epiedit',
            data: {aid: aid, epi: epi, hash: Math.random()},
            dataType: "json",
            async: false,
            success: function(data){
                bool = data.status==200?true:false;
            },
            error: function() {
                bool = false;
            }
        });
        return bool;
    },
    highlight: function(aid, method) {
        var bool;
        $.ajax({
            type: "GET",
            url: '/highlight',
            data: {aid: aid, method: method, hash: Math.random()},
            dataType: "json",
            async: false,
            success: function(data){
                bool = data.status==200?true:false;
            },
            error: function() {
                bool = false;
            }
        });
        return bool;
    },
    search: function(keyword){
        var _this = this;
        $(".subscript-container").html('<img class="load search-load" src="./static/img/01.gif" />');
        $.ajax({
            type: "POST",
            url: '/search',
            data: {keyword: keyword, hash: Math.random()},
            dataType: "json",
            async: true,
            success: function(data){
                if (data.status != 200) {
                    $(".subscript-container").text(data.message);
                } else {
                    var data = data.data;
                    //console.log(data);
                    for (var i=0;i<data.length;i++) {
                        var url = data[i].id.toString().substring(0,2) + '/' + data[i].id + '/1_1_150x85.jpg';
                        var read = data[i].isread==1?" unread-sub":" read-sub";
                        $(".search-load").hide();
                        $('<div class="anime-item"><a class="icon add-anime icon-add" href="##" data-animeid="'+data[i].id+'">+</a><p class="anime-title"><a class="anime-title-a" href="/data/'+data[i].id+'">'+data[i].name+'</a></p><img class="anime-img" onerror=this.src="./static/img/ar.jpg" src="'+_this.imgurl+url+'" /></div>').appendTo(".subscript-container");
                    };
                    $(".add-anime").click(function(){
                        if (_this.add(this.attributes['data-animeid'].nodeValue))
                            $(this).parent().hide();
                    });
                }
            },
            error: function() {
                bool = false;
            }
        });
    },
    add: function(aid){
        var bool;
        $.ajax({
            type: "GET",
            url: '/add_anime',
            data: {aid: aid, hash: Math.random()},
            dataType: "json",
            async: false,
            success: function(data){
                bool = data.status==200?true:false;
            },
            error: function(){
                bool = false;
            }
        });
        return bool;
    },
    del: function(aid){
        var bool;
        $.ajax({
            type: "GET",
            url: '/del_anime',
            data: {aid: aid, hash: Math.random()},
            dataType: "json",
            async: false,
            success: function(data){
                bool = data.status==200?true:false;
            },
            error: function(){
                bool = false;
            }
        });
        return bool;
    }
}
