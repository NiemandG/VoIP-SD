FROM niemanddocker/niemand-stuff
WORKDIR /voip
COPY . .
RUN pip install requests
CMD ["python3", "voip.py"]


