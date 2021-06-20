from django.db import models

# Create your models here.
class PartnerDetail(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    logo = models.TextField()
    whatsapp_group = models.CharField(max_length=300,null=True,blank=True)

class PartnerCourses(models.Model):
    partner = models.ForeignKey(PartnerDetail,on_delete=models.PROTECT) 
    title = models.CharField(max_length=300)
    description = models.TextField()
    tags = models.CharField(max_length=300)
    course_link = models.CharField(max_length=300,blank=True,null=True)
    group_name = models.CharField(max_length=300,blank=True,null=True)
    group_link = models.CharField(max_length=300,blank=True,null=True)
    total_like = models.IntegerField(default=0,blank=True,null=True)
    price = models.CharField(max_length=20)
    offer_price = models.CharField(max_length=20)
    discount = models.CharField(max_length=20)
    isByEdby = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    entry_time = models.DateTimeField(auto_now=False,auto_now_add=True)
    
    def to_dict(self):
        info_dict = {}
        for key in ["id",'title','description',
        'course_link','group_name','group_link',
        'price','offer_price','discount',
        'tags','total_like','isByEdby','entry_time']:
            info_dict[key] = self.__dict__[key].__str__()
        info_dict['partner_name'] = self.partner.name
        info_dict['partner_description'] = self.partner.description
        info_dict['partner_logo'] = self.partner.logo
        info_dict['partner_group'] = self.partner.whatsapp_group
        return info_dict

class EdbyFreeCourseContent(models.Model):
    course = models.ForeignKey(PartnerCourses,on_delete=models.CASCADE)
    num = models.IntegerField()
    link = models.CharField(max_length=300)
    description = models.TextField()