$(function () {

    $("#order_payed_list").click(function () {

        window.open("/shopapp/orderpayed/", target="_self");

    })

    $("#wait_pay_list").click(function () {

        window.open("/shopapp/ordernotpayed/", target="_self");

    })

})