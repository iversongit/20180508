import datetime
import random
import time

from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from shopper.filters import GoodsFilter
from shopper.models import Banner, Nav, MustBuy, Shop, MainProducts, UserModel, UserSession, Goods, OrderModel, \
    OrderGoodsModel, FoodTypes, CartModel
from shopper.serializers import GoodsSerializer
from django.core.urlresolvers import reverse


def home(request):
    banner = Banner.objects.all()
    nav = Nav.objects.all()
    mustbuy = MustBuy.objects.all()

    # shop_1 = Shop.objects.all()[0]
    # shop_2_3 = Shop.objects.all()[1:3]
    # shop_4_7 = Shop.objects.all()[3:7]
    # shop_8_11 = Shop.objects.all()[7:11]
    shop = Shop.objects.all()

    mainproducts = MainProducts.objects.all()

    data = {
        "banner":banner,
        "nav":nav,
        "mustbuy":mustbuy,
        # "shop_1":shop_1,
        # "shop_2_3":shop_2_3,
        # "shop_4_7":shop_4_7,
        # "shop_8_11":shop_8_11,
        "shop":shop,
        "mainproducts":mainproducts
    }
    return render(request,'home/home.html',data)

def login(request):
    if request.method == "GET":
        return render(request,'user/user_login.html')
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("login-password:",password)
        # 一次只能一个用户登录
        if UserModel.objects.filter(username=username).exists(): #　如果用户名存在
            user = UserModel.objects.get(username=username)
            if password == user.password:  # 验证密码
                s = 'abcdefghijklmnopqrstuvwxyz1234567890'
                ticket = ""
                for i in range(15):
                    # 获取随机的字符串，每次获取一个字符
                    ticket += random.choice(s)
                now_time = int(time.time()) # 1970.1.1到现在的秒数
                ticket_value = 'TK_' + ticket + str(now_time)
                # 绑定令牌到cookie里面
                response = HttpResponseRedirect("/shopapp/home")
                response.set_cookie("ticket",ticket_value,max_age=1000)
                # 存在数据库中
                expire_time = datetime.datetime.now() + datetime.timedelta(days=1)
                UserSession.objects.create(
                    session_key="ticket",
                    session_data=ticket_value,
                    expire_time= expire_time,
                    u_id=user.id
                )
                # user.ticket = ticket
                # user.save()
                return response
            else:
                return render(request,"user/user_login.html",{"errorpassword":"密码错误"})
        else:
            return render(request,"user/user_login.html",{"errorusername":"用户不存在"})




def regist(request):
    if request.method == "GET":
        return render(request,"user/user_register.html")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("regist-password:",password)
        email = request.POST.get("email")
        sex = request.POST.get("sex")
        if sex == '男':
            sex = 1
        elif sex == '女':
            sex = 0
        icon = request.FILES.get('icon')
        UserModel.objects.create(
            username=username,
            password=password,
            email=email,
            sex=sex,
            icon=icon
        )
        return HttpResponseRedirect("/shopapp/login/")

def logout(request):
    if request.method == "GET":
        response = HttpResponseRedirect("/shopapp/login/")
        ticket = request.COOKIES.get("ticket")
        response.delete_cookie("ticket")
        UserSession.objects.get(session_data=ticket).delete()
        return response

def mine(request):
    user = request.user
    data = {}
    if user and user.id:
        orders = user.ordermodel_set.all()
        wait_pay,pay =0, 0
        for order in orders:
            if order.o_status == 0:
                wait_pay += 1
            elif order.o_status == 1 or order.o_status == 2:
                pay += 1
        data = {
            "wait_pay":wait_pay,
            "pay":pay
        }
    return render(request,"mine/mine.html",data)

# def cart(request):
#     if request.user and request.method == "GET":
#         return render(request, "cart/cart_2.html")
#     else:
#         return HttpResponseRedirect("/shopapp/login/")

from rest_framework import mixins, viewsets
from rest_framework.response import Response
class GoodsEdit(mixins.ListModelMixin, # 获取所有信息
                mixins.RetrieveModelMixin, # 获取指定信息，可以通过id来查询
                mixins.UpdateModelMixin, # 修改指定信息，可以使用put/patch方法
                mixins.DestroyModelMixin, # 删除指定信息，可以使用delete方法
                mixins.CreateModelMixin, # 创建指定信息，可以使用post方法
                viewsets.GenericViewSet): # 可以调用get_queryset方法，处理queryset的结果
    # 查询所有信息
    queryset = Goods.objects.all()
    # 序列化queryset中的信息
    serializer_class = GoodsSerializer
    # 过滤
    filter_class = GoodsFilter

def market(request):
    return HttpResponseRedirect(reverse('shop:marketparam',args=('104749','0','0')))  # 大分类 详细分类 排序方式
    # type = request.GET.get("type") # 被点击的产品分类
    # detail_of_goods = Goods.objects.filter()
    # classes_of_goods = []
    # for cog in detail_of_goods:
    #     if cog.childcidname not in classes_of_goods:
    #         classes_of_goods.append(cog.childcidname)
    # data = {
    #     'classes_of_goods':classes_of_goods,
    #     'detail_of_goods':detail_of_goods,
    # }
    # return render(request,"market/market.html",data)

def marketparam(request,typeid,cid,sortid):
    if request.method == "GET":
        data = {}
        # 获取所有大类
        goods_broad_types = FoodTypes.objects.all()

        # 获取商品
        if cid == '0':
            specific_broad_type_goods = Goods.objects.filter(categoryid=typeid)
        else:
            specific_broad_type_goods = Goods.objects.filter(categoryid=typeid,childcid=cid)

        # 获取所有细类
        childtypenames = FoodTypes.objects.filter(typeid=typeid).first().childtypenames
        first_divide_of_childtypenames = childtypenames.split('#')
        finish_divide = []
        for each in first_divide_of_childtypenames:
            second_divide_of_childtypenames = each.split(':')
            finish_divide.append(second_divide_of_childtypenames)

        # 按照指定排序规则重新排显示商品
        if sortid == '0': # 不排序，正常显示  （综合排序）
            pass
        elif sortid == '1': # 销量排序
            specific_broad_type_goods = specific_broad_type_goods.order_by('-productnum')
        elif sortid == '2': # 价格降序
            specific_broad_type_goods = specific_broad_type_goods.order_by('-price')
            for ss in specific_broad_type_goods:
                print(ss.price)
        elif sortid == '3': # 价格升序
            specific_broad_type_goods = specific_broad_type_goods.order_by('price')

        data = {
            'goods_broad_types':goods_broad_types,
            'specific_broad_type_goods':specific_broad_type_goods,
            'typeid':typeid,
            'cid':cid,
            'finish_divide':finish_divide, # 每个指定大类下属的所有小类
        }
        return render(request,"market/market.html",data)



        # # 获取商品
        # if cid == '0':
        #     goods_types = Goods.objects.filter(categoryid=typeid)
        # else:
        #     goods_types = Goods.objects.filter(categoryid=typeid,childcid=cid)
        #
        # # 商品的分类
        # if sortid == '0':
        #     pass
        # elif sortid == '1':
        #     goods_types.order_by('productnum')
        # elif sortid == '2':
        #     goods_types.order_by('-price')
        # elif sortid == '3':
        #     goods_types.order_by('price')
        #
        # goods_types = Goods.objects.filter(categoryid=typeid)
        # data['foodtype'] = foodtypes
        # data['typeid'] = typeid
        # data['cid'] = cid
        # data['goods_types'] = goods_types
        #
        # # 获取分类的全部类型
        # foodtypes_childnames = FoodTypes.objects.filter(typeid=typeid).first()
        # childtypenames = foodtypes_childnames.childtypenames
        # childtypenames_list = childtypenames.split('#')
        # child_types_list = []
        # for childtypename in childtypenames_list:
        #     child_types_list.append(childtypename.split(":"))
        # data['child_types_list'] = child_types_list
        # return render(request, "market/market.html", data)



def all_order(request):
    # if request.user and request.method == "GET":
    user = request.user
    data = {}
    if user and user.id:
        orders = user.ordermodel_set.all()
        total_orders_goods = []
        for order in orders:
            ordergoods = order.ordergoodsmodel_set.all()
            one_order = []
            for ordergood in ordergoods:
                one_goods = []
                goods_name = ordergood.goods.productlongname
                goods_num = ordergood.goods_sum
                one_goods.append(goods_name)
                one_goods.append(goods_num)
                one_order.append(one_goods)
            total_orders_goods.append(one_order)

        data = {
            # 'orders': orders,
            'total_orders_goods':total_orders_goods,
        }
        return render(request, "order/order_info.html", data)
    else:
        return HttpResponseRedirect("/shopapp/login/")

def order_payed(request):
    pass

def order_not_payed(request):
    pass

def addgoods(request):
    if request.method == "POST":
        user = request.user
        data = {
            'msg': '请求成功',
            'code': '200',
        }
        if user and user.id:
            goods_id = request.POST.get("goods_id")
            # 去购物车数据表查看用户是否有购买该商品的订单
            specific_goods = CartModel.objects.filter(goods_id=goods_id).first()
            if specific_goods:
                specific_goods.c_num += 1
                data['c_num'] = specific_goods.c_num
                specific_goods.is_select = 1
                print(specific_goods.is_select,type(specific_goods.is_select))
                specific_goods.save()
            else:
                CartModel.objects.create(
                    user_id=user.id,
                    goods_id = goods_id,
                    c_num = 1
                )
                data['c_num'] = 1
        return JsonResponse(data)

    # if request.method == "POST":
    #     data = {
    #         'msg':'请求成功',
    #         'code':'200',
    #     }
    #     user = request.user
    #     if user and user.id:
    #         goods_id = request.POST.get("goods_id")
    #         # 获取购物车信息
    #         user_carts = CartModel.objects.filter(user=user,goods=goods_id).first()
    #         # 如果用户选了指定商品
    #         if user_carts:
    #             user_carts.c_num += 1
    #             user_carts.save()
    #             data['c_num'] = user_carts.c_num
    #         # 如果没选则新建
    #         else:
    #             CartModel.objects.create(
    #                 user=user, # or user_id = user.id
    #                 goods_id=goods_id,
    #                 c_num=1
    #             )
    #             data['c_num'] = 1
    #     return JsonResponse(data)

def subgoods(request):
    if request.method == "POST":
        user = request.user
        goods_id = request.POST.get("goods_id")
        data = {
            'msg':'请求成功',
            'code':'200',
        }
        if user and user.id:
            # 查看购物车数据表中是否有用户减少的指定商品项
            specific_goods = CartModel.objects.filter(goods_id=goods_id).first()
            if specific_goods:
                # 存在，且商品的数量为1，则直接删除
                if specific_goods.c_num == 1:
                    specific_goods.delete()
                    data['c_num'] = 0
                else:
                # 存在，且商品的数量不为1，则减1
                    specific_goods.c_num -= 1
                    specific_goods.is_select = 1
                    specific_goods.save()
                    data['c_num'] = specific_goods.c_num
            return JsonResponse(data)
    # if request.method == "POST":
    #     data = {
    #         'msg':'请求成功',
    #         'code':'200',
    #     }
    #     user = request.user
    #     goods_id = request.POST.get("goods_id")
    #     if user and user.id:
    #         # 查看当前商品是否已经在购物车中
    #         user_carts = CartModel.objects.filter(user=user,goods=goods_id).first()
    #         # 如果存在，则减一
    #         if user_carts:
    #             # 如果商品的数量为1，则删除
    #             if user_carts.c_num == 1:
    #                 user_carts.delete()
    #                 data['c_num'] = 0
    #             # 如果商品数量不为一，则减一
    #             else:
    #                 user_carts.c_num -= 1
    #                 user_carts.save()
    #                 data['c_num'] = user_carts.c_num
    #
    #     return JsonResponse(data)

def cart(request):
    if request.method == "GET":
        user = request.user
        # 如果有用户登录，加载购物车数据
        if user and user.id:
            carts = CartModel.objects.filter(user_id=user.id)
            return render(request,"cart/cart.html",{"carts":carts})
        else:
            # 没登陆，则返回登录页面
            return HttpResponseRedirect(reverse("shop:login"))
    # if request.method == "GET":
    #     user = request.user
    #     # 如果用户登录，加载购物车的数据
    #     if user and user.id:
    #         # 如果用户已经登录，则加载购物车的数据
    #         carts = CartModel.objects.filter(user_id=user.id)
    #         return render(request, "cart/cart_2.html", {"carts":carts})
    #     else:
    #         return HttpResponseRedirect(reverse("shop:login"))

def changecartselect(request):
    if request.method == "POST":
        card_id = request.POST.get("card_id")
        user = request.user
        data = {
            'msg':'请求成功',
            'code':'200',
        }
        if user and user.id:
            cart = CartModel.objects.filter(id=card_id).first()
            if cart.is_select == b'\x01':
                cart.is_select = 0
            else:
                cart.is_select = 1
            cart.save()
            data["is_select"] = cart.is_select
        return JsonResponse(data)
    # if request.method == "POST":
    #     user = request.user
    #     cart_id = request.POST.get("card_id")
    #     data = {
    #         'msg':'请求成功',
    #         'code':'200',
    #     }
    #     if user and user.id:
    #         cart = CartModel.objects.filter(id=cart_id).first()
    #         if cart.is_select:
    #             cart.is_select = False
    #         else:
    #             cart.is_select = True
    #         cart.save()
    #         data['is_select'] = cart.is_select
    #     return JsonResponse(data)
