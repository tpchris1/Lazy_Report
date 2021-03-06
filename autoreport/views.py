from typing import Text
from django.core.checks import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from .models import Admin, Squad, Report
from .messages import * 

import ast
import re
from datetime import date


line_bot_api = LineBotApi(settings.AUTOREPORT_LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.AUTOREPORT_LINE_CHANNEL_SECRET)

squad_id_member_id_pattern = re.compile('\d{1,2}\-\d\d\d') # 一或兩位數班級-三位數學號，匹配訊息是否為3-038這種格式

def adminUserAll(event, current_user):
    if current_user: # 如果不是第一次設定Admin
        if 'set' in event.message.text: # 設定目前Admin的設定資訊
            adminSetAgain(event, current_user)
        elif 'show' in event.message.text: # 顯示目前Admin的設定資訊
            line_bot_api.reply_message(  
                                       event.reply_token,
                                       TextSendMessage(text=admin_set_confirm_message.format(current_user.name, current_user.handle_squad_id, current_user.line_id))
                                      )
        elif 'delete' in event.message.text: # 刪除原本Admin的設定資訊
            current_user.delete()
            line_bot_api.reply_message(  
                        event.reply_token,
                        TextSendMessage(text=admin_delete_message.format(current_user.name, current_user.handle_squad_id))
                    )
    elif 'set' in event.message.text: # 第一次設定Admin
            adminSetInitial(event) # 設定目前Admin的設定資訊
    else:
        line_bot_api.reply_message(  
                                   event.reply_token,
                                   TextSendMessage(text=admin_error_message + '''\n\n''' + admin_help_message)
                                  )
    return

def adminSetInitial(event):
    try:
        current_user_name = line_bot_api.get_profile(event.source.user_id).display_name
        current_user = Admin(
                    name=current_user_name,
                    line_id=event.source.user_id, 
                    handle_squad_id=int(event.message.text.split(' ')[2]),
                    )
        
        current_user.save()

        line_bot_api.reply_message(  
                event.reply_token,
                TextSendMessage(text=admin_set_confirm_message.format(current_user.name, current_user.handle_squad_id, current_user.line_id))
            )
    except: # 格式錯誤回覆
        line_bot_api.reply_message(  
                event.reply_token,
                TextSendMessage(text=admin_set_error_message)
            )
    return

def adminSetAgain(event, current_user):
    try:
        current_user.name = line_bot_api.get_profile(event.source.user_id).display_name
        current_user.handle_squad_id=int(event.message.text.split(' ')[2])
        
        current_user.save()

        line_bot_api.reply_message(  
                event.reply_token,
                TextSendMessage(text=admin_set_confirm_message.format(current_user.name, current_user.handle_squad_id, current_user.line_id))
            )
    except: # 格式錯誤回覆
        line_bot_api.reply_message(  
                event.reply_token,
                TextSendMessage(text=admin_set_error_message)
            )
    return

def squadUserAll(event, current_user):
    existed = False
    if Squad.objects.all().filter(squad_id=current_user.handle_squad_id): # 資料庫裡面有對應的群組資訊
        current_squad = Squad.objects.all().filter(squad_id=current_user.handle_squad_id)[0]
        existed = True
    else: # 資料庫裡面沒有群組資料
        current_squad = Squad(squad_id=current_user.handle_squad_id, member_num=-1, member_id="None", line_group_id="None")
        existed = False

    if 'show' in event.message.text: # 顯示目前班級設定資訊
        if existed:
            message = squadinfo_show_message.format(current_squad.squad_id, 
                                                 current_squad.member_num, 
                                                 current_squad.member_id, 
                                                 current_squad.line_group_name, 
                                                 current_squad.line_group_id)
        else:
            message = squadinfo_show_notexisted_message +  '''\n\n''' + squadinfo_help_message
        
        line_bot_api.reply_message(  
                    event.reply_token,
                    TextSendMessage(text = message)
                )
    elif "delete" in event.message.text: # 刪除當前班級資訊
        if existed:
            current_squad.delete()
            message = squadinfo_delete_message + squadinfo_show_message.format(current_squad.squad_id, 
                                                                        current_squad.member_num, 
                                                                        current_squad.member_id, 
                                                                        current_squad.line_group_name, 
                                                                        current_squad.line_group_id)
        else:
            message = squadinfo_delete_notexisted_message + '''\n\n''' + squadinfo_help_message

        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=message))
    elif "set" in event.message.text and "member_num" in event.message.text: # 設定班級人數
        try:
            current_squad.member_num = event.message.text.split(' ')[3]
            current_squad.save()
            line_bot_api.reply_message(  
                    event.reply_token,
                    TextSendMessage(text= squadinfo_show_message.format(current_squad.squad_id, 
                                                                        current_squad.member_num, 
                                                                        current_squad.member_id, 
                                                                        current_squad.line_group_name, 
                                                                        current_squad.line_group_id))
                )
        except:
            line_bot_api.reply_message(  
                    event.reply_token,
                    TextSendMessage(text=squadinfo_set_member_num_error_message)
                )
    elif "set" in event.message.text and "member_id" in event.message.text: # 設定班級學號
            current_squad.member_id = [int(i) for i in (event.message.text.split(' ')[3:])]
            if len(current_squad.member_id) == current_squad.member_num and all(isinstance(i, int) for i in current_squad.member_id):
                current_squad.save()    
                line_bot_api.reply_message(  
                            event.reply_token,
                            TextSendMessage(text= squadinfo_show_message.format(current_squad.squad_id, 
                                                                                current_squad.member_num, 
                                                                                current_squad.member_id, 
                                                                                current_squad.line_group_name, 
                                                                                current_squad.line_group_id))
                        )
            else:
                line_bot_api.reply_message(  
                        event.reply_token,
                        TextSendMessage(text=squadinfo_set_member_id_error_message)
                    )
            # print(current_squad.member_id, len(current_squad.member_id))
    else: # 顯示如何使用squadinfo菜單
        line_bot_api.reply_message(  
                    event.reply_token,
                    TextSendMessage(text=squadinfo_help_message)
                )
    return

def reportUserAll(event, current_user):
    if "show" in event.message.text:
        if Report.objects.all().filter(squad_id=current_user.handle_squad_id, report_datetime=date.today()):
            current_report = Report.objects.all().filter(squad_id=current_user.handle_squad_id, report_datetime=date.today())[0]
            current_squad = Squad.objects.all().filter(squad_id=current_user.handle_squad_id)[0]
            line_bot_api.reply_message(  
                    event.reply_token,
                    TextSendMessage(text=current_report.genReport(current_squad))
                )
        else: # 沒有報告可以刪除
            line_bot_api.reply_message(  
                    event.reply_token,
                    TextSendMessage(text=report_show_failed_message.format(current_user.handle_squad_id, date.today()))
                )
    elif "delete" in event.message.text:
        # print(Report.objects.all())
        if Report.objects.all().filter(squad_id=current_user.handle_squad_id, report_datetime=date.today()): # 找到可以刪除的報告
            current_report = Report.objects.all().filter(squad_id=current_user.handle_squad_id, report_datetime=date.today())[0]
            current_squad = Squad.objects.all().filter(squad_id=current_user.handle_squad_id)[0]
            line_bot_api.reply_message(  
                    event.reply_token,
                    TextSendMessage(text=report_delete_message + current_report.genReport(current_squad))
                )
            current_report.delete()
        else: # 沒有報告可以刪除
            line_bot_api.reply_message(  
                    event.reply_token,
                    TextSendMessage(text=report_delete_fail_message.format(current_user.handle_squad_id, date.today()))
                )
    elif "send" in event.message.text:
        if Squad.objects.all().filter(squad_id=current_user.handle_squad_id): # 先檢查是否存在小組
            current_squad = Squad.objects.all().filter(squad_id=current_user.handle_squad_id)[0]
            if Report.objects.all().filter(squad_id=current_user.handle_squad_id, report_datetime=date.today()): # 找到今天本班的報告
                current_report = Report.objects.all().filter(squad_id=current_user.handle_squad_id, report_datetime=date.today())[0]
                line_bot_api.push_message(current_squad.line_group_id, TextSendMessage(text=current_report.genReport(current_squad)))
            else:
                line_bot_api.reply_message(  
                    event.reply_token,
                    TextSendMessage(text=report_send_failed_no_report_message.format(current_user.handle_squad_id, date.today()))
                )
        else:
            line_bot_api.reply_message(  
                event.reply_token,
                TextSendMessage(text=report_send_failed_no_squad_message)
            )
        
    else:
        line_bot_api.reply_message(  
                    event.reply_token,
                    TextSendMessage(text=report_help_message)
                )
    return

def processUser(event):
    if Admin.objects.all().filter(line_id=event.source.user_id): # 已經設定過自己的賬戶訊息為Admin
        current_user = Admin.objects.all().filter(line_id=event.source.user_id)[0]

        if 'admin' in event.message.text:
            adminUserAll(event,current_user)
        elif "squadinfo" in event.message.text: # 對班級資訊做操作
            squadUserAll(event, current_user)
        elif "report" in event.message.text: # 對報告做操作
            reportUserAll(event, current_user)
        else: # 顯示所有的選項資訊
            line_bot_api.reply_message(  
                            event.reply_token,
                            TextSendMessage(text=come_back_welcome_message)
                        )
    else: # 當前用戶沒有設定過自己的Admin資訊
        if 'admin' in event.message.text: # 首次使用設定負責的班級
            adminUserAll(event, None)
        else: # 首次使用介紹訊息
            line_bot_api.reply_message(  
                        event.reply_token,
                        TextSendMessage(text=first_welcome_message)
                    )
    return


def squadSetGroupLineID(event):
    current_user = Admin.objects.all().filter(line_id=event.source.user_id)[0]
    if Squad.objects.all().filter(squad_id=current_user.handle_squad_id): # 資料庫裡面有對應的群組資訊
        current_squad = Squad.objects.all().filter(squad_id=current_user.handle_squad_id)[0]
        if current_squad.member_id == 'None':
            message =  squadinfo_set_line_group_id_fail_no_member_id_message
        else:
            current_squad.line_group_id = event.source.group_id
            current_squad.line_group_name = line_bot_api.get_group_summary(event.source.group_id).group_name 
            current_squad.save()
            
            message = squadinfo_set_line_group_id_success_message + '''\n\n''' + squadinfo_show_message.format(current_squad.squad_id, 
                                                                                                            current_squad.member_num, 
                                                                                                            current_squad.member_id, 
                                                                                                            current_squad.line_group_name, 
                                                                                                            current_squad.line_group_id)
        # 通知Admin班級群組設定狀況
        line_bot_api.push_message(current_user.line_id, TextSendMessage(text = message))
    
    return

def reportCollectFromGroup(event, current_member_squad_id, current_member_id):
    if Squad.objects.all().filter(squad_id=current_member_squad_id): # 班級資訊設定已經完成
        current_squad = Squad.objects.all().filter(squad_id=current_member_squad_id)[0]
        # member_id = ast.literal_eval(current_squad.member_id)
        # 開始設定report狀況，檢查是否當前report存在
        if Report.objects.all().filter(squad_id=current_member_squad_id, report_datetime = date.today()):
            current_report = Report.objects.all().filter(squad_id=current_member_squad_id, report_datetime = date.today())[0]
        else: # 不存在今天該班的report
            # member_report_status = [False for i in range(current_squad.member_num)]
            member_report_status = dict(zip(ast.literal_eval(current_squad.member_id), ['' for i in ast.literal_eval(current_squad.member_id)]))
            current_report = Report(squad_id=current_member_squad_id, 
                                    member_report_status=member_report_status, 
                                    report_title=report_report_title, 
                                    report_datetime=date.today())
        current_report.addReport(current_member_id, event.message.text)
        current_report.save()
        
        current_report.genReport(current_squad)
        
        if current_report.getSubmittedNum() == current_squad.member_num:
            current_report.genReport(current_squad)
            
            # member_report_status[current_member_id] = event.message.text
            # print(current_report.squad_id) 
            # print(current_report.member_report_status, type(current_report.member_report_status)) 
            # print(current_report.report_title)
            # print(current_report.report_info)
            # print(current_report.report_datetime)
    return

def processGroup(event):
    
    # 設定當前group的lineID
    if Admin.objects.all().filter(line_id=event.source.user_id) and 'set' in event.message.text:
        squadSetGroupLineID(event)

    if squad_id_member_id_pattern.match(event.message.text): # 匹配訊息是否為3-038這種格式
        current_member_squad_id = int(squad_id_member_id_pattern.match(event.message.text).group().split('-')[0])
        current_member_id = int(squad_id_member_id_pattern.match(event.message.text).group().split('-')[1])
        reportCollectFromGroup(event, current_member_squad_id, current_member_id)
             
    return    


@csrf_exempt
def callback(request):
 
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                # print(event)
                if event.source.type == 'user':
                    processUser(event)
                elif event.source.type == 'group':
                    processGroup(event)
                # line_bot_api.reply_message(  # 回復傳入的訊息文字
                #     event.reply_token,
                #     TextSendMessage(text=event.message.text)
                # )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

