from src.utilities import sken_logger, sken_singleton
from src.services import sequence_match
from flask import Flask, request, Response
import jsonpickle

sken_singleton.Singletons()

logger = sken_logger.get_logger("Main")

app = Flask(__name__)


@app.route('/sequence_match')
def seq_match():
    sentence = request.args.get("sentence")
    resp = Response(jsonpickle.encode(sequence_match.return_idx(sentence)), status=200,
                    mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='9999', debug=True)
