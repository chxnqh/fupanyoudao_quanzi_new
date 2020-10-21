import os
import re
import time
import json
import requests

from pprint import pprint

path = ''




def send_msg(msg, anonymous=0):

    return
    #这里换成你的接收新发言的方式

    send_msg_qwx = 'http://172.18.3.201:4000/send?t={}&tos={}&content={}'
    send_msg_qqq = 'http://127.0.0.1:4444/{}'

    bot = 9227575
    group = 195208438 #195208331 195207904 （使用帮助：QQ群195208438）

    data = {
            "bot": bot,
            "group": group,
            "msg": msg,
            "url": msg,
            "anonymous": anonymous,
            }

    try:
        s = requests.post(url=send_msg_qqq.format('send_group_msg'), data=data)
    except Exception as e:
        s = requests.get(send_msg_qwx.format(1, 23, msg))

    return s






class CirclesComments(object):

    def __init__(self):

        self.circle_content_detail = 'https://www.fupanyoudao.com/api/circleapi/circle_content_detail?id={}'
        # 选择是抽取全部，还是仅仅锋芒发言
        self.article_url_lst = {
             '全部' : 'https://www.fupanyoudao.com/api/circleapi/?userid=16556&circle_id=66&page_num={}&page_size={}',
            #'圈主' : 'https://www.fupanyoudao.com/api/circleapi/get_circle_owner?userid=16556&circle_id=66&page_num={}&page_size={}',
            #'精华' : 'https://www.fupanyoudao.com/api/circleapi/get_essence?userid=16556&circle_id=66&page_num={}&page_size={}',
        }


    def get_comments(self):

        for index, article_url in self.article_url_lst.items():

            fname = path + '{}_circle_{}_{}.json'.format(os.path.basename(__file__).split(".")[0], '16556', '66')
            if os.path.isfile(fname):
                with open(fname, 'r', encoding='utf-8') as f:
                    save_comments_json = json.load(f)
            else:
                save_comments_json = {}

            for i in range(1, 10):
                comments = requests.get(article_url.format(i, 10)).json()
                #pprint(comments)

                if comments:
                    elected_comment_lst = comments['data'] if 'data' in comments else {}

                if elected_comment_lst == {}:
                    continue


                '''
                # 主页（评论只有最新的6条）
                comments_json = {
                    item['id']: {
                        'comment' : {
                            _item['id']: {
                                'content': _item['content'],
                                'from_nickname': _item['from_nickname'],
                                'from_user_is_owner': _item['from_user_is_owner'],
                                'from_userid': _item['from_userid'],
                                'to_nickname': _item['to_nickname'],
                                'to_userid': _item['to_userid'],
                                'type': _item['type'],
                            }
                            for _item in item['comment']
                        },
                        'adtime': item['adtime'],
                        'comment_num': item['comment_num'],
                        'content': item['content'],
                        'essence': item['essence'],
                        'img': item['img'],
                        'is_owner': item['is_owner'],
                        'is_zan': item['is_zan'],
                        'nickname': item['nickname'],
                        'top': item['top'],
                        'userid': item['userid'],
                        'userimg': item['userimg'],
                        'zan': item['zan'],
                    }
                    for item in elected_comment_lst
                }
                '''

                for item in elected_comment_lst:
                    content = requests.get(self.circle_content_detail.format(item['id'])).json()

                    '''
                    comments_json = {
                        item['id']: {
                            'content': content['data'],
                            'comment': {
                                #comment['id']['replylist']: {
                                #    reply['id']: reply
                                #    for reply in comment['replylist']
                                #    },
                                comment['id']: comment
                                for comment in content['commentlist']
                                }
                        }
                    }
                    '''
                    try:
                        comments_json = {
                            item['id']: {
                                'content': {
                                    'adtime': content['data']['adtime'],
                                    'circle_id': content['data']['circle_id'],
                                    'comment_num': content['data']['comment_num'],
                                    'content': content['data']['content'],
                                    'essence': content['data']['essence'],
                                    'img': content['data']['img'],
                                    'is_content_zan': content['data']['is_content_zan'],
                                    'is_owner': content['data']['is_owner'],
                                    'nickname': content['data']['nickname'],
                                    'top': content['data']['top'],
                                    'userid': content['data']['userid'],
                                    'userimg': content['data']['userimg'],
                                    'zan': '1',
                                    },
                                'comment': {
                                    comment['id']: {
                                        'adtime': comment['adtime'],
                                        'comment_num': comment['comment_num'],
                                        'content': comment['content'],
                                        'from_nickname': comment['from_nickname'],
                                        'from_user_is_owner_comment': comment['from_user_is_owner_comment'],
                                        'img': comment['img'],
                                        'is_comment_zan': comment['is_comment_zan'],
                                        'to_userid': comment['to_userid'],
                                        'userimg': comment['userimg'],
                                        'zan': comment['zan'],
                                        'replylist': {
                                            reply['id']: {
                                                #'adtime': reply['adtime'],
                                                 'content': reply['content'],
                                                 'from_nickname': reply['from_nickname'],
                                                 'from_user_is_owner_reply': reply['from_user_is_owner_reply'],
                                                 'from_userid': reply['from_userid'],
                                                 'img': reply['img'],
                                                 'to_nickname': reply['to_nickname'],
                                                 'to_user_is_owner_reply': reply['to_user_is_owner_reply'],
                                                 'to_userid': reply['to_userid'],
                                                 }
                                            for reply in comment['replylist']
                                            },
                                    }
                                    for comment in content['commentlist']
                                    }
                            }
                        }
                    except Exception as e:
                        print('comments_json:', e)

                    #pprint(comments_json)

                    save_comments_json = self.merge_json(comments_json, save_comments_json)

            with open(fname, 'w+', encoding='utf-8') as f:
                json.dump(save_comments_json, f)


    def merge_json(self, comments_json, save_comments_json):

        try:
            for key, value in comments_json.items():
                new_content = False
                new_comment = False
                new_reply = False
                if not key in save_comments_json.keys():
                    new_content = True
                else:
                    try:
                        for _key, _value in value['comment'].items():
                            if not _key in save_comments_json[key]['comment'].keys():
                                new_comment = True
                            else:
                                try:
                                    for __key, __value in value['comment']['replylist'].items():
                                        if not __key in save_comments_json[key]['comment']['replylist'].keys():
                                            new_reply = True
                                except Exception as e:
                                    pass
                    except Exception as e:
                        pass

                if new_content or new_comment or new_reply:
                    save_comments_json[key] = value
                    msg = self.format_comment(value)
                    send_msg(msg)
                    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    print(localtime, '复盘有道', msg.split(' ')[5].replace('\n', ' ')[:100], '...')

        except Exception as e:
            pass

        return save_comments_json


    def format_comment(self, data):

        content = ''
        comment = ''

        try:

            for key, value in data['comment'].items():
                reply = ''
                try:
                    for _key, _value in value['replylist'].items():
                        from_user_is_owner_reply = '★' if int(_value['from_user_is_owner_reply']) else ''
                        to_user_is_owner_reply = '★' if int(_value['to_user_is_owner_reply']) else ''
                        reply += '{}{}{} 回复 {}: {}\n\n'.format(from_user_is_owner_reply, to_user_is_owner_reply, _value['from_nickname'], _value['to_nickname'], _value['content'],)
                except Exception as e:
                    print(e)
                    pass

                is_comment_zan = '★' if int(value['is_comment_zan']) else ''
                from_user_is_owner_comment = '★' if int(value['from_user_is_owner_comment']) else ''
                comment += '{}{} {} ({}) {}\n{}\n\n{}'.format(from_user_is_owner_comment, value['from_nickname'], value['adtime'], value['zan'], is_comment_zan, value['content'], reply)

        except Exception as e:
            print(e)
            pass

        essence = '[精华]' if int(data['content']['essence']) else ''
        is_owner = '[圈主]' if int(data['content']['is_owner']) else ''
        is_content_zan = '★' if int(data['content']['is_content_zan']) else ''
        content = '[复盘有道] 锋芒实战圈子 {}{}{}\n\n{} {} ({})\n{}\n\n{}'.format(is_owner, essence, is_content_zan, data['content']['nickname'], data['content']['adtime'], data['content']['zan'], data['content']['content'], comment,)

        return content


    def run(self):
        while True:
            self.get_comments()
            time.sleep(120)



if __name__ == '__main__':
    s = CirclesComments()
    s.run()
