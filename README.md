# Final lab No Sql - 01/2024

## Authors

- [Arthur Meyniel](https://github.com/ArthurMynl)
- [Hugo Fouché](https://github.com/Fouche-Hugo)
- [Ronan Mornet](https://github.com/Warfird)

## How to use

To start the application, you need to have python installed with pip and run the following commands:

Fill the .env file with your own credentials

```bash
pip install -r requirements.txt
python3 -m uvicorn main:app --reload
```

Then you access the application on [http://localhost:8000] and the documentation on [http://localhost:8000/docs].

## How to test

To ensure the API is working well, we have wrote some tests.
To test the application, you need to have pytest installed, the API running and run the following command:

```bash
pytest tests/testing.py
```