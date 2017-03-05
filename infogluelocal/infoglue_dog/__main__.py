import argparse
import time
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler
from infogluelocal.infoglue_session.InfoglueSession import InfoglueSession
from infogluelocal.utils.config import config


parser = argparse.ArgumentParser(description='Local infoglue')

parser.add_argument('--dir', help='Which directory to watch')

args = parser.parse_args()


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
    print("Will download component")
