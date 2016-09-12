from astroid import MANAGER
from astroid import scoped_nodes


def pyside_transform(obj_):
    if obj_.name == 'Signal':

        for f in ["connect", "emit"]:
            obj_.locals[f] = [scoped_nodes.Function(f, None)]

    # if obj_.name == "os":
    #     print "*********************************************************"
    #     for f in ["startfile"]:
    #         obj_.locals[f] = [scoped_nodes.Class(f, None)]
    #
    # if obj_.name == "email":
    #     print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"
    #     for f in ["MIMEMultipart"]:
    #         obj_.locals[f] = [scoped_nodes.Class(f, None)]


def register(linter):
    """called when loaded by pylint --load-plugins, register our tranformation
    function here
    """
    MANAGER.register_transform(scoped_nodes.Class, pyside_transform)
