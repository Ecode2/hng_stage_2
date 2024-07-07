from unittest import TestCase
from fastapi.testclient import TestClient
from eezydataapi.app.application import create_application


class TestBaseEventHandler(TestCase):
    def test_startup_handler(self):
        app = create_application()
        with self.assertLogs('eezydataapi', level='INFO') as cm:

            with TestClient(app):
                pass
            self.assertEqual(cm.output,
                             ['INFO:eezydataapi:Starting up ...',
                              'INFO:eezydataapi:Shutting down ...'])
