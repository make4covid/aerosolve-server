import unittest
import testcase


class BaseTestCase(testcase):
    def _test_get_request(self, endpoint, template=None):
        response = self.client.get(endpoint)
        self.assert_200(response)
        if template:
            self.assertTemplateUsed(name=template)
        return response






if __name__ == '__main__':
    unittest.main()
