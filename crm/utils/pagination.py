class Pagination:
    def __init__(self, page, all_count,params, per_num=15, max_show=7):
        try:
            page = int(page)
            if page < 0:
                page = 1
        except Exception as e:
            self.page = 1
        self.params=params
        # 获取当前页码
        self.page = page
        # 总的数据数量
        self.all_count = all_count
        # 每一页数据条数
        self.per_num = per_num
        # 最多显示页码
        self.max_show = max_show
        # 总页数
        self.page_num, more = divmod(all_count, per_num)
        if more:
            self.page_num += 1
        # 页码相关的设置
        half_show = max_show // 2
        # 判断页码
        # 总页码小于显示页码
        if self.page_num < max_show:
            self.start_num = 1
            self.end_num = self.page_num
        else:
            # 处理左边的极限
            if page <= half_show:
                self.start_num = 1
                self.end_num = max_show
            # 处理右边极限
            elif page + half_show > self.page_num:
                self.start_num = self.page_num - max_show + 1
                self.end_num = self.page_num
            else:
                self.start_num = page - half_show
                self.end_num = page + half_show

    @property
    def start(self):
        return self.per_num * (self.page-1)

    @property
    def end(self):
        return self.per_num * self.page

    @property
    def page_html(self):
        page_list = []
        if self.page == 1:
            page_list.append('<li class="disabled"><a> << </a></li> ')
        else:
            self.params['page'] = self.page - 1
            page_list.append('<li><a href="?{}"> << </a></li>'.format(self.params.urlencode()))
        for i in range(self.start_num, self.end_num + 1):
            self.params['page'] = i
            if i == self.page:
                page_list.append(
                    '<li class="active"><a href="?{0}">{1}</a></li>'.format(self.params.urlencode(), i))
            else:
                page_list.append(
                    '<li><a href="?{0}">{1}</a></li>'.format(self.params.urlencode(),i))
        if self.page == self.page_num:
            page_list.append('<li class="disabled"><a> >> </a></li> ')
        else:
            self.params['page'] = self.page + 1
            page_list.append(
                '<li><a href="?{}"> >> </a></li>'.format(self.params.urlencode()))
        return ''.join(page_list)
