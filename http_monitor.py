import os
import sys
import requests
import time
from sdcclient import SdMonitorClient

#
# 入力したURLにアクセスしてステータスコードを返す
#
def getWebStatus(url):
    try:
        rq = requests.get(url, timeout=3.0)
        return(rq.status_code)

    except:
        print('//URL監視エラー//')
        return(False)

    
#
# メイン
#

# OS環境変数(シークレット)から環境変数を取得
cm_api_token = os.getenv('CM_API_TOKEN')
cm_url = os.getenv('CM_URL')
mon_url = os.getenv('MON_URL')

cm_event_name = os.getenv('CM_EVENT_NAME')
cm_event_description = os.getenv('CM_EVENT_DESCRIPTION')
cm_event_severity = os.getenv('CM_EVENT_SEVEIRTY')



# 監視対象のURLのステータスコード取得。Webページに問題なくてもステータス取得に失敗することがあるので3回までリトライする
for i in range(3):
    url_status = getWebStatus(mon_url)
    cm_event_scope='url = \"' + mon_url + '\" and status_code = \"' + str(url_status) + '\"'
    print(cm_event_scope)
    if url_status == 200:
        break
    print("Status Code is not 200. Retry URL Check ...")
    time.sleep(10)

# ステータスコードが200でないか取得に失敗した場合はIBM Cloud Monitoringにイベントを発行する
if url_status != 200 or url_status == False:
    # Sysdigクライアントを作成
    sdclient = SdMonitorClient(cm_api_token,cm_url)
    
    # Sysdigイベントを発行
    try:
        res = sdclient.post_event(cm_event_name,cm_event_description,cm_event_severity,cm_event_scope)
    except:
        print('//イベント作成エラー//')
        res=False
    print(res)

time.sleep(1)
