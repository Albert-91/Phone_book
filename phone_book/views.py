from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from phone_book.models import Person

form = """
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
            </label><br><br>
            <label> Surname:
                <input name='surname' size='10'>
            </label><br><br>
            <label> Description:
                <textarea name='description' cols='20' rows='2' placeholder='Describe here'></textarea>
            </label><br><br>"""

        form += "<input type='submit' value='Dodaj osobę'></form>"
        return form

    @decor_warp_html
    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        description = request.POST.get('description')
        if name and surname:
            Person.objects.create(name=name, surname=surname, description=description)
            response = '{} {} was added!'.format(name, surname)
        else:
            response = 'Not enough data'
        return response


@method_decorator(csrf_exempt, name='dispatch')
class DeletePerson(View):
    def get(self, request):
        pass

    def post(self, request):
        pass
