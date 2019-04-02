from django.utils.deprecation import MiddlewareMixin
from crm import models
from django.shortcuts import redirect,reverse


class Auth(MiddlewareMixin):
    def process_request(self, request):
        # 过滤白名单url
        if request.path_info.startswith("/admin/"):
            return
        if request.path_info in [reverse("login"), reverse("reg")]:
            return
        # 检测用户是否登录
        pk = request.session.get("user_id")
        obj = models.UserProfile.objects.filter(pk=pk).first()
        # 如果存在 设置request.account里面添加该用户实例化的对象
        if obj:
            request.account = obj
        # 不存在 返回登录页面
        else:
            return redirect(reverse("login"))