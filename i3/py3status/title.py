# -*- coding: utf-8 -*-

"""
"""


from subprocess import Popen, PIPE
from time import time, sleep
import json


class Py3status:
    """
    """
    cache_timeout = 1.0
    color = None

    def __init__(self):
        self.full_text = u''
        self._perform = False

    def __get_active_workspace(self):
        """
        """
        workspace = None

        # ipc message get_workspaces
        with Popen(['i3-msg', '-t', 'get_workspaces'], stdout=PIPE) as p:
            workspaces = json.loads(p.stdout.read().decode('utf-8'))
        # ipc message get_tree
        with Popen(['i3-msg', '-t', 'get_tree'], stdout=PIPE) as p:
            tree = json.loads(p.stdout.read().decode('utf-8'))

        for w in workspaces:
            if w['visible'] is True and w['focused'] is True:
                for output in tree['nodes']:
                    if output['name'] == w['output']:
                        workspace = output['nodes'][1]['nodes']
                        break
                break

        return workspace

    def __get_active_window_title(self, tree=None):
        """
        """
        if tree is None:
            tree = self.__get_active_workspace()
            self._perform = True
            self.full_text = u''

        if isinstance(tree, list):
            tree = {'list': tree}

        if 'focused' in tree:
            if tree['focused'] == True:
                if 'name' in tree and 'title_format' in tree:
                    self.full_text = tree['title_format'].replace('%title', tree['name'])
                    self._perform = False


        if self._perform is True:
            for nodes in ['nodes', 'floating_nodes', 'list']:
                if nodes in tree:
                    for node in tree[nodes]:
                        self.__get_active_window_title(node)


    def title(self, i3s_output_list, i3s_config):
        try:
            # title
            self.__get_active_window_title()
            #old_full_text = self.full_text
            #while self.full_text == old_full_text :
            #    self.__get_active_window_title()
            #    sleep(self.cache_timeout)
        except Exception as e:
            self.full_text = u"#ERR {}".format(e)
            self.color = i3s_config["color_bad"]
        finally:
            response = {
                'cached_until': time() + self.cache_timeout,
                'full_text': self.full_text,
                'color': self.color
            }
            return response


if __name__ == "__main__":
    i3s = Py3status()

    while True:
        print(i3s.title([], {}))
        sleep(2)
