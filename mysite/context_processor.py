from blog.models import About

def access_aboutus(request):
    about_us = About.objects.all()[0]
    return {'about_us':about_us} 
