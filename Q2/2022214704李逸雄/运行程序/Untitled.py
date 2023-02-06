#encoding:utf-8

# 邮件通知功能
import zmail

Mail={
    "from":'3422135005@qq.com',
    "pwd":'zoldormxgtkcdacj',
}
receiver_list=['1783172311@qq.com']

Mail_Content={
    'subject':"MachineMonitor",
    'content_text':'这是监测日志,请查收',
    'attachments':r'C:\Users\李逸雄\Desktop\运维监测系统\运行程序\MonitoringLog.txt'
}
if __name__=="__main__":
    try:
        server=zmail.server(Mail['from'],Mail['pwd'])
        server.send_mail(receiver_list[0],Mail_Content)

        print('\n')
        print('******邮件发送成功!******')
    except Exception as e:
        print('发送失败',e)