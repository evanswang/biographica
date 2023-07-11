import pendulum as pendulum
import ftplib
import logging

from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from airflow.models import DAG, Variable


@dag(
    schedule_interval=None,
    start_date=pendulum.datetime(2023, 1, 1, tz="Europe/London"),
    catchup=False,
    params={}
)
def biographica():

    @task(task_id='get_ftp_meta')
    def get_ftp_meta(**context):
        files = []
        try:
            ftp = ftplib.FTP("ftp.ensemblgenomes.ebi.ac.uk")
            ftp.login()
            organism = Variable.get("organism")
            task_num = Variable.get("task_num")
            ftp.cwd(f"pub/plants/release-55/gff3/{organism}")
            files = ftp.nlst()
            index = 0
            while files:
                chunk, files = files[:task_num], files[task_num:]
                # s3.write(s3_file_name_index, chunk)
                index += 1
        except ftplib.error_perm as resp:
            if str(resp) == "550 No files found":
                "No files in this directory"
            else:
                raise
        finally:
            ftp.quit()

    @task(task_id='process_ftp_data')
    def process_ftp_data(my_id):
        logging.info(f"processing file {my_id}")

    start = EmptyOperator(task_id='start')
    done = EmptyOperator(task_id='done')

    files = get_ftp_meta()
    ftp_tasks = []
    for i in range(3):
        ftp_tasks.append(process_ftp_data(i))
    start >> files >> ftp_tasks >> done

biographica()
