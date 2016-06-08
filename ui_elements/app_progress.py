"""
An Application level global progress and status bar for display in the UI
"""


class AppProgress(object):
    """
    An Application level global progress bar
    """
    progress = None
    status = None

    def __init__(self, progress, status):
        """
        @param progress: QtGui.QProgressBar
        @param status: QtGui.QText
        """
        if AppProgress.progress is None:
            AppProgress.progress = progress
            AppProgress.status = status

    @staticmethod
    def setProgressBar(currentProgress, status):
        """
        Set the progress bar status
        @param currentProgress: int
        @param status: str
        @return: None
        """
        if AppProgress.progress:
            if status is not None:
                AppProgress.progress.show()
                AppProgress.status.show()
                currentProgress = int(currentProgress)
                AppProgress.progress.setValue(currentProgress)
                AppProgress.status.setText(str(status))
            else:
                AppProgress.progress.hide()
                AppProgress.status.hide()

    @staticmethod
    def enable():
        """
        enable display of the status bar
        """
        if AppProgress.progress:
            AppProgress.progress.show()
            AppProgress.status.show()

    @staticmethod
    def disable():
        """
        disable display of the statusbar
        """

        if AppProgress.progress:
            AppProgress.progress.hide()
            AppProgress.status.hide()
