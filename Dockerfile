FROM python:3
 ADD src/ src/
 WORKDIR "/src"
 RUN pip install -r requirements.txt \
    && chmod +x docker-entrypoint.sh \
    && chmod +x docker-wait.py \
    && chmod +x prepare.py \
    && chmod +x run.py 
 ENTRYPOINT [ "./docker-entrypoint.sh" ]
