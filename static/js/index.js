$(function () {

    // 关闭按钮
    $('.close').click(function () {
        $(this).parent('div').css('display', 'none');
    });


    //***************************base.html********************************
    $('#myCarousel').carousel({
        interval: 3000
    })

    $(".push").click(function () {
        alert("你还未登入，不能发表文章！")
    });

    $('#verifycode').css('cursor','pointer').click(function() {
        $(this).attr('src',$(this).attr('src')+1)
    });


    // detail.html
    // 评论回复
    $(".comment_body").mousemove(function () {
        $(this).find(".reply_comment").css('display', 'inline');
        $(this).find(".reply_comment_del").css('display', 'inline');
    });
    // 回复
    $(".reply").mousemove(function () {
        $(this).find(".reply_r_del").css('display', 'inline');
        $(this).find(".reply_r").css('display', 'inline');
    });
    // 评论回复、删除关闭
    $(".comment_body").mouseout(function () {
        $(this).find('.reply_comment').css('display', 'none');
        $(this).find('.reply_comment_del').css('display', 'none');
    });
    // 回复、删除按钮关闭
    $(".reply").mouseout(function () {
        $(this).find(".reply_r").css('display', 'none');
        $(this).find(".reply_r_del").css('display', 'none');
    });

    // 评论回复表单弹出
    $(".reply_comment").click(function () {
        $(this).parent().next(".reply_form").css('display', 'block');
        $(this).parents("li").siblings().find(".reply_form").css('display', 'none');
    });
    // 回复 回复表单
    $(".reply_r").click(function () {
        $(this).parent().next(".r_r_form").css('display', 'block');
        $(this).parents(".reply_li").siblings().find(".r_r_form").css('display', 'none');
        $(this).parents(".comment-item").siblings().find(".r_r_form").css('display', 'none');
    });


    // 评论表单关闭
    $(".reply_form_close").click(function () {
        $(this).parents(".reply_form").css('display', 'none');
    });
    // 回复表单关闭
    $(".r_r_form_close").click(function () {
        $(this).parents(".r_r_form").css('display', 'none');
    });


    // 删除
    // 新闻评论删除
    $(".news .reply_comment_del").click(function () {
        if(confirm("确定要删除吗？")){
            $.post('/news/del_comment/',
                {
                    csrfmiddlewaretoken: $(this).attr("data-csrf"),
                    comment_id: $(this).attr("data-comment-id")
                },
                function (data) {
                    // console.log(data);
                    alert(data)
                }
            );
        }
    });
    // 新闻回复删除
    $(".news .reply_r_del").click(function () {
        if(confirm("确定要删除吗？")){
            $.post('/news/del_reply/',
                {
                    csrfmiddlewaretoken: $(this).attr("data-csrf"),
                    reply_id: $(this).attr("data-reply-id")
                },
                function (data) {
                    // console.log(data);
                    alert(data)
                }
            );
        }
    });

    // 文章评论删除
    $(".post .reply_comment_del").click(function () {
        if(confirm("确定要删除吗？")){
            $.post('/post/del_comment/',
                {
                    csrfmiddlewaretoken: $(this).attr("data-csrf"),
                    comment_id: $(this).attr("data-comment-id")
                },
                function (data) {
                    // console.log(data);
                    alert(data)
                }
            );
        }
    });
    // 文章回复删除
    $(".post .reply_r_del").click(function () {
        if(confirm("确定要删除吗？")){
            $.post('/post/del_reply/',
                {
                    csrfmiddlewaretoken: $(this).attr("data-csrf"),
                    reply_id: $(this).attr("data-reply-id")
                },
                function (data) {
                    // console.log(data);
                    alert(data)
                }
            );
        }
    });


});
