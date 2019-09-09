import csv
from functools import update_wrapper

from django.conf.urls import url
from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from django.db import DatabaseError, transaction
from django.shortcuts import render
from django.urls import path
from regist.models import Author, Article


class AuthorAdmin(admin.ModelAdmin):
    list_filter = ('user__is_active', 'is_ugm')


admin.site.register(Author, AuthorAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('edas_id', 'title', 'page_no')
    list_filter = ('is_paid', )
    search_fields = ['edas_id', 'title']

    change_list_template = 'admin/custom_change_list.html'

    def get_urls(self):
        # this is just a copy paste from the admin code
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            return update_wrapper(wrapper, view)

        # get the default urls
        urls = super(ArticleAdmin, self).get_urls()
        # define my own urls
        custom_urls = [
            path('upload/data',
                 wrap(self.upload_initial_data),
                 name='upload_initial_data'),
        ]
        return urls + custom_urls

    def upload_initial_data(self, request):

        if request.method == 'POST' and request.FILES['myfile']:
            error = ''
            myfile = request.FILES['myfile']
            decoded_file = myfile.read().decode('utf-8-sig').splitlines()
            reader = csv.DictReader(decoded_file)

            try:
                with transaction.atomic():
                    for row in reader:
                        # create article
                        article = Article.objects.create(
                            edas_id=row.get('#', '-'),
                            title=row.get('Title', '-'),
                            remark=row.get('Track', '-'),
                            page_no=row.get('final manuscript: pages', 0)
                        )

                        # create author(s) - User
                        authors = row.get('Authors', '')
                        author_list = [x.strip() for x in authors.split(';')]
                        ids = row.get('Author IDs', '')
                        id_list = [x.strip() for x in ids.split(';')]
                        emails = row.get('Author emails', '')
                        email_list = [x.strip() for x in emails.split(';')]

                        for index, author in enumerate(author_list):
                            first_space = author.find(' ')
                            first_name = author[:first_space]
                            last_name = author[first_space + 1:]
                            try:
                                user = User.objects.get(username=id_list[index])
                            except User.DoesNotExist:
                                user = User.objects.create_user(
                                    username=id_list[index],
                                    email=email_list[index],
                                    password='Ti9021IcIeeT',
                                    first_name=first_name,
                                    last_name=last_name,
                                    is_active=False
                                )
                            article.authors.add(user)

            except DatabaseError as ex:
                error = str(ex)
        else:
            error = 'PLEASE UPLOAD!'

        return render(request, template_name='admin/upload_initial_data.html', context={'error': error})


admin.site.register(Article, ArticleAdmin)
