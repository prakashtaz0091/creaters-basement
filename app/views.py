from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.models import Group
from . models import AudioFile, Cart, OriginalAudio, YoutubeLink, Description, ContactMessage, UserFile, RequestForDemo, PhotoGallery
from asgiref.sync import sync_to_async
import asyncio
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import VerifyUser

# video gallery
def videoGallery(request):
    return render(request, 'videoGallery.html')


# viewing demo requests
def viewDemoRequest(request):

    request_messages = RequestForDemo.objects.all()

    if request.method == "POST":
        message_id = request.POST.get('message_id')
        message_to_be_deleted = RequestForDemo.objects.get(pk=message_id)
        message_to_be_deleted.delete()

        messages.success(request, "Message deleted successfully !")
        return redirect('viewDemoRequest')

    context = {
        'user': request.user,
        'request_messages': reversed(request_messages),
        'no_of_messages': request_messages.count(),

    }

    return render(request, 'demoRequest.html', context)


# request a demo
@login_required(login_url='loginPage')
def requestDemo(request, pk):
    demoFile = UserFile.objects.get(pk=pk)

    request_message = f'Hello Sir, Please provide me a demo of " {demoFile.finalProduct} " final product.'
    messages.success(
        request, f"request for demo of {demoFile.finalProduct} sent.")
    RequestForDemo.objects.create(
        user=request.user,
        message=request_message,
    )

    return redirect('getFinalProduct')

#  ends

# setting price of file in commpleted projects page


@login_required(login_url='loginPage')
@allowed_users(allowed_roles='admin')
def setPriceCompleted(request, pk):

    if request.method == "POST":
        actual_price = float(request.POST.get('actual_price'))
        service_charge = float(request.POST.get('service_charge'))
        tax_amount = percentage(actual_price)

        total_price = actual_price + service_charge + tax_amount

        userFile = UserFile.objects.get(pk=pk)
        userFile.actual_price = actual_price
        userFile.service_charge = service_charge
        userFile.tax_amount = tax_amount
        userFile.total_price = total_price
        userFile.save()

        return redirect('viewCompletedProjects')

    else:
        context = {
            'file': UserFile.objects.get(pk=pk),
        }

        return render(request, 'setPriceCompleted.html', context)


# view completed projects
@login_required(login_url='loginPage')
@allowed_users(allowed_roles='admin')
def viewCompletedProjects(request):

    userFiles = UserFile.objects.all()
    audios = []
    videos = []
    for f in userFiles:
        if f.rawFile.name.endswith(('.mp4', '.webm', '.mkv', '.flv', '.vob', '.ogg', '.ogv', '.avi', '.mov', '.wmv', '.m4p', '.m4v', '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.nsv', '.flv', '.f4v')):
            videos.append(f)
        else:
            audios.append(f)

    context = {
        'audios': reversed(audios),
        'videos': reversed(videos),
    }

    return render(request, 'completedProjects.html', context)


# inform Customer that project has been completed
@login_required(login_url='loginPage')
@allowed_users(allowed_roles='admin')
def informCustomer(request, pk):
    userFile = UserFile.objects.get(pk=pk)

    userEmail = userFile.user.email
    print(f"sending mail to ....{userFile.user.email}")
    heading = "Creater's Basement >> Project Completed"
    message_to_user = f"Dear, Customer. We have completed your {userFile.rawFile.name} project. Go to : http://127.0.0.1:8000/get-final-product/ for futher info. "
    send_mail(heading, message_to_user, settings.EMAIL_HOST_USER,
              [userEmail], fail_silently=False)
    print("mail sent")
    messages.success(request, f'{userEmail} was informed successfully !')
    return redirect('viewUserUploadedContents')


# upload final product-- only admin
def uploadFinalProduct(request, pk):
    if request.method == "POST":
        finalFile = request.FILES.get('file')
        userFile = UserFile.objects.get(pk=pk)

        userFile.finalProduct = finalFile
        userFile.save()
        print("final file uploaded")
        return redirect('viewUserUploadedContents')

    else:
        userFile = UserFile.objects.get(pk=pk)

        context = {
            'file': userFile,
        }
        return render(request, 'uploadFinalProduct.html', context)


# view user uploaded contents to admin
@login_required(login_url='loginPage')
@allowed_users(allowed_roles='admin')
def viewUserUploadedContents(request):
    files = UserFile.objects.all()
    audios = []
    videos = []
    for file in files:
        if file.rawFile.name.endswith(('.mp4', '.webm', '.mkv', '.flv', '.vob', '.ogg', '.ogv', '.avi', '.mov', '.wmv', '.m4p', '.m4v', '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.nsv', '.flv', '.f4v')):
            videos.append(file)
        else:
            audios.append(file)

    context = {
        'audios': reversed(audios),
        'videos': reversed(videos),
    }

    return render(request, 'userUploadedContent.html', context)


# giving final product to user
@login_required(login_url='loginPage')
def getFinalProduct(request):

    userFile = UserFile.objects.filter(user=request.user)
    user = request.user.username
    audios = []
    videos = []
    for f in userFile:
        if f.rawFile.name.endswith(('.mp4', '.webm', '.mkv', '.flv', '.vob', '.ogg', '.ogv', '.avi', '.mov', '.wmv', '.m4p', '.m4v', '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.nsv', '.flv', '.f4v')):
            videos.append(f)
        else:
            audios.append(f)

    context = {
        'user': user,
        'audios': reversed(audios),
        'videos': reversed(videos),
    }

    return render(request, 'getFinalProduct.html', context)

# deleting user files


def deleteUserFile(request, pk):
    if request.method == "POST":
        userfile = UserFile.objects.get(pk=pk)
        userfile.deleteRawFile()
        return redirect('uploadContentUser')

# uploading contents by users

@login_required(login_url='loginPage')
def uploadContentUser(request):
    if request.method == "POST":
        files = request.FILES.getlist('files')
        count = 0
        for file in files:
            print(f"{file} uploading.......")

            UserFile.objects.create(
                user=request.user,
                rawFile=file
            )

            print("uploaded succesfully")
            count += 1

        messages.success(request, 'uploaded successfully !')
        return redirect(uploadContentUser)

    files = UserFile.objects.filter(user=request.user)
    audios = []
    videos = []
    for file in files:
        if file.rawFile.name.endswith(('.mp4', '.webm', '.mkv', '.flv', '.vob', '.ogg', '.ogv', '.avi', '.mov', '.wmv', '.m4p', '.m4v', '.mpg', '.mp2', '.mpeg', '.mpe', '.mpv', '.nsv', '.flv', 'f4v')):
            videos.append(file)
        else:
            audios.append(file)

    context = {
        'audios': reversed(audios),
        'videos': reversed(videos),
    }

    return render(request, 'uploadContentUser.html', context)


# delete messages
def deleteMessage(request, pk):
    message = ContactMessage.objects.get(pk=pk)
    message.delete()

    return redirect('viewMessages')
# ends


# replying message
async def replyMessage(request):
    if request.method == "POST":
        email = request.POST.get('email')
        reply = request.POST.get('reply')

        heading = f"Creaters Basement "
        message = reply

        try:
            loop = asyncio.get_event_loop()
            task = loop.create_task(mail(heading, message, [email]))
        except:
            pass
        finally:
            loop.run_until_complete(task)
            loop.close()

        # asyncio.run(mail(heading,message,[email]))

        return redirect('home')


# viewing messages
def viewMessages(request):
    messages = ContactMessage.objects.all()

    context = {
        'message': reversed(messages),
        'no_of_messages': len(messages),
    }

    return render(request, 'viewMessage.html', context)
# ends


# mail function
@sync_to_async
def mail(heading, message_to_user, emails, name, message_from_user):
    print(f'sending mail .......from {settings.EMAIL_HOST_USER}')
    print(emails)
    send_mail(heading, message_to_user, settings.EMAIL_HOST_USER,
              emails, fail_silently=False)
    print('mail sent successfully...........')

    ContactMessage.objects.create(
        name=name,
        email=emails,
        message=message_from_user,
    )
    print("message saved")


# contactUs handling
async def contactUs(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_from_user = request.POST.get('message')

        # loop = asyncio.get_event_loop()

        first_name = name.split(" ", 1)[0]

        heading = f"Creaters Basement "
        message_to_user = f"Hello {first_name}, Thank you for contacting us. We will reach you soon"

        task1 = asyncio.create_task(
            mail(heading, message_to_user, [email], name, message_from_user))

        return redirect('home')


# ends


# edit description texts
def edit(request, label):
    desc = Description.objects.get(label=label)

    if request.method == "POST":

        desc.desc = request.POST.get('desc')
        desc.save()
        return redirect('home')

    else:
        context = {
            'desc': desc,
        }

        return render(request, 'edit.html', context)
# ends


# adding youtube videos link
def addYoutubeLink(request):
    if request.method == "POST":
        full_link = request.POST.get('link')
        link_id = full_link.replace("https://youtu.be/", "")

        YoutubeLink.objects.create(
            link_id=link_id,
        )

        return redirect('home')
# ends

# remove ytlink


def removeYtLink(request, pk):
    if request.method == "POST":
        toRemoveLink = YoutubeLink.objects.get(pk=pk)
        toRemoveLink.delete()

        return redirect('home')
# ends


# this is index page, at first user is redirected here
# @login_required(login_url='loginPage')
def home(request):
    latest_six_audios = AudioFile.objects.order_by('-id')[:3]
    youtubeLinks = YoutubeLink.objects.all()

    descriptions = Description.objects.all()

    if request.user.is_authenticated:
        logged_in = True

        admin = request.user.is_staff
        if admin:
            admin = True

        context = {
            'admin': admin,
            'logged_in': logged_in,
            'audios': latest_six_audios,
            'youtubeLinks': reversed(youtubeLinks),
            'descriptions': descriptions,

        }
        return render(request, 'index.html', context)

    context = {
        'audios': latest_six_audios,
        'youtubeLinks': reversed(youtubeLinks),
        'descriptions': descriptions,
    }

    return render(request, 'index.html', context)


# index ends here


# validate email
def validateEmail(request):

    if request.method == "POST":
        otp = request.session['otp']
        user = User.objects.get(email=request.POST.get('gmail'))
        verifyuser = user.verifyuser

        if request.POST.get('otp') == str(otp):
            verifyuser.verified = True
            verifyuser.save()
            messages.success(request, f"{user.username}, Thanks for verifying your gmail. you can login now")
            return redirect('loginPage')
        else:
            invalid_input = verifyuser.count
            if invalid_input >=3:
                user.delete()
                messages.success(request, f"{user.username}'s account has been deleted due to unverified gmail")
                return redirect('registerPage')
            else:
                verifyuser.count += 1
                verifyuser.save()

                messages.error(request, f"Invalid OTP for {invalid_input + 1} times. If you entered invalid OTP more than 3 times, your account will be deleted")
                return redirect('validateEmail')
            
    else:

        gmail = request.session['gmail']
        context = {
            'gmail': gmail,
        }

        return render(request, 'validateEmail.html', context)


# if user is not logged in
@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        username = request.POST.get('username')
        gmail = request.POST.get('email')
        if gmail[-10:] == "@gmail.com":

            if len(User.objects.filter(email=gmail)) > 0:
                messages.warning(request, f"Account with {gmail} aready exists !")
                return redirect('registerPage')   
            else:

                if form.is_valid():
                    user = form.save()

                    VerifyUser.objects.create(
                        user=user,

                    )

                    group = Group.objects.get(name='customer')
                    user.groups.add(group)

                    messages.success(
                        request, f"Account successfully created for {username}")

                    import random
                    otp = random.randint(000000, 999999)
                    heading = "Gmail Verification"
                    message_to_user = f"Hello, {username}. Please enter this OTP  {otp}  in gmail validation page.  "
                    send_mail(heading, message_to_user, settings.EMAIL_HOST_USER, [
                            gmail], fail_silently=False)
                    
                    request.session['otp'] = otp
                    request.session['gmail'] = gmail
                    return redirect('validateEmail')

        else:
            messages.error(request, f"We only accept gmail account !")
            return redirect('registerPage')

    context = {
        'form': form,
    }
    return render(request, 'registerPage.html', context)

# register function ends here


#resend otp 
def resendOtp(request,gmail):

    if request.method == "POST":
        import random
        otp = random.randint(000000, 999999)
        heading = "Gmail Verification"
        username = User.objects.get(email=gmail).username
        message_to_user = f"Hello, {username}. Please enter this OTP  {otp}  in gmail validation page.  "
        send_mail(heading, message_to_user, settings.EMAIL_HOST_USER, [gmail], fail_silently=False)
        request.session['otp'] = otp

        messages.success(request, "OTP sent")
        return redirect('validateEmail')


# login function
@unauthenticated_user
def loginPage(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:

            from .models import VerifyUser
            if user.verifyuser.verified:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, "You haven't verified your gmail yet. Please verify it and go forward.  ")
           
                return redirect('validateEmail')

        else:
            messages.info(
                request, 'Username or Password is Incorrect ! Please try again')
            return redirect('loginPage')

    return render(request, 'loginPage.html')

# login functions ends here


# logout user function
def logoutUser(request):
    logout(request)
    return redirect('home')

# logout user function ends here

# when user enters tracks in nav


def tracks(request):

    return render(request, 'tracks.html')
# ends


# redirecting user to newmusic page

def newMusic(request):

    audios = AudioFile.objects.all()
    context = {
        'audios': audios,
    }
    return render(request, 'newmusic.html', context)
# ends


# for demo files uploading
def upload(file):
    AudioFile.objects.create(
        file=file,
    )


def uploadContent(request):

    if request.method == "POST":
        files = request.FILES.getlist('files')
        count = 0
        for file in files:
            print(f"{file} uploading.......")
            upload(file)
            print("uploaded succesfully")
            count += 1

        messages.success(request, f'{count} Audios uploaded successfully !')
        return redirect(uploadContent)

    audios = AudioFile.objects.all()
    context = {
        'audios': reversed(audios),
    }

    return render(request, 'upload.html', context)

# demo files uploading ends here


# viewing original files
def viewOriginal(request):
    original_audios = OriginalAudio.objects.all()

    context = {
        'audios': reversed(original_audios),
    }

    return render(request, 'viewOriginal.html', context)
# ends


# uploading original files
def uploadOriginal(request, pk):

    if request.method == "POST":
        originalFile = request.FILES.get('file')

        demoAudio = AudioFile.objects.get(pk=pk)

        OriginalAudio.objects.create(
            audioFile=demoAudio,
            originalFile=originalFile,
        )

        messages.success(
            request, f'Original Audio of {demoAudio.file.name[:50]} uploaded successfully !')
        return redirect('viewOriginal')

    else:
        original_audios = OriginalAudio.objects.all()

        context = {
            'audios': reversed(original_audios),
        }

        return render(request, 'uploadOriginal.html', context)

# ends


# calculating percentage i.e tax 13%
def percentage(price):
    percentage = float(13)/float(100) * float(price)
    return float(percentage)
# ends


# setting price of audio in upload page
@login_required(login_url='loginPage')
@allowed_users(allowed_roles='admin')
def setPrice(request, pk):

    if request.method == "POST":
        actual_price = float(request.POST.get('actual_price'))
        service_charge = float(request.POST.get('service_charge'))
        tax_amount = percentage(actual_price)

        total_price = actual_price + service_charge + tax_amount

        audio = AudioFile.objects.get(pk=pk)
        audio.actual_price = actual_price
        audio.service_charge = service_charge
        audio.tax_amount = tax_amount
        audio.total_price = total_price
        audio.save()

        return redirect('uploadContent')

    else:
        context = {
            'audio': AudioFile.objects.get(pk=pk),
        }

        return render(request, 'setPrice.html', context)

# setting price ends


# deleting files
def delete(request, pk):
    demoAudio = AudioFile.objects.get(pk=pk)
    copy = demoAudio

    original_exist = request.POST.get('org_exist')
    if original_exist == "True":
        originalAudio = OriginalAudio.objects.get(audioFile=demoAudio)
        originalAudio.delete()

    demoAudio.delete()
    audio_name = str(copy.file)
    messages.success(request, f"{audio_name} deleted successfully !")
    print(f"{audio_name} deleted successfully")

    return redirect(uploadContent)
# deleting functions ends here

# _____________________________________________________________________________
# memories
# _____________________________________________________________________________

# removing memories


def removeMemories(request, pk):
    image = PhotoGallery.objects.get(pk=pk)
    image.delete()
    print('deleted')
    return redirect('memories')


# viewing memories
def memories(request):
    images = PhotoGallery.objects.all()
    print(len(images))
    admin = False
    if request.user.is_staff:
        admin = True

    if request.method == "POST":
        images = request.FILES.getlist('image')
        for i in images:
            PhotoGallery.objects.create(
                image=i,
            )
        print('image uploaded')
        return redirect('memories')

    context = {
        'images': reversed(images),
        'admin': admin,
    }
    return render(request, 'photogallery.html', context)
# viewing memories ends

# _____________________________________________________________________________
# _____________________________________________________________________________


# redirecting user to buying page
def getOurMusic(request):

    audios = AudioFile.objects.all()

    priced_audios = []
    for audio in audios:
        if audio.total_price != 0:
            priced_audios.append(audio)

    latest_audios = reversed(priced_audios)

    context = {
        'audios': latest_audios,
    }

    return render(request, 'getmusic.html', context)
# ends


# esewa verification function
def esewaVerify(request):

    import requests

    oid = request.GET.get('oid')
    amt = request.GET.get('amt')
    refId = request.GET.get('refId')
    print(oid, amt, refId)

    url = "https://uat.esewa.com.np/epay/transrec"
    d = {
        'amt': amt,
        'scd': 'EPAYTEST',
        'rid': refId,
        'pid': oid,
    }
    resp = requests.post(url, d)

    import xml.etree.ElementTree as ET
    root = ET.fromstring(resp.content)
    status = root[0].text.strip()

    print(status)

    if status == "Success":
        print("payment done successfully")

        if request.session['buyFromStore']:
            print(request.session['store_item_id'])
            add_to_cart_item = AudioFile.objects.get(
                pk=request.session['store_item_id'])
            add_file = add_to_cart_item.originalaudio.originalFile
            print(add_file)
            Cart.objects.create(
                user=request.user,
                downloadable_file=add_file,
            )
            add_to_cart_item.delete()

        if request.session['buyFromProjects']:
            print(request.session['project_item_id'])
            add_to_cart_item = UserFile.objects.get(
                pk=request.session['project_item_id'])
            add_file = add_to_cart_item.finalProduct

            print(add_file)
            Cart.objects.create(
                user=request.user,
                downloadable_file=add_file,
            )
            add_to_cart_item.deleteRawFile()
            add_to_cart_item.deleteFinalProduct()
            add_to_cart_item.delete()

        return redirect('cart')
    else:
        print("payment error")
        return redirect('esewaRequest')
# verification ends here

# esewa payment handling function ends here


# handling the buy request
def buy(request, item, pk):
    import random

    item_id = item.id

    if item_id == pk:
        trying_to_buy = item
        random_pid = random.randint(10000, 30000)

        context = {
            'pid': f"{random_pid}+{item.id}",
            'item': item,
        }

        return render(request, 'confirm.html', context)


# ending of buy request


# for buy from store
def buyFromStore(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            item = AudioFile.objects.get(pk=pk)
            res = buy(request, item, pk)

            request.session['buyFromStore'] = True
            request.session['buyFromProjects'] = False

            request.session['store_item_id'] = item.id
            return res

    else:
        return redirect('loginPage')


# buy from user edited projects
def buyFromProjects(request, pk):
    if request.user.is_authenticated:
        if request.method == "POST":
            item = UserFile.objects.get(pk=pk)
            res = buy(request, item, pk)
            request.session['buyFromProjects'] = True
            request.session['buyFromStore'] = False

            request.session['project_item_id'] = item.id

            return res

    else:
        return redirect('loginPage')


# function to user's cart
def cart(request):
    if request.user.is_authenticated:

        if request.method == "POST":
            pass
        else:
            downloadables = Cart.objects.filter(user=request.user)

            context = {
                'user': request.user,
                'downloadables': downloadables,

            }

            return render(request, 'cart.html', context)

    else:
        return redirect('loginPage')

# carts ends here
