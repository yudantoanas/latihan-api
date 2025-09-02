# command:
# install -> pip install "fastapi[standard]"
# execute script/nyalain server API -> fastapi dev [nama_file].py
# bukan -> python namafile.py

# matiin fastapi di terminal / matiin server
# di keyboard: CTRL + C

# import package
from fastapi import FastAPI, Header, HTTPException
import pandas as pd

# membuat object
app = FastAPI()

# api keys
password = "123456"

# endpoint -> standard untuk, contoh: membuka halaman utama -> meminta data halaman utama
# 1. http function
# 2. url yang bisa diakses oleh client
@app.get("/")
def getMain():
    # baca file csv -> pandas
    df = pd.read_csv('data.csv')

    # misal ada filter, sort, dsb dilakukan sebelum return

    return {
        "message": "Hello world",
        "hasil": df.to_dict(orient="records")
    }

# setiap endpoint tidak boleh memiliki 
# kombinasi http function & url yang sama

# endpoint untuk mendapatkan data specific (filter)
# www.google.com/data/john cena -> response data john cena
# www.google.com/data/randy orton -> response data randy orton
# www.google.com/data/asep -> response error (404 not found)
@app.get("/data/{username}")
def getData(username: str):
    # baca file csv -> pandas
    df = pd.read_csv('data.csv')

    # melakukan filter
    result = df.query(f"nama == '{username}'")

    return {
        "message": "Hello world",
        "hasil": result.to_dict(orient="records")
    }

# endpoint untuk melakukan delete - protected
# jika tidak ada api-key atau api-key != password maka response error
# jika ada dan sesuai maka lanjut delete -> success
@app.delete("/data/{username}")
def deleteData(username: str, api_key: str = Header(None)):
    # cek authentication
    if api_key == None or api_key != password:
        # response error -> object HTTPException
        raise HTTPException(status_code=401, detail="authentication gagal!")

    # baca file csv -> pandas
    df = pd.read_csv('data.csv')

    # melakukan logic delete -> filter exclude
    result = df.query(f"nama != '{username}'")

    # export dataframe ke csv/replace data terbaru 
    # kasih index=False supaya index tidak masuk ke csv
    result.to_csv('data.csv', index=False)

    return {
        "message": "Hello world",
        "hasil": result.to_dict(orient="records")
    }