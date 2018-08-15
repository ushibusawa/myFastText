import lxml.html
import os
import sys
import re
import MeCab
import random

# td要素からテキスト抽出
def td2string(e):
    # 先頭と末尾の改行を削除(strip)
    # 文字列途中の改行は半角空白に置換
    str =  e.text_content().strip()
    return re.sub('\n', ' ', str)

def extract(htmlfile, rule):
    # htmlを開いてDOMを取得
    with open(htmlfile, 'r') as fin:
        dom = lxml.html.fromstring(fin.read())

    # table内の要素 <tr><td>XXX</td></tr> を取得
    elems = dom.xpath('//table[@class="qma-problems"]/tr/td/.')

    list = []
    # 形式ごとに不要な列を除外
    # [x::y] 0から数えてx番目の要素をy個置きに取得
    if rule is 'true_or_false':
        # ○×：問題文、正解○×　→　正解を除外
        question = elems[0::2]
        for q in question:
            list.append(td2string(q))
    if rule in {'four', 'associate', 'order', 'multi', 'group'}:
        # 四択：問題文、選択肢、解答○×　→　解答を削除
        # 連想：問題文、選択肢、解答○×　→　解答を削除
        # 順番あて：問題文、選択肢、順番　→　順番を削除
        # 一問多答：問題文、選択肢、解答　→　解答を削除
        # グループ分け：問題文、選択肢、解答　→　解答を削除
        question = elems[0::3]
        choices = elems[1::3]
        for q, c in zip(question, choices):
            if rule is 'group':
                qstr = re.sub('A: |B: |C: ' , '', td2string(q))
            else:
                qstr = td2string(q)
            list.append(' '.join([qstr, td2string(c)]))
    if rule in {'panel', 'sort', 'cube'}:
        # パネル：問題文、パネル文字、正解　→　パネル文字を削除
        # 並べ替え：問題文、元の文字列、正解　→　元の文字列を削除
        # キューブ：問題文、元の文字列、正解　→　元の文字列を削除
        question = elems[0::3]
        answer = elems[2::3]
        for q, a in zip(question, answer):
            list.append(' '.join([td2string(q), td2string(a)]))
    if rule is 'effect':
        # エフェクト：問題文、エフェクト、解答（ひらがな）　→　解答を削除
        question = elems[0::3]
        answer = elems[1::3]
        for q, a in zip(question, answer):
            list.append(' '.join([td2string(q), td2string(a)]))
    if rule is 'line':
        # 線結び：問題文、選択肢１、選択肢２、順番　→　順番を削除
        question = elems[0::4]
        left_choices = elems[1::4]
        right_choices = elems[2::4]
        for q, l, r in zip(question, left_choices, right_choices):
            l2 = re.sub('A. |B. |C. ' , '', td2string(l))
            r2 = re.sub('1. |2. |3. ' , '', td2string(r))
            list.append(' '.join([td2string(q), l2, r2]))
    if rule in {'slot', 'type'}:
        # スロット：問題文、正解
        # タイピング：問題文、正解
        question = elems[0::2]
        answer = elems[1::2]
        for q, a in zip(question, answer):
            list.append(' '.join([td2string(q), td2string(a)]))

    return list

def extract_all():
    genre_list = ['anime_game', 'sport', 'entertainment', 'lifestyle',
             'society', 'literature', 'science']
    gname_list = ['アニメ＆ゲーム', 'スポーツ', '芸能', 'ライフスタイル',
             '社会', '文系学問', '理系学問']
    rule_list = ['true_or_false', 'four', 'associate', 'sort', 'panel',
            'slot', 'type', 'effect', 'cube', 'order',
            'line', 'multi', 'group']

    tagger = MeCab.Tagger('-Owakati')

    for genre, gname in zip(genre_list, gname_list):
        g_result = []
        label = '__label__' + gname
        for rule in rule_list:
            input_file = genre + '-' + rule + '.html'
            # htmlから問題文リストを抽出
            result = extract(input_file, rule)
            # 中間ファイルを保存
#            output_file = '__extract__' + g + '-' + r + '.txt'
#            with open(output_file, 'wt') as fout:
#                fout.write('\n'.join(result))
            # 一問ごとにラベルを付与
            for item in result:
                wakati = tagger.parse(item)
                g_result.append(' , '.join([label, wakati]))

        # 学習データをサンプリング（各ジャンル1000個ずつとする）
        g_traindata = random.sample(g_result, 1000)
        with open('__traindata__' + genre + '.txt', 'wt') as fout:
            fout.write(''.join(g_traindata))

        # テストデータは元データと学習データの差分とする
        diff = set(g_result) - set(g_traindata)
        g_testdata = list(diff)
        with open('__testdata__' + genre + '.txt', 'wt') as fout:
            fout.write(''.join(g_testdata))

if __name__ == '__main__':
    extract_all()
'''
    argvs = sys.argv
    input_file = argvs[1]
    rule = argvs[2]

    result = extract(input_file, rule)
    output_file = '__extract__' + rule + '.txt'
    with open(output_file, 'wt') as fout:
        fout.write('\n'.join(result))
'''
