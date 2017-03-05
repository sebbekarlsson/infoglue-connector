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

def push(filename):
    sess.update_component({
            "Template": "Lorem Ipsum"
        })

class MyHandler(PatternMatchingEventHandler):
    patterns = [
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
    
    print("Will download component")
