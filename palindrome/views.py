from django.shortcuts import redirect, render
from .models import Palindrome
from .forms import PalindromeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def Palindrom(request):
    pal=Palindrome.objects.all()
    context={'pal':pal}
    return render(request,'pal.html',context)

@login_required(login_url='login')
def CreatePal(request):
    profile=request.user.profile
    form = PalindromeForm()
    
    if request.method=='POST':
        form=PalindromeForm(request.POST)
        if form.is_valid():
           a=form.save(commit=False)
           a.owner=profile
           b=a.input[::-1]
           if a.input==b:
                print(a.input,'True')
                a.save()
                messages.success(request,'You won the game')
                
           else:
                
                print(a.input,'False')
                print('a is not equal to b')
                messages.error(request,'You lose the game')
                return redirect('palindrome')

        return redirect('palindrome')
        
    return render(request,'create-pal.html',{'form':form})

@login_required(login_url='login')
def UpdatePal(request,pk):
    profile=request.user.profile
    pal=profile.palindrome_set.get(id=pk)
    form=PalindromeForm(instance=pal)
    if request.method=='POST':
        form=PalindromeForm(request.POST,instance=pal)
        form.owner=request.user.profile
        
        if form.is_valid():
            a=form.save(commit=False)
            b=a.input[::-1]
            
            if a.input==b:
                print(a.input,'True')
                a.save()
                messages.success(request,'You won the game')

            else:
                
                print(a.input,'False')
                print('a is not equal to b')
                messages.error(request,'You lose the game')
                return redirect('palindrome')
                
            return redirect('palindrome')

    return render(request,'create-pal.html',{'form':form})

@login_required(login_url='login')
def DeletePal(request,pk):
   
    pal=Palindrome.objects.get(id=pk)
    if request.method=='POST':
        pal.delete()
        return redirect('palindrome')
    context={'object':pal}
    return render(request,'delete.html',context)