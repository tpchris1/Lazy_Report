from re import error


work_flow_message = '''簡單的6步驟如下：\n1. 設定你自己的是第幾班\n2. 設定班級的人數\n3. 設定班級所有人的學號\n4. 把bot拉到自己班群以及需要回報的班長群\n5. 告訴bot哪個是班群，哪個是班長群\n6. 手機扔一邊不用管了'''
initial_menu_message = '''使用方法：\n1. help 顯示本使用方法\n2. admin 有關你的資訊的操作菜單\n3. squadinfo 你所在班級的資訊的操作菜單\n4. report 關於回報內容的使用方法'''
first_welcome_message = '''歡迎使用LazyReport懶得回報!\n\n''' + work_flow_message +'''\n\n首次使用請通過\nadmin set 班級\n來設定你自己負責第幾班！\n\n''' + initial_menu_message
come_back_welcome_message = '''歡迎回來LazyReport懶得回報!\n\n''' + work_flow_message +'''\n\n''' + initial_menu_message

admin_help_message = '''個人資訊設定使用方法：\n1. admin set 班級 設定你的個人資訊（如admin set 3）\n2. admin show 顯示你的個人資訊\n3. admin delete 刪除你的個人資訊'''
admin_set_confirm_message = '''您的個人資訊設定如下：\n您的名字是： {} \n您負責的班級是： 第{}班\n您的Line UID是： {}'''
admin_set_error_message = '''設定格式錯誤，請重新輸入：\nadmin set 負責班級號碼\n如：\nadmin set 3'''
admin_delete_message = '''您已經刪除的設定如下：\n您的名字是： {} \n您負責的班級是： 第{}班\n\n注：因您已經刪除您的個人資訊，若仍需使用請使用\nadmin set 班級\n重新設定'''
admin_error_message = '''尚未設定您的個人資訊，請使用\nadmin set 班級\n重新設定'''

squadinfo_show_message = '''您的班級設定如下：\n負責的班級： 第{}班\n班級人數： {}員\n班級人員學號： {}\n班群名稱：{}\n班群UID：{}'''
squadinfo_show_notexisted_message = '''尚未設定班級資訊，請先設定班級資訊'''
squadinfo_delete_message = '''已經刪除的班級資訊如下：\n\n'''
squadinfo_delete_notexisted_message = '''尚未設定班級資訊，請先設定班級資訊'''
squadinfo_set_member_num_error_message = '''設定格式錯誤，請重新輸入：\nsquadinfo set member_num 人數\n如：\nsquadinfo set member_num 18'''
squadinfo_set_member_id_error_message = '''設定格式錯誤，請重新輸入：\nsquadinfo set member_id 學號列表\n如：\nsquadinfo set member_id 35 36 37 38 39...\n注：請先設定人數(member_num)，且學號數量需要與人數一致'''
squadinfo_help_message = '''班級資訊設定使用方法：\n1. squadinfo set member_num 設定班級成員人數\n2. squadinfo set member_id 設定班級成員學號\n3. squadinfo show 顯示班級設定資訊\n4. squadinfo delete 刪除班級資訊'''

squadinfo_set_line_group_id_success_message = "成功設定班級群組的ID!"
squadinfo_set_line_group_id_fail_no_member_id_message = "尚未設定班級學號，請先設定班級學號!\n輸入：\nsquadinfo set member_id 學號列表\n如：\nsquadinfo set member_id 35 36 37 38 39..."

report_report_title = '''{}班休假回報\n應到{}員 實到{}員\n\n'''
report_show_failed_message='''沒有第{}班在{}的任何報告可以顯示'''
report_delete_message='''已經刪除的報告如下:'''
report_delete_fail_message = '''沒有第{}班在{}的任何報告可以刪除'''
report_send_failed_no_squad_message='''沒有設定對應的班級資訊，無法提交報告，請先輸入squadinfo以設定班級資訊'''
report_send_failed_no_report_message='''沒有第{}班在{}的任何報告，無法提交報告，請先等待報告提交'''
report_help_message = '''回報資訊使用方法：\n1. report show 顯示目前所有回報狀況\n2. report delete 刪除當前班級的所有當日回報\n3. report send 將報告送到班頭群以及班群'''

