# -*- coding: utf-8 -*-
#!/usr/bin/python
from openerp import models, fields, api, _
from openerp.exceptions import ValidationError
from datetime import datetime
from openerp.modules import module
from zipfile import *
from StringIO import StringIO
from os import listdir

import os
import sys

import tempfile
import tarfile
import gzip

import base64

class import_module(models.TransientModel):
    _name = 'import.module'
    _description = 'Importar un Modulo de Formato Zip'

    file = fields.Binary('Archivo')
    datas_fname = fields.Char('Nombre del Archivo',size=256)

    @api.multi
    def module_import(self, file):
        if (self.datas_fname.endswith("tar.gz")):
            path_scripts = os.path.dirname(os.path.abspath("/scripts/restart_odoo.sh"))
            # print "######### SELF PATH SCRIPTS >>>>>>>> ", path_scripts
            if path_scripts == '/scripts':
                context = dict(self._context or {})
                split_name_module = self.datas_fname.split(".tar.gz")
                path_act_module = module.get_module_path('module_import')
                path_complete = path_act_module+'/modules/'
                # print "######## SELF SPLIT NAME MODULE >>>>>> ", split_name_module
                module_name, des= split_name_module
                path_module = module.get_module_path(module_name)
                if path_module == False:
                    raise ValidationError(_('El Modulo Que Desea Actualizar No Existe'))
                else:
                    split_path_module, com = path_module.split(module_name)
                    path_module = split_path_module+module_name
                    # print "######## SELF PATH >>>>>>>>>>>>>>>>>>> ", path_module
                    # print "######## SELF PATH ACT MOCULE >>>>>>>> ", path_complete
                    # print "######## SELF PATH MODULE >>>>>>>>>>>> ", split_path_module
                    compress_file = open(path_complete+self.datas_fname, "wb")
                    compress_file.write(base64.b64decode(self.file))
                    arch_module = path_complete+self.datas_fname
                    # Descomprime el archivo tar.gz en el directorio seleccionado
                    os.system('tar -xzvf %s -C %s' % (arch_module,path_complete))
                    descom_module = path_complete+module_name
                    # print "########## SELF DESCOM MODULE >>>>>>>> ", descom_module
                    cont_listdir = len(listdir(descom_module))
                    # print "########## SELF CONT LISTDIR >>>>>>>>> ", cont_listdir
                    if cont_listdir == 1:
                        raise ValidationError(_('Error Al Descomprimir El Modulo'))
                        os.system('rm -R %s && %s' %(arch_module,descom_module))
                    else:
                        os.system('rm -R %s' %(path_module))
                        os.system('mv %s %s' %(descom_module,split_path_module))
                        os.system('rm -R %s && %s' %(arch_module,descom_module))
                        os.system('screen /scripts/restart_odoo.sh')
                #os.path.dirname(os.path.abspath("/scripts/restart_odoo.sh"))

                # Lee todos los archivos y los compara con los archivos actualizados para remplazarlos
                # os.system('cp -a %s* %s' % (descom_module,split_path_module))
                

                #temp_bytes = base64.b64encode(self.file).decode('utf-8')
                #print "######## SELF TEMP BYTES >>>>>>>> ", temp_bytes
                #zip_text_file = StringIO(self.file)
                #zipper = gzip.GzipFile(mode='wb', fileobj=zip_text_file)
                #zipper.write(context)
                #zipper.close()
                #enc_text =  base64.b64encode(zip_text_file.getvalue())
                #print "####### SELF ENC TEXT >>>>> ", enc_text
                #print "######### SELF FILE >>>>>>>> ", self.file
                #tar -xzvf archivo.tar.gz -C /directorio/final





                #os.system('tar -xvf %s' %(self.datas_fname))
                #os.system('tar -xvf %s' %(self.datas_fname))
                #os.system('tar xvzf %s %s'%(self.datas_fname,path_complete))
                # sample_text_file = gzip.GzipFile(mode='rb', fileobj=StringIO(base64.b64decode(self.file)))
                # DEFAULT_SAMPLE = sample_text_file.read()
                # self.datas_fname.write(DEFAULT_SAMPLE)
                # sample_text_file.close()
                # print "########## SELF DEFAULT SAMPLE >>>>>>>>>>> ", DEFAULT_SAMPLE
                # print "########## SELF PATH MODULE >>>>>>>>> ", path_module
                #path_module = module.get_module_path(module_name)
                #arch_module = base64.b64decode(self.file).decode('utf-8')
                #arch_module.save(self.datas_fname)
                #print "##### SELF ARCH MODULE >>>>>> ", arch_module
                #print "####### SPLIT NAME MODULE >>>>>> ", split_name_module
                #print "#######  SELF MODULE NAME >>>>>> ", module_name
                #print "###### SELF MODULE PATH >>>>>> ", path_module
                #os.system('tar -xvzf %s.tar.gz %s'%(module_name,path_module))
                #os.system('mv %s /tmp/' % (self.datas_fname))
                #new_path = '/tmp/'+self.datas_fname
                #new_path = '/tmp/'+module_name+'.tar.gz'
                #with ZipFile(self.datas_fname) as myzip:
                #    myzip.extractall()
                #if (self.datas_fname.endswith("tar.gz")):
                #    tar = tarfile.open(new_path, "r:gz")
                #    tar.extractall()
                #    tar.close()
            else:
                raise ValidationError(_('No Se Puede Reiniciar'))
        else:
            raise ValidationError(_('El Archivo Debe Ser Formato "tar.gz"'))



