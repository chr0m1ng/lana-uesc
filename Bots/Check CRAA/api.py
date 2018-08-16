import pdftotext
import urllib2
from flask import Flask, request
from flask_restful import Resource, Api
import re
import os


app = Flask(__name__)
api = Api(app)

class CheckCRAA(Resource):
    def post(self):
	print('teste')
        if 'url' in request.json:
            r = urllib2.urlopen(request.json['url'])

            pdf = pdftotext.PDF(r)

            # Read some individual pages
            p = re.compile('([0-9]{1,2},[0-9]{1,2})')
            craa = p.findall(pdf[0])[2]
            return {'craa' : craa}
        else:
            return 'Fora do padrao', 400

api.add_resource(CheckCRAA, '/api/check_craa')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
