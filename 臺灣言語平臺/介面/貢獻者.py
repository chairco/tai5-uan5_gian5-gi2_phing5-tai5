# -*- coding: utf-8 -*-
from django.http.response import JsonResponse

from 臺灣言語資料庫.關係模型 import 文本校對表


def 貢獻者表(request):
    # 2 = 臺灣閩南語常用詞辭典, 269 = 台文華文線頂辭典
    contributor_dict = {}

    for 文本 in 文本校對表.objects.prefetch_related('舊文本__來源'):
        # 取出第一層
        來源_id = 文本.舊文本.來源_id
        來源名稱 = 文本.舊文本.來源.名

        if 來源_id not in contributor_dict:
            contributor_dict[來源_id] = dict()
            contributor_dict[來源_id]['名'] = 來源名稱
            contributor_dict[來源_id]['數量'] = 0
        contributor_dict[來源_id]['數量'] += 1

    result = list()

    for user in sorted(contributor_dict.values(),
                       key=lambda x: x['數量'], reverse=True):
        if user['名'] == '匿名':
            user['名'] = '沒有人'
        result.append(user)

    return JsonResponse({"名人": result})


def 正規化團隊表(request):
    數量表 = {}
    for 來源名稱 in 文本校對表.objects.values_list('新文本__來源__名', flat=True):
        try:
            數量表[來源名稱] += 1
        except KeyError:
            數量表[來源名稱] = 1
    名人 = []
    for 名, 量 in sorted(數量表.items(), key=lambda 數量: 數量[1], reverse=True):
        名人.append({'名': 名, '數量': 量})
    return JsonResponse({"名人": 名人})
