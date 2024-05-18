from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from passlib.hash import django_pbkdf2_sha256 as handler
from django.shortcuts import get_object_or_404 
from rest_framework.decorators import action
from Usable.permissions import *
from rest_framework import status
from .serializer import *
from Usable import token as _auth

# Create your views here.
def home(request):
    return render(request, 'userapi/index.html') 

# User sign-up

class UserAuthViewset(ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['POST'])
    def signup(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            password = request.data.get('password')
            hashed_password = handler.hash(password)
            serializer.validated_data['password'] = hashed_password

            serializer.save()
            return Response({"status": True, "message": "Account Created Successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"status": False,"message":serializer.errors}, status=200)
    

# User sign-in

    @action(detail=False, methods=['POST'])
    def login(self, request):
        try:
            requireFeild = ['email', 'password']
            validator = uc.requireFeildValidation(request.data, requireFeild)
            if validator['status']:
                ser = UserLoginSerializer(data=request.data)
                if ser.is_valid():
                    fetchuser = ser.validated_data["fetch_user"]
                    print(fetchuser)
                    admin_token = _auth.UserGenerateToken(fetchuser)
                    if admin_token["status"]:
                        return Response(
                            {
                                "status": True,
                                "message": "Login Successfully",
                                "token": admin_token["token"],
                                "payload": admin_token["payload"],
                            },
                            status=200,
                        )
                    return Response({"status": False,"message": f"Invalid Credentials {admin_token['message']}",},status=400,)
                return Response({"status": False, "message": "invalid credientials"}, status=400)
            return Response({"status": False, "message": str(validator['message'])}, status= status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=400)
        
class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.filter(is_deleted=False)
    serializer_class = AddProjectSerializer
    permission_classes = [UserPermission]
    @action(detail=False, methods=["POST", "PUT", "DELETE", "GET"])
    def Project(self, request):
        try:
            if request.method == "POST":
                requireFeilds = ["name", "description"]
                validator = uc.requireFeildValidation(request.data, requireFeilds)
                if validator['status']:
                    token = request.auth
                    user_instance = get_object_or_404(User, pk=token['id'])
                    rooms = Project.objects.create(user=user_instance)  # Associate room_id with Roomcards instance
                    serializer = AddProjectSerializer(rooms, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({"status": True, "message": "Product Added Successfully"}, status=status.HTTP_200_OK)
                    return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                    
            if request.method == "GET":
                token = request.auth
                project_obj = Project.objects.filter(user=token['id']).count()
                return Response({"status": True, 'your_projects': project_obj})
        
            
            if request.method == "DELETE":
                requireFeilds = ['id']
                validator = uc.requireFeildValidation(request.data , requireFeilds)
                if validator['status']:
                    fetch_project = Project.objects.filter(id = request.data['id']).first()
                    if fetch_project:
                        fetch_project.delete()
                        return Response({"status": True, "message": f"{fetch_project.name} deleted successfully"}, status= 200)
                    return Response({"status": False, "error": "id not exist"}, status= 400)
                return Response({"status": False, "error": str(validator['message'])}, status= 400)
            
            if request.method == "PUT":
                fetch_employee = Project.objects.filter(id = request.data['id']).first()
                if fetch_employee:
                    name = request.data['name']
                    description = request.data['description']
                    user = request.data['user']
                    
                    user_obj= Project.objects.filter(id=user).first()
                    fetch_employee.name = name
                    fetch_employee.description = description
                    fetch_employee.user = user_obj
                  

                    fetch_employee.save()
                    return Response({"status": True, "message": f"{fetch_employee.name} Updated Successfully"}, status= 200)
                return Response({"status": False, "error": "id not exist"}, status= 400)
            return Response({"status": False, "error": validator['message']}, status= 400)

        except Exception as e:
            return Response({"status": False, "error": str(e)}, status= 400)

            
    @action(detail=False, methods=['GET'])
    def Get_Project(self, request):
        project_id = request.GET.get('id')
        
        fetch_project = Project.objects.filter(id=project_id).values()
        
        if fetch_project:
            return Response({"status": True, 'Project': fetch_project})

        
        return Response({"status": False, "error": "id not exist"}, status=400)


    @action(detail=True, methods=['POST'])
    def add_user(self, request, pk=None):
        requireFeilds = ['contributor_users']
        validator = uc.requireFeildValidation(request.data , requireFeilds)
        if validator['status']:
            project = self.get_object()
            serializer = AddUserSerializer(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": True, "message": "User added successfully"}, status=status.HTTP_200_OK)
            return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": False, "error": str(validator['message'])}, status= 400)
    
    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        project.is_deleted = True
        project.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=False, methods=["POST", "PUT", "DELETE", "GET"])
    def Task(self, request):
        try:
            if request.method == "POST":
                requireFeilds = ["project", "title", "description", "status","due_date"]
                validator = uc.requireFeildValidation(request.data, requireFeilds)
                if validator['status']:
                    serializer = AddTaskSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({"status": True, "message": "Task Added Successfully"}, status=status.HTTP_200_OK)
                    return Response({"status": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                    
            if request.method == "GET":
                token = request.auth
                project_obj = Task.objects.filter(user=token['id']).count()
                return Response({"status": True, 'your_Tasks': project_obj})
        
            
            if request.method == "DELETE":
                requireFeilds = ['id']
                validator = uc.requireFeildValidation(request.data , requireFeilds)
                if validator['status']:
                    fetch_task = Task.objects.filter(id = request.data['id']).first()
                    if fetch_task:
                        fetch_task.delete()
                        return Response({"status": True, "message": f"{fetch_task.title} deleted successfully"}, status= 200)
                    return Response({"status": False, "error": "id not exist"}, status= 400)
                return Response({"status": False, "error": str(validator['message'])}, status= 400)
            
            if request.method == "PUT":
                fetch_Task = Task.objects.filter(id = request.data['id']).first()
                if fetch_Task:
                    title = request.data['title']
                    description = request.data['description']
                    status = request.data['status']
                    due_date = request.data['due_date']
                    project = request.data['project']
                    
                    project_obj= Task.objects.filter(id=project).first()
                    fetch_Task.title = title
                    fetch_Task.description = description
                    fetch_Task.status=status
                    fetch_Task.due_date=due_date
                    fetch_Task.project = project_obj
                  

                    fetch_Task.save()
                    return Response({"status": True, "message": f"{fetch_Task.title} Updated Successfully"}, status= 200)
                return Response({"status": False, "error": "id not exist"}, status= 400)
            return Response({"status": False, "error": validator['message']}, status= 400)

        except Exception as e:
            return Response({"status": False, "error": str(e)}, status= 400)

        

    @action(detail=False, methods=['GET'])
    def Get_Task(self, request):
        task_id = request.GET.get('id')
        
        fetch_task = Task.objects.filter(id=task_id).values()
        
        if fetch_task:
            return Response({"status": True, 'Task': fetch_task})

        
        return Response({"status": False, "error": "id not exist"}, status=400)


