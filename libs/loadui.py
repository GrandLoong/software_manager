import pysideuic
import xml.etree.ElementTree as xml
from PySide import QtGui

from cStringIO import StringIO


def load_ui_type(ui_file):

    """
    Pyside lacks the "load_ui_type" command, so we have to convert the ui file to py code in-memory first
    and then execute it in a special frame to retrieve the form_class.
    """
    parsed = xml.parse(ui_file)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(ui_file, 'r') as f:
        o = StringIO()
        frame = {}

        pysideuic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        # Fetch the base_class and form class based on their type in the xml from designer
        form_class = frame['Ui_%s' % form_class]
        base_class = getattr(QtGui, widget_class)

    return form_class, base_class


def load_style_sheet(styleFile):
    f = open(styleFile, 'r')
    data = f.read()
    data.strip('\n')

    return data
