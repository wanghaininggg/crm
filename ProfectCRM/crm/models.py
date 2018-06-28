from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    '''    客户信息表    '''
    source_choices = ((0, '转介绍'),
                      (1, 'QQ群'),
                      (2, '官网'),
                      (3, '百度推广'),
                      (4, '51CTO'),
                      (5, '知乎'),
                      (6, '市场推广')
                    )
    status_choices = ((0, '未签约'),
                      (1, '已签约')
                    )
    name = models.CharField(max_length=32, blank=True, null=True, verbose_name="客户姓名")
    qq = models.CharField(max_length=64, unique=True, verbose_name="QQ")
    qq_name = models.CharField(max_length=64, blank=True, null=True, verbose_name="QQ名称")
    phone = models.CharField(max_length=64, blank=True, null=True, verbose_name="手机号")
    source = models.SmallIntegerField(choices=source_choices, verbose_name="了解方式")
    referral_from = models.CharField(max_length=64, blank=True, null=True, verbose_name="转介绍人QQ")
    consult_course = models.ForeignKey("Course", verbose_name="咨询课程", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="咨询详情")
    tags = models.ManyToManyField("Tag", blank=True, verbose_name="标签")
    consultant = models.ForeignKey("UserProfile", on_delete=models.CASCADE, verbose_name='负责人员')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')
    date = models.DateTimeField(auto_now_add=True, verbose_name='登记日期')
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name='状态')

    class Meta:
        verbose_name = '客户信息表'
        verbose_name_plural = '客户信息表' 

    def __str__(self):
        return self.qq

class Tag(models.Model):
    '''    标签表    '''
    name = models.CharField(unique=True, max_length=32, verbose_name='标签名')

    class Meta:
        verbose_name = '标签表'
        verbose_name_plural = '标签表'

    def __str__(self):
        return  self.name


class CustomerFollowUp(models.Model):
    '''    客户跟进表    '''
    intentions_choices = ((0, '2周内报名'),
                        (1, '一个月内报名'),
                        (2, '近期无报名计划'),
                        (3, '已在其他机构报名'),
                        (4, '已报名'),
                        (5, '已拉黑'),
                    )
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, verbose_name='客户')
    content = models.TextField(verbose_name="跟进内容")
    consultant = models.ForeignKey("UserProfile", on_delete=models.CASCADE, verbose_name='跟进人员')
    intention = models.SmallIntegerField(choices=intentions_choices, verbose_name='学员意向')
    date = models.DateTimeField(auto_now_add=True, verbose_name='登记时间')

    class Meta:
        verbose_name = '客户跟进表'
        verbose_name_plural = '客户跟进表'

    def __str__(self):
        return "<%s, %s>" % (self.customer.qq, self.intention)


class Course(models.Model):
    '''    课程表    '''
    name = models.CharField(max_length=64, unique=True, verbose_name="课程名称")
    price = models.PositiveSmallIntegerField(verbose_name="价格")
    period = models.PositiveSmallIntegerField(verbose_name="周期(月)")
    outline = models.TextField(verbose_name='课程大纲')

    class Meta:
        verbose_name = '课程表'
        verbose_name_plural = '课程表'

    def __str__(self):
        return self.name


class ClassList(models.Model):
    '''    班级表    '''
    class_type_choices = ((0, '面授（脱产）'),
                          (1, '面授（周末）'),
                          (2, '网络班')
                        )
    branch = models.ForeignKey("Branch", on_delete=models.CASCADE, verbose_name='校区')
    course = models.ForeignKey("Course", on_delete=models.CASCADE, verbose_name='课程')
    class_type = models.SmallIntegerField(choices=class_type_choices,max_length=32, verbose_name="班级类型")
    semester = models.PositiveSmallIntegerField(verbose_name='学期')
    teachers = models.ManyToManyField("UserProfile", verbose_name='教师')
    start_date = models.DateField(verbose_name='开班日期')
    end_date = models.DateField(blank=True, null=True, verbose_name='结业日期')

    class Meta:
        unique_together = ('branch', 'course', 'semester')
        verbose_name = '班级表'
        verbose_name_plural = '班级表'

    def __str__(self):
        return "%s, %s, %s" % (self.branch, self.course, self.semester)


class Branch(models.Model):
    '''    校区    '''
    name = models.CharField(max_length=128, unique=True, verbose_name='校区名')
    addr = models.CharField(max_length=128, verbose_name='地点')

    class Meta:
        verbose_name = '校区'
        verbose_name_plural = '校区'

    def __str__(self):
        return self.name


class CourseRecord(models.Model):
    '''    上课记录    '''
    from_class = models.ForeignKey("ClassList", verbose_name='班级', on_delete=models.CASCADE)
    day_num = models.PositiveSmallIntegerField(verbose_name='第几节')
    teacher = models.ForeignKey("UserProfile", on_delete=models.CASCADE)
    has_homework = models.BooleanField(default=True, verbose_name='是否有作业')
    homework_title = models.CharField(max_length=128, blank=True, null=True, verbose_name='作业题目')
    homework_content = models.TextField(blank=True, null=True, verbose_name='作业内容')
    outline = models.TextField(verbose_name="本节课程大纲")
    date = models.DateField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        unique_together = ("from_class", "date")
        verbose_name = '上课记录'
        verbose_name_plural = '上课记录'

    def __str__(self):
        return "%s %s" % (self.from_class, self.day_num)


class StudyRecord(models.Model):
    '''    学习记录    '''
    attendance_choices = ((0, '已签到'),
                          (1, '迟到'),
                          (2, '缺勤'),
                          (3, '早退')
                        )
    score_choices = ((100, 'A+'),
                     (90, 'A'),
                     (85, 'B+'),
                     (80, 'B'),
                     (75, 'B-'),
                     (70, 'C+'),
                     (60, 'C'),
                     (40, 'C-'),
                     (-50, 'D'),
                     (-100, 'COPY'),
                     (0, 'N/A')
                     )
    student = models.ForeignKey("Enrollment", on_delete=models.CASCADE, verbose_name='学生')
    course_record = models.ForeignKey("CourseRecord", on_delete=models.CASCADE, verbose_name='课程')
    attendance = models.SmallIntegerField(choices=attendance_choices, default=0, verbose_name='出勤情况')
    score = models.SmallIntegerField(choices=score_choices, verbose_name='成绩')
    memo = models.TextField(blank=True, null=True, verbose_name='备注')
    date = models.DateField(auto_now_add=True, verbose_name='添加日期')

    class Meta:
        unique_together = ('student', 'course_record')
        verbose_name = '学习记录'
        verbose_name_plural = '学习记录'

    def __str__(self):
        return "%s %s %s" % (self.student, self.course_record, self.score)


class Enrollment(models.Model):
    '''    报名表    '''
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, verbose_name='客户')
    enrolled_class = models.ForeignKey("ClassList", on_delete=models.CASCADE, verbose_name='班级')
    consultant = models.ForeignKey("UserProfile", on_delete=models.CASCADE, verbose_name='课程顾问')
    contract_agreed = models.BooleanField(default=False, verbose_name="学员已同意合同条款")
    contract_approved = models.BooleanField(default=False, verbose_name="合同已审核")
    date = models.DateTimeField(auto_now_add=True, verbose_name='添加日期')

    class Meta:
        unique_together = ("customer", "enrolled_class")
        verbose_name = '报名表'
        verbose_name_plural = '报名表'

    def __str__(self):
        return "%s %s" % (self.customer, self.enrolled_class)


class Payment(models.Model):
    '''    客户支付表    '''
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, verbose_name='客户')
    course = models.ForeignKey("Course", on_delete=models.CASCADE, verbose_name='所报课程')
    amount = models.PositiveIntegerField(default=500, verbose_name='金额')
    consultant = models.ForeignKey("UserProfile",on_delete=models.CASCADE, verbose_name='负责人')
    date = models.DateTimeField(auto_now_add=True, verbose_name='添加日期')

    class Meta:
        verbose_name = '客户支付表'
        verbose_name_plural = '客户支付表'

    def __str__(self):
        return "%s %s" % (self.customer, self.amount)


class UserProfile(models.Model):
    '''    工作人员    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, verbose_name='姓名')
    roles = models.ManyToManyField("Role", blank=True, verbose_name='角色')

    class Meta:
        verbose_name = '工作人员表'
        verbose_name_plural = '工作人员表'

    def __str__(self):
        return self.name


class Role(models.Model):
    '''    角色表    '''
    name = models.CharField(max_length=32, unique=True, verbose_name='角色名称')
    menu = models.ManyToManyField('Menu', blank=True, verbose_name='菜单')

    class Meta:
        verbose_name = '角色表'
        verbose_name_plural = '角色表'
        
    def __str__(self):
        return self.name

class Menu(models.Model):
    '''    菜单    '''
    name = models.CharField(max_length=32, verbose_name='菜单名')
    url_name = models.CharField(max_length=64, verbose_name='地址')

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = '菜单'

    def __str__(self):
        return self.name

# class CourseRecord(models.Model):
#     pass

