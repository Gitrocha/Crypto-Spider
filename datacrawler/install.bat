@echo off
title GPS - Gestao de Pagamentos Stone.
echo .............................................................
echo ................. Configurando o Python .....................
echo .............................................................
echo
python -m pip install --upgrade pip setuptools wheel
python -m pip install virtualenv
echo .............................................................
echo .................. Criando virtualenv .......................
echo .............................................................
echo
python -m virtualenv env
echo .............................................................
echo ................... Finalizado - 1/2 ........................
echo .............................................................
echo ................ Instalando dependencias ....................
echo .............................................................
echo
env\Scripts\activate && python -m pip install -r requirements.txt && deactivate && echo ................... Finalizado - 2/2 .......................