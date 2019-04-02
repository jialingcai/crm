from django.shortcuts import render,redirect,HttpResponse,reverse
from crm import models
from crm.forms import RegForm,UserForm,ConsultForm,EnrollmentForm
import hashlib
from django.views import View
from django.db.models import Q
from crm.utils.pagination import Pagination
from crm.utils.urls import reverse_url
# Create your views here.


def index(request):
    return HttpResponse("this is index")


def login(request):
    err_msg = ''
    if request.method == "POST":
        user = request.POST.get("user")  #前端中获取用户名
        pwd = request.POST.get("pwd")  #获取前端中密码
        # 加密
        md5 = hashlib.md5()
        md5.update(pwd.encode("utf8"))
        pwd = md5.hexdigest()
        user_obj = models.UserProfile.objects.filter(username=user, password=pwd,is_active=True).first()    #数据库中作比较
        if user_obj:
            request.session["user_id"] = user_obj.pk
            return redirect('/index/')
        err_msg = "用户名或者密码错误"
    return render(request, 'login.html', {"err_msg": err_msg})


def logout(request):
    request.session.flush()
    return redirect(reverse("login"))


def reg(request):
    form_obj = RegForm()
    if request.method == "POST":
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            # form_obj.cleaned_data.pop("re_password")#数据库中没有re_password字段,踢除
            # models.UserProfile.objects.create(**form_obj.cleaned_data)  # 打散输入
            form_obj.save()             #直接在数据库中保存
            return redirect("/login/")
    return render(request, "reg.html", {"form_obj": form_obj})


# def customer(request):
#     # 公户
#     if request.path_info == reverse("customer"):
#         all_customer = models.Customer.objects.filter(consultant__isnull=True)
#     else:
#         all_customer = models.Customer.objects.filter(consultant=request.account)
#     return render(request, "customer.html", {"all_customer": all_customer})


class Customer(View):
    def get(self, request):
        q = self.search(['qq', 'name'])
        if request.path_info == reverse("customer"):
            all_customer = models.Customer.objects.filter(q, consultant__isnull=True)
        else:
            all_customer = models.Customer.objects.filter(q, consultant=request.account)
        pager = Pagination(request.GET.get("page", "1"), all_customer.count(), request.GET.copy(), 2)
        return render(request,"customer.html", {"all_customer": all_customer[pager.start:pager.end], "page_html": pager.page_html})

    def post(self, request):
        action = request.POST.get("action")

        if not hasattr(self, action):
            return HttpResponse("非法输入")
        else:
            getattr(self, action)()
            return self.get(request)

    def private(self):
        # 共转私
        ids = self.request.POST.getlist("id")
        models.Customer.objects.filter(id__in=ids).update(consultant=self.request.account)

    def public(self):
        #私转公
        ids = self.request.POST.getlist("id")
        models.Customer.objects.filter(id__in=ids).update(consultant=None)

    def search(self, query_list):
        query = self.request.GET.get("query", '')
        q = Q()
        q.connector = 'OR'

        for i in query_list:
            q.children.append(Q(('{}__contains'.format(i), query)))
        return q



user_list = [{'name':'wang{}'.format(i),'pwd':'密码{}'.format(i)} for i in range(1,102)]


def page(request):
    try:
        now_page = int(request.GET.get("page"))
    except Exception as e:
        now_page =1
    # 总数据
    all_count = len(user_list)
    # 每一页数据
    page_count = 10
    #总页数
    page_num, more = divmod(all_count, page_count)
    if more:
        page_num += 1
    start = (now_page-1)*page_count
    end = now_page*page_count
    #最大显示数
    max_page = 7
    helf_page = max_page//2
    if page_num < max_page:
        page_start = 1
        page_end = page_num
    else:
        if now_page <= helf_page:
            page_start = 1
            page_end = max_page
        elif now_page > page_num-helf_page:
            page_start = page_num-max_page+1
            page_end = page_num
        else:
            page_start = now_page-helf_page
            page_end = now_page+helf_page

    return render(request, 'page.html', {"user_list": user_list[start:end], "page_num": range(page_start, page_end+1),
                                         "now_page":now_page,"page_after":now_page-1,
                                         "page_before":now_page+1,
                                         "paged":page_num+1})


def page2(request):
    pager = Pagination(request.GET.get('page', '1'), len(user_list), per_num=10)

    return render(request, 'page2.html',
                  {"all_user": user_list[pager.start:pager.end],
                   'page_html': pager.page_html
                   }, )


def customer_add(request):
    user_obj = UserForm()
    if request.method == "POST":
        user_obj = UserForm(request.POST)
        if user_obj.is_valid():
            user_obj.save()
            return redirect(reverse("customer"))
    return render(request, "customer_add.html", {"user_obj": user_obj})


def customer_edit(request,edit_id):
    customer_obj = models.Customer.objects.filter(pk=edit_id).first()
    user_obj = UserForm(instance=customer_obj)
    if request.method == "POST":
        user_obj = UserForm(request.POST, instance=customer_obj)
        if user_obj.is_valid():
            user_obj.save()
            return redirect(reverse("customer"))
    return render(request, "customer_edit.html", {"user_obj": user_obj})


def customer_change(request,edit_id=None):
    obj = models.Customer.objects.filter(pk=edit_id).first()
    user_obj = UserForm(instance=obj)
    if request.method == "POST":
        user_obj = UserForm(request.POST,instance=obj)
        if user_obj.is_valid():
            user_obj.save()
            return redirect(reverse_url(request, "customer"))
    return render(request, "customer_change.html", {"user_obj": user_obj,"edit_id":edit_id})


class Consult(View):
    def get(self,request,customer_id):
        if customer_id == "0":
            consult_obj = models.ConsultRecord.objects.all()
        else:
            consult_obj = models.ConsultRecord.objects.filter(customer_id=customer_id)
        return render(request, "consult.html",{"consult_obj":consult_obj})


def consult_add(request):
    # 实例化一个包含当前销售的跟进记录
    con_obj = models.ConsultRecord(consultant=request.account)
    consult_obj = ConsultForm(instance=con_obj)
    # 处理post请求
    if request.method == "POST":
        # 实例化一个带提交参数的form
        consult_obj = ConsultForm(request.POST, instance=con_obj)
        # 数据校验
        if consult_obj.is_valid():
            consult_obj.save()
            return redirect(reverse("consult",args="0"))

    return render(request, "consult_add.html", {"consult_obj": consult_obj})


def consult_edit(request, edit_id):
    obj = models.ConsultRecord.objects.filter(pk=edit_id).first()
    consult_obj = ConsultForm(instance=obj)
    if request.method == "POST":
        consult_obj = ConsultForm(request.POST, instance=obj)
        if consult_obj.is_valid():
            consult_obj.save()
            return redirect(reverse("consult",args="0"))
    return render(request, "consult_edit.html", {"consult_obj": consult_obj})


class Enroll(View):
    def get(self, request, customer_id):
        if customer_id == "0":
            enrollment_obj = models.Enrollment.objects.all()
        else:
            enrollment_obj = models.Enrollment.objects.filter(customer_id=customer_id)

        return render(request, "enrollment.html", {"enrollment_obj":enrollment_obj})


def enrollment_add(request, customer_id):
    obj = models.Enrollment(customer_id=customer_id)
    enrollment_obj = EnrollmentForm(instance=obj)
    if request.method == "POST":
        enrollment_obj = EnrollmentForm(request.POST, instance=obj)
        if enrollment_obj.is_valid():
            enrollment_obj.save()
            return redirect(reverse("enrollment",args='0'))

    return render(request, "enrollment_change.html", {"enrollment_obj": enrollment_obj})
