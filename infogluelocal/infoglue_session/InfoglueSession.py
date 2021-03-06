# encoding=utf8  
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

from requests import Session
import string
from urllib3._collections import HTTPHeaderDict


class InfoglueSession(object):

    def __init__(self, cms_url):
        self.cms_url = cms_url
        self.session = Session()
        self.has_logged_in = False

    def login(self, username, password):
        action = '/ViewCMSTool.action'

        data = {
                'j_username': username,
                'j_password': password,
                'x': 12, # ??? from original request
                'y': 5 # same as above ? 
                }

        r = self.session.post(self.cms_url + action, data)
        
        if r.status_code == 200 or r.status_code == 302:
            self.has_logged_in = True

        return self.has_logged_in

    def update_component(self, new_data):
        action = '/UpdateContentVersion.action'

        data = {
            'languageId':1,
            'stateId':0,
            'Template':'',
            'ComponentProperties':'',
            'ComponentPropertiesEditorType6IsActive':'false',
            'ComponentPropertiesHidden':'',
            'Name':'',
            'RelatedComponents':'',
            'RelatedComponentsEditorType4IsActive':'false',
            'RelatedComponentsHidden':'',
            'Description':'',
            'Manual':'<p>No manual entered</p>',
            'ComponentTasks':'',
            'PreTemplate':'undefined83',
            'ComponentLabels':'undefined83',
            'ModelClassName':'',
            'versionValue':"<?xml version='1.0' encoding='UTF-8'?><article xmlns='x-schema:ArticleSchema.xml'><attributes><Template><![CDATA[{Template}]]></Template><ComponentProperties><![CDATA[{ComponentProperties}]]></ComponentProperties><Name><![CDATA[{Name}]]></Name><RelatedComponents><![CDATA[{RelatedComponents}]]></RelatedComponents><Description><![CDATA[{Description}]]></Description><Manual><![CDATA[{Manual}]]></Manual><GroupName><![CDATA[{GroupName}]]></GroupName><ComponentTasks><![CDATA[{ComponentTasks}]]></ComponentTasks><PreTemplate><![CDATA[{PreTemplate}]]></PreTemplate><ComponentLabels><![CDATA[{ComponentLabels}]]></ComponentLabels><ModelClassName><![CDATA[{ModelClassName}]]></ModelClassName><IGAuthorFullName><![CDATA[{IGAuthorFullName}]]></IGAuthorFullName><IGAuthorEmail><![CDATA[{IGAuthorEmail}]]></IGAuthorEmail></attributes></article>",
            'currentEditorId':1,
            #'repositoryId':8,
            'contentId':19884,
            'GroupName': []
        }

        data_ = HTTPHeaderDict()

        for k, v in new_data.items():
            if k in data:
                data[k] = v

        keys = [t[1] for t in string.Formatter().parse(data['versionValue']) if t[1] is not None]
        for k, v in data.items():
            if k in keys:
                try:
                    kr = '{' + k + '}'
                    vr = v
                    vr_ = None

                    if isinstance(vr, list):
                        vr_ = ""

                        for i, item in enumerate(vr):
                            vr_ += item 

                            if i < len(vr):
                                vr_ += ','

                    if vr_ is not None:
                        vr = vr_

                    data['versionValue'] = data['versionValue'].replace(
                            kr,
                            vr
                            )
                except KeyError:
                    pass

        for k, v in data.items():
            if isinstance(v, list):
                for value in v:
                    data_.add(k, value)
            else:
                data_.add(k, v)

        r = self.session.post(self.cms_url + action, data_)
