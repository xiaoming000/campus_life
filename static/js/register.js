$(function () {
    var flag_username = 0;
    var flag_email = 0;
    var flag_password1 = 0;
    var flag_password2 = 0;
    // 密码位数必须大于8
   $("#registerpwd1").blur(function () {
        if($(this).val() == ""){
            $("#error").css('display', 'block').text("请输入密码！");
            flag_password1 = 0;
        }else{
            var reg = /^[0-9]+$/;
            if(!reg.test($(this).val())) {
                len = $(this).val().length;
                if(len < 8){
                    $("#error").css('display', 'block').text("请输入至少8位的密码！");
                    flag_password1 = 0;
                }else{
                    $("#error").css('display', 'none');
                    flag_password1 = 1;
            }
            }else{
               $("#error").css('display', 'block').text("请不要输入纯数字的密码！");
               flag_password1 = 0;
            }
        }
   });
    // 确认密码必须相等
   $("#registerpwd2").blur(function () {
        if($(this).val() == ""){
            $("#error").css('display', 'block').text("请输入密码！");
            flag_password2 = 0;
        }else {
            text1 = $("#registerpwd1").val();
            text2 = $(this).val();
            if (text1 != text2) {
                $("#error").css('display', 'block').text("2次输入的密码不一样！");
                flag_password2 = 0;
            } else {
                $("#error").css('display', 'none');
                flag_password2 = 1;
            }
        }
   });
   // 用户名验证！
    $("#registername").blur(function () {
        if($(this).val() == ""){
            $("#error").css('display', 'block').text("请输入用户名！")
            flag_username = 0;
        }else{
            $.post("/userajax/",
                {
                  username: $("#registername").val()
                },
                function (data) {
                    if(data.repeat == 1){
                        $("#error").css('display', 'block').text("你输入的用户名已经存在！");
                        flag_username = 0;
                    }else {
                        $("#error").css('display', 'none');
                        flag_username = 1;
                    }
                }
            );
        }
    });
    // 邮箱验证
    $("#registeremail").blur(function(){
        if($(this).val() == ""){
            $("#error").css('display', 'block').text("请输入你的邮箱！！");
            flag_email = 0;
        }else{
           var reg = /^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/;
           if(!reg.test($(this).val())) {
               $("#error").css('display', 'block').text("你输入的邮箱格式不正确！");
               flag_email = 0;
           }else{
               $("#error").css('display', 'none');
               flag_email = 1;
           }
        }
    });
    //注册提交
//     flag = 0;
//     if(flag_username == 0){
//         $(this).attr('data-content', "你的用户名不合法，请检查后提交！");
//         $("[data-toggle='popover']").popover({trigger: 'hover'});
//     }else if(flag_email == 0){
//         $(this).attr('data-content', "你的邮箱！不合法，请检查后提交！");
//         $("[data-toggle='popover']").popover({trigger: 'hover'});
//     }else if(flag_password1 == 0){
//         $(this).attr('data-content', "你的密码不合法，请检查后提交！");
//         $("[data-toggle='popover']").popover({trigger: 'hover'});
//     }
// else
    $("#register_sub").click(function(e){
        e.preventDefault();
        if(flag_username == 0){
            $(this).attr('data-content', "你的用户名不合法，请检查后提交！");
            $("[data-toggle='popover']").popover();
        }else if(flag_email == 0){
            $(this).attr('data-content', "你的邮箱不合法，请检查后提交！");
            $("[data-toggle='popover']").popover();
        }else if(flag_password1 == 0){
            $(this).attr('data-content', "你的密码不合法，请检查后提交！");
            $("[data-toggle='popover']").popover();
        }else if(flag_password2 == 0) {
            $(this).attr('data-content', "你的确认密码不合法，请检查后提交！");
            $("[data-toggle='popover']").popover();
        }else{
            $("#register_form").submit();
        }
    });


    // 注册格式提示
    $(".popover-options a").popover({html : true });

    // 关闭注册框框是隐藏提示弹出框
    $("#register").on('hide.bs.modal',
    function() {
        $(".popover-options a").popover('hide');
    })

    // 添加标签
    $(".tag_add").click(function(){
        $(this).before('<div class="tag pull-left" style="padding-left: 5px;"><input  autofocus type="text" size="1"></div>');
        var ipt = $(this).prev().children("input");
        // alert(ipt);
        ipt.bind('input propertychange',function(){
            var obj = $(this);
            var text_length = obj.val().length;  //获取当前长度
            var width = parseInt(text_length)*16; //该12是改变前的宽度除以当前字符串的长度，算出每个字符的长度
            if(width>10){
                obj.css({
                    'width': width+'px'
                });
            }
        });
        ipt.blur(function () {
            ipt.before('<span>'+ ipt.val() +'</span>');
            ipt.remove();
            var len = $(".tag").length;
            var str = "";
            for(i=0; i<len; i++){
                if(i == len-1){
                    str += $(".tag").eq(i).children("span").text();
                }else {
                    str += $(".tag").eq(i).children("span").text() + ",";
                }
            }
            $("#tags_input").val(str);
        });
    });
});
// $(function () {
// 	$("[data-toggle='popover']").popover();
// });