from django.conf.urls import url
from shopper import views
from rest_framework.routers import SimpleRouter
router = SimpleRouter() # 定义一个路由
router.register(r'goods',views.GoodsEdit)

urlpatterns = [
    url(r'^home/',views.home,name="home"),
    url(r'^login/',views.login,name="login"),
    url(r'^regist/',views.regist,name="regist"),
    url(r'^logout/',views.logout,name="logout"),
    url(r'^mine/',views.mine,name="mine"),
    url(r'^cart/',views.cart,name="cart"),
    # 闪购
    url(r'^market/$',views.market,name="market"), # 不加$将无法匹配到marketparam方法
    url(r'^market/(\d+)/(\d+)/(\d+)',views.marketparam,name="marketparam"),

    url(r'^allorder/',views.all_order,name='allorder'),
    url(r'^orderpayed/',views.order_payed,name='orderpayed'),
    url(r'^ordernotpayed/',views.order_not_payed,name='ordernotpayed'),

    # 添加购物车商品
    url(r'^addgoods/',views.addgoods,name="addgoods"),
    # 减少购物车商品
    url(r'^subgoods/',views.subgoods,name="subgoods"),

    # 购物车
    url(r'^cart/',views.cart,name="cart"),
    # 修改购物车商品的选项
    url(r'^changecartselect/',views.changecartselect,name="changecartselect")
]

urlpatterns += router.urls # 将路径与对应的类都添加到urlpatterns中