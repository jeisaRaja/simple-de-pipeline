echo "Start Luigi ETL Pipeline Process"
VENV_PATH="/home/jeisa/programming/de/pacmann-project-1/venv/bin/activate"
source "$VENV_PATH"

PYTHON_SCRIPT="/home/jeisa/programming/de/pacmann-project-1/etl.py"

python3 "$PYTHON_SCRIPT" >> /home/jeisa/programming/de/pacmann-project-1/logs/logfile.log 2>&1

dt=$(date '+%d/%m/%Y %H:%M:%S');
echo "Luigi Started at ${dt}" >> /home/jeisa/programming/de/pacmann-project-1/logs/luigi_info.log

echo "End Luigi ETL Pipeline Process"

