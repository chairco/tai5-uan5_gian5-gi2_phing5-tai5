from dateutil import tz
from django.http.response import JsonResponse


from 臺灣言語平臺.項目模型 import 平臺項目表

from 臺灣言語資料庫.資料模型 import 來源表

_臺北時間 = tz.gettz('Asia/Taipei')
_時間輸出樣式 = '%Y-%m-%d %H:%M:%S'
def 轉做臺北時間字串(時間物件):
	return 時間物件.astimezone(_臺北時間).strftime(_時間輸出樣式)

def 外語請教條相關資料內容(request):
	try:
		外語請教條項目編號 = request.GET['平臺項目編號']
	except:
		return JsonResponse({'錯誤': '沒有平臺項目的編號'})
		
	try:
		外語項目 = 平臺項目表.揣編號(int(外語請教條項目編號))
		外語 = 外語項目.外語
		
		回應資料 = {}
		回應資料['外語請教條項目編號'] = 外語請教條項目編號
		回應資料['外語資料'] = 外語.外語資料
		回應資料['外語語言'] = 外語.外語語言.語言腔口
	except:
		return JsonResponse({'錯誤': '這不是外語請教條的編號'})
	
	回應資料['新詞影音'] = []
	for 翻譯影音 in 外語.翻譯影音.all():
		影音 = 翻譯影音.影音
		回應影音 = {'新詞影音項目編號':str(影音.平臺項目.get().編號())}
		回應影音['影音資料網址'] = 影音.網頁影音資料.url
		回應影音['新詞文本'] = []
		for 影音文本 in 影音.影音文本.all():
			文本 = 影音文本.文本
			回應文本 = {'新詞文本項目編號':str(文本.平臺項目.get().編號())}
			回應文本['文本資料'] = 文本.文本資料
			回應影音['新詞文本'].append(回應文本)
		回應資料['新詞影音'].append(回應影音)
		
	回應資料['新詞文本'] = []
	for 翻譯文本 in 外語.翻譯文本.all():
		文本 = 翻譯文本.文本
		回應文本 = {'新詞文本項目編號':str(文本.平臺項目.get().編號())}
		回應文本['文本資料'] = 文本.文本資料
		回應資料['新詞文本'].append(回應文本)
	return JsonResponse(回應資料)

def 看資料單一內容(request):
	try:
		平臺項目編號 = request.GET['平臺項目編號']
	except:
		return JsonResponse({'錯誤': '沒有平臺項目的編號'})
	try:
		平臺項目 = 平臺項目表.揣編號(int(平臺項目編號))
		資料 = 平臺項目.資料()
	except:
		return JsonResponse({'錯誤': '這不是合法平臺項目的編號'})
	return JsonResponse({
			'收錄者':資料.收錄者.編號(),
			'來源':資料.來源.編號(),
			'收錄時間':轉做臺北時間字串(資料.收錄時間),
			'種類':資料.種類.種類,
			'語言腔口':資料.語言腔口.語言腔口,
			'版權':資料.版權.版權,
			'著作所在地':資料.著作所在地.著作所在地,
			'著作年':資料.著作年.著作年,
			'屬性內容':資料.屬性內容(),
			'推薦用字':平臺項目.推薦用字結果(),
		})

def 看來源內容(request):
	try:
		來源編號 = request.GET['來源編號']
	except:
		return JsonResponse({'錯誤': '沒有來源編號的參數'})
	try:
		來源 = 來源表.objects.get(pk=來源編號)
	except:
		return JsonResponse({'錯誤': '這不是合法的來源編號'})
	來源內容 = {
			'名':來源.名,
			'屬性內容':來源.屬性內容(),
		}
	try:
		來源內容['email'] = 來源.使用者.email
		來源內容['分數'] = 來源.使用者.分數
	except:
		pass
	return JsonResponse(來源內容)
