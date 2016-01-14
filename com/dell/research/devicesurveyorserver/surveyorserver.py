import os

__author__ = 'irwin_reyes'

from flask import Flask, render_template, request, make_response

my_path = os.path.dirname(os.path.realpath(__file__))
base_path = os.path.join(my_path, '..', '..', '..', '..')
out_dir = os.path.join(base_path, 'data')
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

app = Flask(__name__, template_folder=os.path.join(base_path, 'templates'))


@app.route("/")
def index():
    return render_template('index.html', title='Visualization')

@app.route("/surveypost/",methods=['POST'])
def post():
    response = make_response()

    # Put a size limit of 10 KBs on transmissions
    if request.content_length < 10 * 1024:
        data = request.get_json()

        # Only write data from messages containing a deviceID field
        if 'deviceRandomID' in data:
            device_id = data['deviceRandomID']
            device_manufacturer = data['deviceManufacturer']
            device_model = data['deviceModel']
            out_path = os.path.join(out_dir, "%s_%s--%s" % (device_manufacturer, device_model, device_id))

            # Do not overwrite existing files
            if not os.path.exists(out_path):
                file_out = open(out_path, 'w')
                for label in data:
                    # Skip getevent data to put it at the very end
                    if label == 'getevent':
                        continue

                    value = data[label]
                    file_out.write("%s : %s\n" % (label, value))

                # Append getevent data if available
                if 'getevent' in data:
                    file_out.write("\n\n-----\n%s : %s" % ('getevent', data['getevent']))

                file_out.close()

                response.headers['X-SurveySuccess'] = 'success'
            else:
                response.headers['X-SurveySuccess'] = 'survey already submitted'
        else:
            response.headers['X-SurveySuccess'] = 'invalid submission'
    else:
        response.headers['X-SurveySuccess'] = 'submission too large'

    return response

if __name__ == "__main__":
    app.debug = False
    app.run(host='0.0.0.0', port=5000)
    # Then visit http://localhost:5000 to subscribe
    # and send messages by visiting http://localhost:5000/publish
