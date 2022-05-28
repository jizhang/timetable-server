# TimeTable

What have you done today?

## Development

### Linux

```
/usr/local/opt/python@3.8/bin/python3 -m venv venv
make dev
make
```

Browse http://127.0.0.1:5001/

### Windows

```
C:\ProgramData\Anaconda3\Scripts\activate base
conda create -n timetable python=3.8
conda activate timetable
pip install -r requirements.txt -r requirements-dev.txt
flask run
```
