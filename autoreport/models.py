from ast import literal_eval
from django.db import models

class Admin(models.Model):
    name = models.CharField(max_length=100)
    line_id = models.CharField(max_length=100)
    handle_squad_id = models.IntegerField()
    
    def __str__(self):
        return self.name

class Squad(models.Model):
    squad_id = models.IntegerField()
    member_num = models.IntegerField(blank=True)
    member_id = models.CharField(max_length=200, blank=True)
    line_group_id = models.CharField(max_length=100, blank=True)
    line_group_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return "第" + str(self.squad_id) + "班"

class Report(models.Model):
    '''
    squad_id: 第幾班
    member_report_status: dict，{學號:報告內容}
    report_title: 報告的前幾句抬頭
    report_info: 報告整合內容
    report_datetime: 報告日期
    '''
    squad_id = models.IntegerField() 
    member_report_status = models.CharField(max_length=200)
    report_title = models.TextField(blank=True) 
    # report_title_start = models.TextField(blank=True) 
    # report_title_between = models.TextField(blank=True) 
    # report_title_end = models.TextField(blank=True) 
    report_info = models.TextField(blank=True)
    report_datetime = models.DateTimeField(blank=True)

    def __str__(self):
        return str(self.squad_id) + str(self.member_report_status)

    def getSubmittedNum(self):
        if isinstance(self.member_report_status, str):
            member_report_status = literal_eval(self.member_report_status)
        else:
            member_report_status = self.member_report_status
        
        result = 0
        for i in list(member_report_status.values()):
            if i != '':
                result+=1
        return result
    
    def genReport(self, squad_info):
        report_info = self.report_title.format(self.squad_id, squad_info.member_num, self.getSubmittedNum())
        
        if isinstance(self.member_report_status, str):
            member_report_status = literal_eval(self.member_report_status)
        else:
            member_report_status = self.member_report_status
        
        not_submitted_part = '''未繳交：\n'''
        submitted_part = ''

        for i in literal_eval(squad_info.member_id):
            if member_report_status[i] == '':
                member_id = '{0:03d}'.format(i)
                not_submitted_part += ('''{}-{}：\n'''.format(squad_info.squad_id, member_id))
            else:
                submitted_part += (member_report_status[i] + '''\n\n''')
        
        if self.getSubmittedNum() < squad_info.member_num: 
            not_submitted_part += '''\n'''
            report_info += not_submitted_part + submitted_part
        else:
            report_info += submitted_part
        # print(report_info)
        
        return report_info
    
    def addReport(self, current_member_id, current_member_message):
        if isinstance(self.member_report_status, str):
            member_report_status = literal_eval(self.member_report_status)
            member_report_status[current_member_id] = current_member_message
            self.member_report_status = member_report_status
        else:
            self.member_report_status[current_member_id] = current_member_message

        return
