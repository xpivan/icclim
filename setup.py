#!/usr/bin/env python
# -*- coding: utf-8 -*-
# notez qu'on import la lib
# donc assurez-vous que l'importe n'a pas d'effet de bord
#import icclim

import os

from icclim import __version__

#from distutils.core import setup, Extension, Command

from setuptools import setup, Extension, find_packages, Command
import pdb
lib_path = os.getenv('PATH').split(os.pathsep)[0][:-3]+'lib/site-packages/'
os.system('gcc -fPIC -g -c -Wall ./icclim/libC.c -o ./icclim/libC.o')
os.system('gcc -shared -o ./icclim/libC.so ./icclim/libC.o')

module1 = Extension('libC',
                sources = ['./icclim/libC.c'])

# Ceci n'est qu'un appel de fonction. Mais il est treeeeeeeeeees long
# et il comporte beaucoup de parametres
setup(
 
    # le nom de votre bibliotheque, tel qu'il apparaitre sur pypi
    name='icclim',
    
    #include_dirs = ['/usr/local/include']
    #library_dirs = [lib_path],
    # la version du code
    version=__version__,
    # Liste les packages a inserer dans la distribution
    # plutot que de le faire a la main, on utilise la foncton
    # find_packages() de setuptools qui va cherche tous les packages
    # python recursivement dans le dossier courant.
    # C'est pour cette raison que l'on a tout mis dans un seul dossier:
    # on peut ainsi utiliser cette fonction facilement
    packages=find_packages(),
 

                    
    # votre pti nom
    author="Christian P.",
 
    # Votre email, sachant qu'il sera publique visible, avec tous les risques
    # que ca implique.
    author_email="christian.page@cerfacs.fr",
 
    # Une description courte
    description="Python library for climate indices calculation",
 
    # Une description longue, sera affichee pour presenter la lib
    # Generalement on dump le README ici
    long_description=open('README.md').read(),

    # Vous pouvez rajouter une liste de dependances pour votre lib
    # et meme preciser une version. A l'installation, Python essayera de
    # les telecharger et les installer.
    #
    # Ex: ["gunicorn", "docutils >= 0.3", "lxml==0.5a7"]
    #
    # Dans notre cas on en a pas besoin, donc je le commente, mais je le
    # laisse pour que vous sachiez que ca existe car c'est tres utile.
    # install_requires= ,
 
    # Active la prise en compte du fichier MANIFEST.in
    include_package_data=True,
    data_files = [('icclim', ['icclim/config_indice.json'])],
    # Une url qui pointe vers la page officielle de votre lib
    url='https://github.com/cerfacs-globc/icclim',
 
    # Il est d'usage de mettre quelques metadata a propos de sa lib
    # Pour que les robots puissent facilement la classer.
    # La liste des marqueurs autorisees est longue, alors je vous
    # l'ai mise sur 0bin: http://is.gd/AajTjj
    #
    

    # Il n'y a pas vraiment de regle pour le contenu. Chacun fait un peu
    # comme il le sent. Il y en a qui ne mettent rien.
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 1 - Planning",
        "License :: OSI Approved",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Topic :: Climate Index",
    ],
 
    #setup_requires=["pytest-runner"],
    #tests_require=["pytest"], 
    # C'est un systeme de plugin, mais on s'en sert presque exclusivement
    # Pour creer des commandes, comme "django-admin".
    # Par exemple, si on veut creer la fabuleuse commande "proclame-sm", on
    # va faire pointer ce nom vers la fonction proclamer(). La commande sera
    # cree automatiquement. 
    # La syntaxe est "nom-de-commande-a-creer = package.module:fonction".
    #entry_points = {
    #    'console_scripts': [
    #        'proclame-sm = sm_lib.core:proclamer',
    #    ],
    #},
    #
    # A fournir uniquement si votre licence n'est pas listee dans "classifiers"
    # ce qui est notre cas
    #license="WTFPL",
 
    # Il y a encore une chiee de parametres possibles, mais avec ca vous
    # couvrez 90% des besoins
    #cmdclass={'install_all':Install_C_sharedLib}
)

