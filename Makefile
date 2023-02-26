WORKDIR = yatube
TEMPLATES-DIR = $(WORKDIR)/templates
MANAGE = python $(WORKDIR)/manage.py

style:
	black -S -l 79 $(WORKDIR)
	isort $(WORKDIR)
	djlint $(TEMPLATES-DIR) --reformat
	flake8 $(WORKDIR)

run:
	$(MANAGE) runserver

shell:
	$(MANAGE) shell

testp:
	$(MANAGE) test posts

testa:
	$(MANAGE) test about

testu:
	$(MANAGE) test users
