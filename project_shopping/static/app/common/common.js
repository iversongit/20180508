function addShop(goods_id){
     alert("addShop");
     csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url:'/shopapp/addgoods/',
        type:'POST',
        data:{"goods_id":goods_id},
        dataType:'json',
        headers:{"X-CSRFToken":csrf},
        success:function (msg) {
            alert("success"+msg.c_num);
            alert(goods_id);
            $('#num_'+ goods_id).html(msg.c_num);
        },
        error:function (msg) {
            alert("传送错误");
            alert("error"+msg.c_num);
        }
    });
}

function subShop(goods_id){
    alert("subShop");
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url:'/shopapp/subgoods/',
        type:'POST',
        data:{"goods_id":goods_id},
        dataType:'json',
        headers:{'X-CSRFToken':csrf},
        success:function (msg) {
            $('#num_'+ goods_id).html(msg.c_num)
        },
        error:function (msg) {
            alert("传送错误");
        }
    });
}

function changecartselect(card_id){
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url:'/shopapp/changecartselect/',
        type:'POST',
        data:{"card_id":card_id},
        dataType:'json',
        headers:{"X-CSRFToken":csrf},
        success:function(msg){
            if(msg.is_select){
                alert("is_select true");
                s = '<span onclick="changecartselect('+ card_id +')">√</span>';
            }else{
                s = '<span onclick="changecartselect('+ card_id +')">x</span>';
            }
            $('#changeselect_'+ card_id).html(s);
        },
        error:function (msg){
            alert("传输错误")
        }
    });
}
// function cartchangeselect(cart_id) {
//     csrf = $('input[name="csrfmiddlewaretoken"]').val();
//     $.ajax({
//        url:'/shopapp/changecartselect/',
//        type:'POST',
//        data:{'cart_id':cart_id},
//        dataType:'json',
//        headers:{'X-CSRFToken':csrf},
//        success:function(msg) {
//            if(msg.is_select){}
//                 s = '<span onclick="cartchangeselect({{ cart.id }})">√</span>'
//            else{
//                 s = '<span onclick="cartchangeselect({{ cart.id }})">x</span>'
//            }
//            $('#changeselect_'+ cart_id).html(s)
//        },
//        error:function (msg) {
//
//        }
//     });
//
// }