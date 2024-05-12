FROM python:3.12
RUN mkdir python_tg_bot_calorie
WORKDIR /python_tg_bot_calorie
COPY /pyproject.toml /python_tg_bot_calorie
RUN pip3 install poetry==1.8.2
RUN poetry config virtualenvs.create false
RUN poetry install
COPY . /python_tg_bot_calorie
#CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:3000"]
#CMD ["ls", "-a"]

#RUN python /app/main.py
ENV TG_API_TOKEN="7126934059:AAF5QjfYEOKtolSuYYttRXBTnv0CLD5TMlI"
ENV DB_NAME="test_db"
ENV DB_USER="valentins"
ENV DB_PASSWORD="yyUi6g5uJoPbeN*GgEZr"
ENV DB_HOST="127.0.0.1"
#ENTRYPOINT ["python", "main.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]