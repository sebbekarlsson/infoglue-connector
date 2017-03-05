import argparse
import time
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler
from infogluelocal.infoglue_session.InfoglueSession import InfoglueSession
from infogluelocal.infoglue_session.component import Component
from infogluelocal.utils.config import config
import os
import json
import shutil


sess = InfoglueSession(cms_url=config['cms_url'])
sess.login(config['username'], config['password'])

_patterns = [
    "*.html",
    "*.php",
    "*.js",
    "*.css",
    "*.json",
    "*.jsp",
    "*.jspx",
    "*.java",
    "*.txt",
    "*.ini",
    "*.sql"
]

def push(filename):
    print("pushing")
    print(filename)
    comp_config = None

    comp_name = filename.split('components/')[1]
    comp_name = comp_name.split('/')[0]
    
    if 'component.json' in filename:
        json_path = filename
    elif 'components' in filename:
        json_path = filename.split(comp_name)[0] + comp_name + '/component.json'
    
    if os.path.isfile(json_path):
        with open(json_path) as conf_file:
            comp_config = json.loads(conf_file.read())
        conf_file.close()

    if comp_config:
        comp = Component(sess, comp_config['component_id'])

        for k, v in comp_config.items():
            if 'component.json' in filename:
                for _f in _patterns:
                    f = _f.replace('*', '')
                    file_path = filename.replace('component.json', '') + '/' + k + f
                    
                    if os.path.isfile(file_path):
                        break

            elif 'components' in filename:
                for _f in _patterns:
                    f = _f.replace('*', '')
                    file_path = filename.split(comp_name)[0] + comp_name + '/{}{}'.format(k, f)

                    if os.path.isfile(file_path):
                        break
            
            if os.path.isfile(file_path):
                with open(file_path) as file_file:
                    setattr(comp, k, file_file.read())
                file_file.close()
            else:
                setattr(comp, k, v)
    
    return comp.update()

class MyHandler(PatternMatchingEventHandler):
    
    patterns = _patterns

    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        print(event.src_path, event.event_type)  # print now only for degug
        
        if event.event_type not in ['moved', 'deleted']:
            # Push the modified file to the server
            push(event.src_path)
                
        print('WATCHING FOR CHANGES...')

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

def watch():
    parser = argparse.ArgumentParser(description='Infoglue')
    parser.add_argument('--dir', help='Which directory to watch')
    args = parser.parse_args()

    dir = args.dir

    print('WATCHING FOR CHANGES...')
    observer = Observer()
    observer.schedule(MyHandler(), path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        quit()

    observer.join()

def get():
    parser = argparse.ArgumentParser(description='Infoglue')
    parser.add_argument('--id', help='Which directory to download component to')
    parser.add_argument('--dir', help='Which directory to download component to')
    args = parser.parse_args()

    out_dir = args.dir if args.dir else '.'
    
    print('Downloading component...')
    comp = Component(sess, component_id=args.id)
    
    final_dir = out_dir + '/' + comp.realname.replace(' ', '_')

    if os.path.isdir(final_dir):
        shutil.rmtree(final_dir)

    os.makedirs(final_dir)

    with open('{}/{}'.format(final_dir, 'component.json'), 'w+') as component_file:
        dot = {}

        for k, v in comp.__dict__.items():
            try:
                json.dumps(v)
                dot[k] = v
            except:
                pass

        component_file.write(json.dumps(dot, sort_keys=True,indent=4, separators=(',', ': ')))

    component_file.close()
    
    print("Component \"{}\" was downloaded: {}".format(comp.realname, final_dir))
