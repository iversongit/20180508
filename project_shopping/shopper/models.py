from django.db import models

# Create your models here.
# 全局搜索 ctrl + shift + R
class Base(models.Model):
    img = models.CharField(max_length=200) # 图片,没有管理后台插入图片，直接在数据库中导入
    name = models.CharField(max_length=200) # 图片名称
    trackid = models.CharField(max_length=16) # 通用id
    class Meta:
        abstract = True # 父类为抽象类，便于子类继承

class Banner(Base):
    # 轮播banner
    class Meta:
        db_table = "axf_banner"

class Nav(Base):
    # 导航
    class Meta:
        db_table = "axf_nav"

class MustBuy(Base):
    # 必购
    class Meta:
        db_table = "axf_mustbuy"

class Shop(Base):
    # 商铺
    class Meta:
        db_table = "axf_shop"

class MainProducts(Base):
    # 主要商品展示
    categoryid = models.CharField(max_length=16) # 分类id
    brandname = models.CharField(max_length=100) # 分类名称
    img1 = models.CharField(max_length=200)  # 产品图片
    childcid1 = models.CharField(max_length=16) # 子类id
    productid1 = models.CharField(max_length=16) # 产品id
    longname1 = models.CharField(max_length=100) # 产品名称
    price1 = models.FloatField(default=0) # 优惠价格
    marketprice1 = models.FloatField(default=1) # 原始价格
    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=16)
    productid2 = models.CharField(max_length=16)
    longname2 = models.CharField(max_length=100)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=1)
    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=16)
    productid3 = models.CharField(max_length=16)
    longname3 = models.CharField(max_length=100)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=1)

    class Meta:
        db_table = "axf_mainproducts"

class FoodTypes(models.Model):
    # 闪购 -- 左侧类型表
    typeid = models.CharField(max_length=15) #食品类型id,不用系统自带的自增id
    typename = models.CharField(max_length=100) # 食品类型名称
    childtypenames = models.CharField(max_length=200) # 食品子类名称
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = "axf_foodtypes"

class Goods(models.Model):
    productid = models.CharField(max_length=16) # 产品编号
    productimg = models.CharField(max_length=200) # 产品图片
    productname = models.CharField(max_length=100) # 产品名称
    productlongname = models.CharField(max_length=200) # 产品规格
    isxf = models.IntegerField(default=1)
    pmdesc = models.CharField(max_length=100)
    specifics = models.CharField(max_length=100) # 详细规格
    price = models.FloatField(default=0)  # 折后价格
    marketprice = models.FloatField(default=1)  # 原价
    categoryid = models.CharField(max_length=16) # 分类id
    childcid = models.CharField(max_length=16) # 子分类id
    childcidname = models.CharField(max_length=100) # 子分类的名称
    dealerid = models.CharField(max_length=16)
    storenums = models.IntegerField(default=1)
    productnum = models.IntegerField(default=1) # 按照销量排序

    class Meta:
        db_table = "axf_goods"

class UserModel(models.Model):
    # 用户信息
    username = models.CharField(max_length=32,unique=True) # 姓名
    password = models.CharField(max_length=256) # 密码
    email = models.CharField(max_length=64,unique=True) # 邮箱
    sex = models.BooleanField(default=False) # 性别 False代表女
    icon = models.ImageField(upload_to='icons') # 头像
    is_delete = models.BooleanField(default=False) # 是否删除
    class Meta:
        db_table = "axf_user"

class CartModel(models.Model):
    # 购物车模型
    user = models.ForeignKey(UserModel) # 关联用户
    goods = models.ForeignKey(Goods) # 关联商品
    c_num = models.IntegerField(default=1) # 商品个数
    is_select = models.BooleanField(default=True) # 是否选择

    class Meta:
        db_table = "axf_cart"

class OrderModel(models.Model):
    # 订单模型
    user = models.ForeignKey(UserModel) # 关联用户
    o_num = models.CharField(max_length=64) # 数量
    # 0 代表已下单，但是未付款 1 已付款未发货 2 已付款，已发货
    o_status = models.IntegerField(default=0) # 订单状态
    o_create = models.DateTimeField(auto_now_add=True) # 创建时间

    class Meta:
        db_table = "axf_order"

class OrderGoodsModel(models.Model):
    # 订单和商品之间的关联模型
    goods = models.ForeignKey(Goods) # 关联的商品
    order = models.ForeignKey(OrderModel) # 关联的订单
    goods_sum = models.IntegerField(default=1) # 商品的个数

    class Meta:
        db_table = "axf_order_goods"

class UserSession(models.Model):
    # 定义令牌
    session_key = models.CharField(max_length=50)
    session_data = models.CharField(max_length=50)
    expire_time = models.DateTimeField()
    u = models.ForeignKey(UserModel) # 关联用户

    class Meta:
        db_table = "axf_session"