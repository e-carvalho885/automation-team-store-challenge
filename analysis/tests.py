from django.test import TestCase
from django.contrib.auth.models import User
import json

test_user = {"username": "testuser", "password": "testpassword"}
test_analysis = {"viscosity": 1.063838496e-05, "diameter": 0.6, "flow": 0.094635295}


class AnalysisTest(TestCase):
    def setUp(self):
        new_user = User.objects.create(username=test_user["username"])
        new_user.set_password(test_user["password"])
        new_user.save()

    def get_token(self):
        res = self.client.post(
            "/api/token/",
            data=json.dumps(
                {
                    "username": test_user["username"],
                    "password": test_user["password"],
                }
            ),
            content_type="application/json",
        )
        result = json.loads(res.content)
        self.assertTrue("access" in result)
        return result["access"]

    def test_add_analysis_unauthorized(self):
        res = self.client.post(
            "/api/analysis/",
            data=json.dumps(test_analysis),
            content_type="application/json",
        )
        self.assertEquals(res.status_code, 401)
        res = self.client.post(
            "/api/analysis/",
            data=json.dumps(test_analysis),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer WRONG TOKEN",
        )
        self.assertEquals(res.status_code, 401)

    def test_add_analysis_ok(self):
        token = self.get_token()
        res = self.client.post(
            "/api/analysis/",
            data=json.dumps(test_analysis),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEquals(res.status_code, 201)
        result = json.loads(res.content)
        self.assertEquals(result["reynolds_number"], 188771447.88225105)
        self.assertEquals(result["reynolds_number_regime"], "turbulent")
        self.assertEquals(result["viscosity"], 1.063838496e-05)
        self.assertEquals(result["diameter"], 0.6)
        self.assertEquals(result["flow"], 0.094635295)

    def test_add_analysis_wrong_data(self):
        token = self.get_token()
        res = self.client.post(
            "/api/analysis/",
            data=json.dumps(
                {"viscosity": -1.063838496e-05, "diameter": 0.6, "flow": 0.094635295}
            ),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEquals(res.status_code, 400)

        res = self.client.post(
            "/api/analysis/",
            data=json.dumps(
                {"viscosity": 1.063838496e-05, "diameter": -0.6, "flow": 0.094635295}
            ),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEquals(res.status_code, 400)

        res = self.client.post(
            "/api/analysis/",
            data=json.dumps(
                {"viscosity": 1.063838496e-05, "diameter": 0.6, "flow": -0.094635295}
            ),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEquals(res.status_code, 400)

        res = self.client.post(
            "/api/analysis/",
            data=json.dumps({"viscosity": 0.0, "diameter": 0.6, "flow": 0.094635295}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEquals(res.status_code, 400)

        res = self.client.post(
            "/api/analysis/",
            data=json.dumps(
                {"viscosity": 1.063838496e-05, "diameter": 0.0, "flow": 0.094635295}
            ),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEquals(res.status_code, 400)

        res = self.client.post(
            "/api/analysis/",
            data=json.dumps(
                {"viscosity": 1.063838496e-05, "diameter": 0.6, "flow": 0.0}
            ),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEquals(res.status_code, 400)

    def test_add_analysis_calculate(self):
        token = self.get_token()
        res = self.client.post(
            "/api/analysis/",
            data=json.dumps(
                {
                    "viscosity": 1.063838496e-05,
                    "diameter": 0.6,
                    "flow": 0.094635295,
                    "reynolds_number": 1445555,
                    "reynolds_number_regime": "some unknown regime",
                }
            ),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEquals(res.status_code, 201)
        result = json.loads(res.content)
        self.assertEquals(
            result["reynolds_number"], 188771447.88225105
        )  # should be calculated
        self.assertEquals(
            result["reynolds_number_regime"], "turbulent"
        )  # should be calculated

    def test_get_records(self):
        token = self.get_token()
        res = self.client.post(
            "/api/analysis/",
            data=json.dumps(
                {"viscosity": 1.063838496e-05, "diameter": 1, "flow": 0.094635295}
            ),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEquals(res.status_code, 201)
        id1 = json.loads(res.content)["id"]

        res = self.client.post(
            "/api/analysis/",
            data=json.dumps(
                {"viscosity": 1.063838496e-02, "diameter": 2, "flow": 0.194635295}
            ),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEquals(res.status_code, 201)
        id2 = json.loads(res.content)["id"]

        res = self.client.get(
            "/api/analysis/",
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )

        self.assertEquals(res.status_code, 200)
        result = json.loads(res.content)
        self.assertEquals(len(result), 2)  # 2 records
        self.assertTrue(result[0]["id"] == id1 or result[1]["id"] == id1)
        self.assertTrue(result[0]["id"] == id2 or result[1]["id"] == id2)

        res = self.client.get(
            f"/api/analysis/{id1}/",
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEquals(res.status_code, 200)
        result = json.loads(res.content)
        self.assertEquals(result["flow"], 0.094635295)
        self.assertEquals(result["diameter"], 1.0)
        self.assertEquals(result["viscosity"], 1.063838496e-05)
        self.assertEquals(result["reynolds_number_regime"], "turbulent")
        self.assertEquals(result["reynolds_number"], 113262868.72935063)

    def test_put_delete_records(self):
        token = self.get_token()
        res = self.client.post(
            "/api/analysis/",
            data=json.dumps(
                {"viscosity": 1.063838496e-05, "diameter": 1, "flow": 0.094635295}
            ),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEquals(res.status_code, 201)
        id = json.loads(res.content)["id"]

        res = self.client.put(
            f"/api/analysis/{id}/",
            data=json.dumps(
                {"viscosity": 1.063838496e-05, "diameter": 1, "flow": 0.294635295}
            ),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )

        self.assertEquals(res.status_code, 200)
        result = json.loads(res.content)
        self.assertEquals(result["flow"], 0.294635295)

        res = self.client.get(
            f"/api/analysis/{id}/",
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEquals(res.status_code, 200)
        result = json.loads(res.content)
        self.assertEquals(result["reynolds_number"], 352629943.623238)
        self.assertEquals(result["reynolds_number_regime"], "turbulent")
        self.assertEquals(result["viscosity"], 1.063838496e-05)
        self.assertEquals(result["diameter"], 1)
        self.assertEquals(result["flow"], 0.294635295)

        res = self.client.delete(
            f"/api/analysis/{id}/",
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEquals(res.status_code, 204)  # No contents

        res = self.client.get(
            f"/api/analysis/{id}/",
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {token}",
        )
        self.assertEquals(res.status_code, 404)  # Not found
