set python_path= "C:\Users\roik2\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Python 3.7\python.exe"

%python_path% -m pip install virtualenv
%python_path% -m venv venv

mkdir venv\nltk_data

venv\Scripts\activate & ^
python -m pip install --upgrade pip & ^
pip install -r requirements.txt & ^
python setup.py & ^
deactivate

