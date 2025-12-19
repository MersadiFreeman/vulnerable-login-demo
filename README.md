\# Vulnerable vs Secure Login Demo (Flask)



This project demonstrates the difference between an \*\*intentionally insecure\*\* login system and a \*\*secure\*\* login system built with Python and Flask.



The goal is to learn common web authentication vulnerabilities by building them on purpose, then fixing them using basic security best practices.



---



\## Project Structure



vulnerable-login-demo/

├── insecure\_app/

│ └── app.py # Intentionally insecure login logic

├── secure\_app/

│ ├── app.py # Secure login implementation

│ └── db.sqlite3 # SQLite database (created at runtime)

├── requirements.txt

└── README.md





\## Insecure Version (`insecure\_app`)



The insecure application is intentionally vulnerable and demonstrates \*\*what NOT to do\*\*.



\### Vulnerabilities demonstrated:

\- Plaintext passwords

\- No password hashing

\- No rate limiting (brute-force possible)

\- No account lockout

\- Unsafe authentication logic

\- Informative error behavior



This version exists \*\*only for local testing and learning purposes\*\*.



---



\## Secure Version (`secure\_app`)



The secure application fixes the vulnerabilities found in the insecure version.



\### Security improvements:

\- Password hashing using `werkzeug.security`

\- Parameterized SQL queries (prevents SQL injection)

\- SQLite database for credential storage

\- Basic rate limiting to reduce brute-force attacks

\- Generic login error messages

\- Session-based authentication



---



\## How to Run



\### Requirements

\- Python 3.10+

\- Git



Install dependencies:

```bash

pip install -r requirements.txt

Run the insecure app

cd insecure\_app

python app.py



Run the secure app

cd secure\_app

python app.py





Open your browser and visit:



http://127.0.0.1:5000



Learning Objectives



This project was built to:



Understand how authentication systems fail when security is ignored



Practice identifying common login vulnerabilities



Compare insecure vs secure implementations side-by-side



Learn hands-on by breaking and fixing real code



!!! WARNING !!!



This project is for educational use only.

The insecure application should never be deployed to a public server.

