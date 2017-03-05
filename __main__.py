from infogluelocal.infoglue_session.InfoglueSession import InfoglueSession
from infogluelocal.infoglue_session.component import Component
from infogluelocal.utils.config import config


if __name__ == '__main__':
    sess = InfoglueSession(cms_url=config['cms_url'])

    sess.login(config['username'], config['password'])
    #sess.update_component({
    #        "Template": "Lorem Ipsum dolum bepa"
    #    })

    comp = Component(sess, 19884, 8)
    
    comp.template = 'OST!!!'

    comp.update()

    print(comp)
