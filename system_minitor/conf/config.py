# coding=utf-8
mess = u"""
【告警信息】

"""
minitor_map = {
    "Local": {
        "items": ["cpu", "memory"],
        "trigger": {
            "cpu": 80,
            "memory": 80
        },
        "batch": 1
    }
}

mail_addr = ['11003@sangfor.com']
mail_theam = "Monitor Notes"
mail_server = "Mgmailsvr/sangfor"
mail_user = "mail\郑茂11003"
batch_time = 2
