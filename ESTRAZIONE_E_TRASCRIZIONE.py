output_dir = "audio"
os.makedirs(output_dir, exist_ok=True)


# Connessione al database
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=SQLINPSSVIL83.ser-test.inps,1433;"
    "Database=DS05323_EVCANUTFRAG_test;"
    "UID=DBDS0532300;"
    "PWD=SSppcc2300;"
)
cursor = conn.cursor()   
query = "SELECT IdSegreteriaTelefonica, FileAudio FROM dbo.[Query]"
cursor.execute(query)
model = whisper.load_model("large")
for row in cursor:
    if row.FileAudio:
        filename = os.path.join(output_dir, f"audio_{row.IdSegreteriaTelefonica}.mp3")
        with open(filename, "wb") as f:
            f.write(row.FileAudio)
            f.flush()
            os.fsync(f.fileno())
        print(f"File salvato: {filename}")

        if not os.path.exists(filename):
            print(f"File non trovato: {filename}")
            continue

        try:
            
            result = model.transcribe(filename, language="it")
            trascrizione = result['text']
            print(f"Trascrizione ({filename}): {trascrizione}")
        except Exception as e:
            print(f"Errore nella trascrizione della richiesta {filename}: {e}")
    else:
        print(f"Nessun file audio per ID {row.IdSegreteriaTelefonica}")
