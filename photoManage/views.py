import mimetypes
import os
import re

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from djangoProject3 import settings
from photoManage import models


def photoupload(request):
    if request.method == 'POST':
        upload_photo = request.FILES.get("upload_photo", None)  # 得到用户上传的文件
        photo_type = os.path.splitext(upload_photo.name)  # 得到文件的后缀
        photo_size = upload_photo.size # 得到文件的大小
        print(photo_type[1])
        print(photo_size)

        # 如果上传的文件不符合要求
        if photo_type[1] != '.jpg' and photo_type[1] != '.jpeg' and photo_type[1] !='.png':
            return render(request, 'error.html', {"errorInfo" : "上传失败！！：请上传jpg,png,jpeg格式的图片"})
        if photo_size >= 1024000:
            return render(request, 'error.html', {"errorInfo": "上传失败！！：上传图片不可超过1M"})

        # 构造真正的图片名称 检查名称是否重复
        photo_name = request.POST.get("photoName")
        photo_name = re.sub(r'\s+', '', photo_name)
        print(photo_name)
        gavegtml = photo_name

        if photo_name == '':
            return render(request, 'error.html', {"errorInfo": "上传失败！！：请填写唯一标识"})
        photo_name = photo_name + photo_type[1]
        isPhoto = models.userUploadPhotos.objects.filter(photosname=photo_name).first()
        if isPhoto != None:
            return render(request, 'error.html', {"errorInfo": "上传失败！！：请填写唯一标识（学号加第几次上传）"})

        # 编辑图片保存地址
        uploadPhotoSavePaht = os.path.join(settings.BASE_DIR,'photoManage', 'photos/useruUploadPhoto', photo_name)
        print(uploadPhotoSavePaht)

        #如果上传的图片不为空
        if upload_photo:
            # 将文件保存到指定位置
            with open(uploadPhotoSavePaht, 'wb+') as destination:
                for chunk in upload_photo.chunks():
                    destination.write(chunk)
                destination.close()
                # 保存文件信息
                models.userUploadPhotos.objects.create(photosname=photo_name, photostate='未处理')
            return render(request, 'success.html', {"successInfo" : "图片上传成功", "photo_name":gavegtml})
        else:
            return render(request, 'error.html', {"errorInfo": "请上传图片"})

    return render(request, 'photoupload.html')

def getUserUploaPhotoList(request):
    if request.method == 'POST':
        acmAdmin = request.POST.get("acmAdmin")
        if acmAdmin == 'asdeurnwergfg':
            allPhoto = models.userUploadPhotos.objects.filter().all()
            for photo in allPhoto:
                print(photo.photosname)
            return render(request, 'getUserUploaPhotolist.html', {"allPhoto": allPhoto})
    return render(request, 'getUserUploaPhotolist.html', {"allPhoto": ''})

def getUserUploadPhoto(request):
    getUserUploadPhotoName = request.GET['getUserUploadPhotoName']
    print(getUserUploadPhotoName)
    if getUserUploadPhotoName == '':
        return render(request, 'error.html', {"errorInfo": "参数错误"})
    else:
        print(getUserUploadPhotoName)
        # 获取图片类型
        photoType = mimetypes.guess_type(getUserUploadPhotoName)
        print(photoType[0])
        getUserUploadPhotoSavePath = os.path.join(settings.BASE_DIR, 'photoManage', 'photos/useruUploadPhoto', getUserUploadPhotoName)
        with open(getUserUploadPhotoSavePath, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type=photoType[0])  # 假设图片是JPEG格式
            response['Content-Disposition'] = 'inline; filename="{0}"'.format(getUserUploadPhotoName)  # 设置文件名和显示方式
            return response;
        return render(request, 'error.html', {"errorInfo": "错误"})

def acmAdminProcessOkUpload(request):
    getUserUploadPhotoName = request.GET['getUserUploadPhotoName'] #得到用户上传图片的名字
    if request.method == 'POST':
        upload_photo = request.FILES.get("upload_photo", None)
        if upload_photo.name != getUserUploadPhotoName:
            return render(request, 'error.html', {"errorInfo": "上传的图片和用户命名不符"})
        else:
            uploadPhotoSavePaht = os.path.join(settings.BASE_DIR, 'photoManage', 'photos/adminUploadUser', getUserUploadPhotoName)
            with open(uploadPhotoSavePaht, 'wb+') as destination:
                for chunk in upload_photo.chunks():
                    destination.write(chunk)
                destination.close()
                # 保存文件信息
                update_userLoad_adta = models.userUploadPhotos.objects.get(photosname=getUserUploadPhotoName)
                update_userLoad_adta.photostate = '处理完成'
                update_userLoad_adta.save()
                models.userGetPhotos.objects.create(photosname=getUserUploadPhotoName, photostate='处理完成')
            return render(request, 'success.html', {"successInfo" : "图片上传成功", "photo_name" : getUserUploadPhotoName})
    return render(request, 'acmAdminProcessOkUpload.html', {"getUserUploadPhotoName":getUserUploadPhotoName})

def userGetMyselfUploadPhotoList(request):
    if request.method == "POST":
        photoName = request.POST.get("photoName")
        if photoName == '':
            return render(request, 'error.html', {"errorInfo": "请输入学号加第几次上传(图片的唯一标识)"})
        else:
            photoNamePng = photoName + '.png'
            allPhot = []
            isPhotoNamePng = models.userUploadPhotos.objects.filter(photosname=photoNamePng).first()
            # 如果当前的图片存在
            if isPhotoNamePng != None:
                allPhot.append(isPhotoNamePng)

            photoNameJpg = photoName + '.jpg'
            isPhotoNameJpg = models.userUploadPhotos.objects.filter(photosname=photoNameJpg).first()
            if isPhotoNameJpg != None:
                allPhot.append(isPhotoNameJpg)

            photoNameJpeg = photoName + '.jpeg'
            isPhotoNameJpeg = models.userUploadPhotos.objects.filter(photosname=photoNameJpeg).first()
            if isPhotoNameJpeg != None:
                allPhot.append(isPhotoNameJpeg)
            return render(request, 'userGetMyselfUploadPhotoList.html', {'allPhot' : allPhot});

    if request.method == 'GET':
        return render(request, 'userGetMyselfUploadPhoto.html');

def userGetRealPhoto(request):
    getUserUploadPhotoName = request.GET['getUserUploadPhotoName']
    if getUserUploadPhotoName == '':
        return render(request, 'error.html', {"errorInfo": "参数错误"})
    else:
        print(getUserUploadPhotoName)
        # 获取图片类型
        photoType = mimetypes.guess_type(getUserUploadPhotoName)
        print(photoType[0])
        getUserUploadPhotoSavePath = os.path.join(settings.BASE_DIR, 'photoManage', 'photos/adminUploadUser',
                                                  getUserUploadPhotoName)
        with open(getUserUploadPhotoSavePath, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type=photoType[0])  # 假设图片是JPEG格式
            response['Content-Disposition'] = 'inline; filename="{0}"'.format(getUserUploadPhotoName)  # 设置文件名和显示方式
            # 更改文件信息
            update_userLoad_adta = models.userUploadPhotos.objects.get(photosname=getUserUploadPhotoName)
            update_userLoad_adta.photostate = '用户已经下载'
            update_userLoad_adta.save()
            return response;
        return render(request, 'error.html', {"errorInfo": "错误"})