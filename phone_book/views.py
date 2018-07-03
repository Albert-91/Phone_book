from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from phone_book.models import Person, Email, Phone, Address

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
    @decor_warp_html
    def get(self, request):
        table = """
            <table border=1>
                <tr>
                    <td align="center">Surname and name</td>
                    <td align="center">Options</td>
                </tr>
            """
        persons = Person.objects.order_by('surname')
        for person in persons:
            table += """
                <tr>
                    <td align="center"><a href='/person/{0}' style="color:black">{1} {2}</a></td>
                    <td align="center"><a href='/delete/{0}' style="color:red">delete</a>
                        <a href='/modify/{0}' style="color:green"> modify</a></td>
                </tr>
                """.format(person.id, person.surname, person.name)
        table += "</table><br>"
        table += """<form><button formaction="/new/">Add new person</button></form>"""
        return table


@method_decorator(csrf_exempt, name='dispatch')
class ShowDetail(View):
    @decor_warp_html
    def get(self, request, id):
        person = Person.objects.get(id=id)
        table = """
            <table border=1>
                <tr>
                    <td></td>
                    <td align="center">Data</td>
                </tr>
                <tr>
                    <td>Name</td>
                    <td align="center">{}</td>
                </tr>
                <tr>
                    <td>Surname</td>
                    <td align="center">{}</td>
                </tr>
                <tr>
                    <td>Description</td>
                    <td align="center">{}</td>
                </tr>
                
        """.format(person.name, person.surname, person.description)

        emails = Email.objects.filter(person_id=id)
        phones = Phone.objects.filter(person_id=id)
        addresses = Address.objects.filter(person_id=id)
        # if emails or phones or addresses:
        #     for email in emails:
        #         table += """
        #             <tr>
        #                 <td>Email</td>
        #                 <td align="center">{}</td>
        #             </tr>
        #         """

        # groups = Address.objects.filter(person_id=id)
        table += "</table><br>"
        table += """<form><button formaction="/modify/{}">Modify person</button></form>""".format(id)
        return table


@method_decorator(csrf_exempt, name='dispatch')
class ModifyPerson(View):
    @decor_warp_html
    def get(self, request, id):
        return "modified"

    @decor_warp_html
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

    def post(self, request):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        description = request.POST.get('description')
        if name and surname:
            Person.objects.create(name=name, surname=surname, description=description)
            last_id = Person.objects.order_by('-id')[0]
            response = HttpResponseRedirect('/person/{}'.format(last_id.id))
        else:
            response = 'Not enough data'
        return response


@method_decorator(csrf_exempt, name='dispatch')
class DeletePerson(View):
    @decor_warp_html
    def get(self, request, id):
        person = Person.objects.get(id=id)
        person.delete()
        answer = "{} {} was deleted from database".format(person.name, person.surname)
        return answer


