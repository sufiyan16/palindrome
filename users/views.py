from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from .forms import CustomUserCreationForm, ProfileForm
from django.contrib.auth.decorators import login_required
from .models import Profile
# Create your views here.
def loginUser(request):
    page='login'

    if request.user.is_authenticated:
        return redirect('palindrome')


    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"username doesn't match ")
            
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'User logged in successfully')
            return redirect('palindrome')
            
        else:
            messages.error(request,"username or pass doesn't match ")


    return render(request,'users/login.html')

def logoutUser(request):
    logout(request)
    messages.info(request,"You're logged out successfully ")
    return redirect('palindrome')


def registerUser(request):
    page='register'
    form=CustomUserCreationForm() 
    if request.method =='POST':
        
        form=CustomUserCreationForm(request.POST)   

        if form.is_valid():
            user=form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request,'User account was created! ')

            login(request,user)
            return redirect('login')
        else:
            
            messages.success(request,'An error occured during registration')

    context={'page':page,'form':form}
    return render(request,'users/register.html',context)

@login_required(login_url='login')  
def userAccount(request):
    
    profile=request.user.profile
    pal=profile.palindrome_set.all()
    
    context={'profile':profile,'pal':pal}
    return render(request,'users/account.html',context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/edit-account.html', context)


@login_required(login_url='login')
def deleteUser(request,pk):
    profile=Profile.objects.get(id=pk)

    if request.method=='POST':
        profile.delete()
        messages.success(request,'User has been deleted succesfully')
        return redirect('palindrome')


    context = {'profile': profile}
    return render(request,'users/delete-user.html',context)