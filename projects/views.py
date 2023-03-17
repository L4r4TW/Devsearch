from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Project, Tag 
from .forms import ProjectForm  
from .utils import searchProjects

# projectsList = [
#     {
#         'id': '1',
#         'title': 'Ecommerce Website',
#         'description': 'Fully functional ecommerce website'
#     },
#     {
#         'id': '2',
#         'title': 'Portfolio Website',
#         'description': 'A personal website to write articles and display work'
#     },
#     {
#         'id': '3',
#         'title': 'Social Network',
#         'description': 'An open source project built by the community'
#     }
# ]

# Create your views here.



def projects(request):

    projects, search_query = searchProjects(request)

    page = request.GET.get('page')
    results = 3
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    
    context = {'projects' : projects, 'search_query' : search_query}
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    # projectObj = None
    # for i in projectsList:
    #     if i['id'] == pk:
            # projectObj = i
    projectObj = Project.objects.get(id=pk)
   
    return render(request, 'projects/single-project.html', {'project' : projectObj})

@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    # profile = profile.project_set.get(id=pk)
    form = ProjectForm()
    
    if request.method == 'POST':
        print("rak egye a beled!")
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {'form' : form}
    return render(request, "projects/project_form.html", context)

@login_required(login_url="login")
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        # print(request.POST)
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form' : form}
    return render(request, "projects/project_form.html", context)
    
@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id = pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object' : project}
    return render(request, 'delete_template.html', context)