from flask import Flask, render_template, request, redirect, url_for
from pysnmp.hlapi import *


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Kullanıcı adı ve şifreyi kontrol edin (bu örnekte sabit değerler kullanılıyor)
    if username == 'can' and password == 'boz':
        return redirect(url_for('snmp_query'))
    else:
        return 'Geçersiz kullanıcı adı veya şifre'

@app.route('/snmp')
def snmp_query():
    # SNMP GET komutu ile sysDescr OID'si sorgulanıyor
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData('public', mpModel=0),
               UdpTransportTarget(('demo.snmplabs.com', 161)),
               ContextData(),
               ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'))  # sysDescr OID'si
        )
    )

    if errorIndication:
        result = str(errorIndication)
    elif errorStatus:
        result = '%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
        )
    else:
        # sysDescr değerini varBinds'den alın
        result = varBinds[0][1].prettyPrint()

    return render_template('snmp_result.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
