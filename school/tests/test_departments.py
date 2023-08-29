import pytest
from rest_framework import status
from model_bakery import baker
from school import models


@pytest.fixture
def get_obj(api_client):
    def do_get_obj(obj):
        return api_client.get(f'/school/departments/{obj}/')
    return do_get_obj

@pytest.fixture
def delete_department(api_client):
    def do_get_obj(obj):
        return api_client.delete(f'/school/departments/{obj}/')
    return do_get_obj
    

@pytest.mark.django_db
class TestCreateDepartment:
    def test_if_user_is_anonymous_returns_401(self, get_obj):
        department = baker.make(models.Department)
        response = get_obj(department.id)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_if_user_has_permission_return_200(self, authenticate_superuser, get_obj):
        authenticate_superuser(is_superuser=True)
        department = baker.make(models.Department)
        response = get_obj(department.id)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] > 0
        assert response.data['name'] == department.name

    def test_delete_department_containing_employee_return_405(self, authenticate_superuser, delete_department):
        authenticate_superuser(is_superuser=True)
        department = baker.make(models.Department)
        baker.make(models.Employee, department=department)
        response = delete_department(department.id)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_delete_department_containing_teacher_return_405(self, authenticate_superuser, delete_department):
        authenticate_superuser(is_superuser=True)
        department = baker.make(models.Department)
        baker.make(models.Teacher, department=department)
        response = delete_department(department.id)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_delete_department_containing_student_return_405(self, authenticate_superuser, delete_department):
        authenticate_superuser(is_superuser=True)
        department = baker.make(models.Department)
        baker.make(models.Student, department=department)
        response = delete_department(department.id)
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_create_department_with_duplicate_name_returns_400(self, authenticate_superuser, api_client):
        authenticate_superuser(is_superuser=True)
        baker.make(models.Department, name='Human')
        department_with_duplicate_name = baker.prepare(models.Department, name='Human')
        department_data = {
            'name': department_with_duplicate_name.name,
            'budget': department_with_duplicate_name.budget,
            'duty': department_with_duplicate_name.duty
        }
        response = api_client.post('/school/departments/', department_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

        #def test_if_user_is_not_admin_returns_403
        #def test_if_data_is_invalid_returns_400
        #def test_if_data_is_valid_returns_201
        #def test_if_collection_exists_return_200
     
       
