from django.http import HttpResponse
from django.shortcuts import render, redirect
from database.models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def home(request):
    product = allproduct.objects.all().order_by('id').reverse()[:3]
    preorder = allproduct.objects.filter(quantity__lte=3)
    context = {'product': product, 'preorder': preorder}
    return render(request, 'home.html', context)


def item(request):
    return render(request, 'item.html')


def about(request):
    return render(request, 'about.html')


def contactus(request):
    return render(request, 'contactus.html')


def addproduct(request):
    if request.user.profile.usertype != 'admin':
        return redirect('home')

    if request.method == 'POST' and request.FILES['imageupload']:
        data = request.POST.copy()
        name = data.get('name')
        price = data.get('price')
        detail = data.get('detail')
        imageurl = data.get('imageurl')
        quantity = data.get('quantity')
        unit = data.get('unit')

        new = allproduct()
        new.name = name
        new.price = price
        new.detail = detail
        new.imageurl = imageurl
        new.quantity = quantity
        new.unit = unit
        ##########save Imange#################
        file_image = request.FILES['imageupload']
        file_image_name = request.FILES['imageupload'].name.replace(' ', '')
        print('FILE_IMAGE:', file_image)
        print('IMAGE_NAME:', file_image_name)
        fs = FileSystemStorage()
        filename = fs.save(file_image_name, file_image)
        upload_file_url = fs.url(filename)
        new.image = upload_file_url[6:]
        ###########################
        new.save()

    return render(request, 'addproduct.html')


def product(request):
    product = allproduct.objects.all().order_by('id').reverse()
    context = {'product': product}
    return render(request, 'allproduct.html', context)


def register(request):
    if request.method == 'POST':
        data = request.POST.copy()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')

        newuser = User()
        newuser.username = email
        newuser.email = email
        newuser.first_name = first_name
        newuser.last_name = last_name
        newuser.set_password(password)
        newuser.save()

        profile = Profile()
        profile.user = User.objects.get(username=email)
        profile.save()

        user = authenticate(username=email, password=password)
        login(request, user)

    return render(request, 'register.html')


def AddtoCart(request, pid):
    username = request.user.username
    user = User.objects.get(username=username)
    check = allproduct.objects.get(id=pid)

    try:
        newcart = Cart.objects.get(user=user, productid=str(pid))
        newquan = newcart.quantity + 1
        newcart.quantity = newquan
        calculate = newcart.price * newquan
        newcart.total = calculate
        newcart.save()

        # update จำนวนของตระกร้าสินค้าตอนนี้
        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updatequan = Profile.objects.get(user=user)
        updatequan.cartquan = count
        updatequan.save()

        return redirect('allproduct')

    except:
        newcart = Cart()
        newcart.user = user
        newcart.productid = pid
        newcart.productname = check.name
        newcart.price = int(check.price)
        newcart.quantity = 1
        calculate = int(check.price) * 1
        newcart.total = calculate
        newcart.save()

        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updatequan = Profile.objects.get(user=user)
        updatequan.cartquan = count
        updatequan.save()

        return redirect('allproduct')


def MyCart(request):
    username = request.user.username
    user = User.objects.get(username=username)

    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        productid = data.get('productid')
        item = Cart.objects.get(user=user, productid=productid)
        item.delete()
        context['status'] = 'delete'

        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updatequan = Profile.objects.get(user=user)
        updatequan.cartquan = count
        updatequan.save()

    mycart = Cart.objects.filter(user=user)
    count = sum([c.quantity for c in mycart])
    total = sum([c.total for c in mycart])

    context['mycart'] = mycart
    context['count'] = count
    context['total'] = total

    return render(request, 'mycart.html', context)


def MyCartEdit(request):
    username = request.user.username
    user = User.objects.get(username=username)

    context = {}

    if request.method == 'POST':
        data = request.POST.copy()
        print(data)

        if data.get('clear') == 'clear':
            print(data.get('clear'))
            Cart.objects.filter(user=user).delete()
            updatequan = Profile.objects.get(user=user)
            updatequan.cartquan = 0
            updatequan.save()
            return redirect('MyCart')

        editlist = []
        for k, v in data.items():
            print(k, v)
            if k[:2] == 'pd':
                pid = int(k.split('_')[1])
                dt = [pid, int(v)]
                editlist.append(dt)
        print('editlist : ', editlist)

        for ed in editlist:
            edit = Cart.objects.get(productid=ed[0])
            edit.quantity = ed[1]
            calculate = edit.price * ed[1]
            edit.total = calculate
            edit.save()
        count = Cart.objects.filter(user=user)
        count = sum([c.quantity for c in count])
        updatequan = Profile.objects.get(user=user)
        updatequan.cartquan = count
        updatequan.save()

        return redirect('MyCart')

    mycart = Cart.objects.filter(user=user)
    context['mycart'] = mycart

    return render(request, 'mycartedit.html', context)


def Checkout(request):
    return render(request, 'checkout1.html')
