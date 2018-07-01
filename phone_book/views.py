from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from phone_book.models import Person


def decor_warp_html(form):
    def wrap_html(*args, **kwargs):
        html = """
            <html>
                <body>
                    {}
                </body>
            </html>""".format(form(*args, **kwargs))
        return HttpResponse(html)
    return wrap_html


@method_decorator(csrf_exempt, name='dispatch')
class ShowAll(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


@method_decorator(csrf_exempt, name='dispatch')
class ShowDetail(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


@method_decorator(csrf_exempt, name='dispatch')
class ModifyPerson(View):
    def get(self, request):
        pass

    def post(self, request):
        pass


@method_decorator(csrf_exempt, name='dispatch')
class AddPerson(View):
    @decor_warp_html
    def get(self, request):
        form = """<html><body><form action='#' method='POST'>"""
        form += """
            <label> Name:
                <input name='name' size='10'>
            </label>
            <label> Surname:
                <input name='surname' size='10'>
            </label>
            <label> Description:
                <input type="text" name='description'>
            </label><br><br>"""
        form += """
            <label>Phone number:
                <input name='phone_number' size='10'>
            </label>
            <label>Phone type:
                <select name="phone_type">
                    <option value=1>Home</option>
                    <option value=2>Business</option>
                    <option value=3>Mobile</option>
                </select>
            </label><br><br>"""
        form += """
            <label>E-mail address:
                <input name='email' size='10'>
            </label>
            <label>Phone type:
                <select name="email_type">
                    <option value=1>Home</option>
                    <option value=2>Business</option>
                    <option value=3>Mobile</option>
                </select>
            </label><br><br>"""
        form += """
            <label>Street:
                <input name='street' size='10'>
            </label>
            <label>House number:
                <input name='house_number' size='5'>
            </label>
            <label>Apartment number:
                <input name='apartment_number' size='5'>
            </label>
            <label>City:
                <input name='city' size='10'>
            </label><br><br>
        """
        form += "<input type='submit' value='Dodaj osobę'></form>"
        return form

    @decor_warp_html
    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        description = request.POST.get('description')
        Person.objects.create(name=name, surname=surname, description=description)


@method_decorator(csrf_exempt, name='dispatch')
class DeletePerson(View):
    def get(self, request):
        pass

    def post(self, request):
        pass
