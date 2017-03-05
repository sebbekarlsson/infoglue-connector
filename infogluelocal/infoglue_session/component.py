from bs4 import BeautifulSoup


class Component(object):

    def __init__(self, sess, component_id):
        self.component_id = component_id
        self.realname = None
        self.name = None
        self.description = None
        self.pre_template = None
        self.template = None
        self.labels = None
        self.properties = None
        self.group_names = []
        self.tasks = None
        self.model_class_name = None
        self.language = 2
        self.connected = False

        self.connect(sess, component_id)

    def connect(self, sess, component_id):
        self.sess = sess
        self.component_id = component_id

        action = '{}/ViewContent.action?contentId={}'.format(
                    self.sess.cms_url,
                    component_id
                )

        html_doc = self.sess.session.get(action).text

        self.realname = html_doc.split('contentName')[1]
        self.realname = self.realname.split('= ')[1]
        self.realname = self.realname.split(';')[0]
        self.realname = self.realname.replace('"', '')

        if html_doc:
            soup = BeautifulSoup(html_doc, 'html.parser')

        name_input = soup.select_one('input[name="Name"]')
        description_input = soup.select_one('textarea[name="Description"]')
        template_input = soup.select_one('textarea[name="Template"]')
        pre_template_input = soup.select_one('textarea[name="PreTemplate"]')
        labels_input = soup.select_one('textarea[name="ComponentLabels"]')
        properties_input = soup.select_one('textarea[name="ComponentProperties"]')
        group_names_inputs = soup.select('input[name="GroupName"]')
        task_input = soup.select_one('textarea[name="ComponentTasks"]')
        model_class_name_input = soup.select_one('input[name="ModelClassName"]')

        if name_input:
            self.name = name_input.text

        if description_input:
            self.description = description_input.text

        if template_input:
            self.template = template_input.text

        if pre_template_input:
            self.pre_template = pre_template_input.text

        if labels_input:
            self.labels = labels_input.text

        if properties_input:
            self.properties = properties_input.text

        if group_names_inputs:
            self.group_names = [
                {
                    "name": g.get("name"),
                    "value": g.get("value"),
                    "checked": g.get("checked")
                } for g in group_names_inputs
            ]

        if task_input:
            self.tasks = task_input.text

        if model_class_name_input:
            self.model_class_name = model_class_name_input.text

        self.connected = True


    def update(self):
        data = {
            'contentId': self.component_id,
            'Template': self.template,
            'PreTemplate': self.pre_template,
            'Name': self.name,
            'ComponentLabels': self.labels,
            'ComponentProperties': self.properties,
            'ModelClassName': self.model_class_name,
            'ComponentDescription': self.description,
            'languageId': self.language,
            'GroupName': [grp['value'] for grp in self.group_names if grp['checked']]
        }

        return self.sess.update_component(data)
