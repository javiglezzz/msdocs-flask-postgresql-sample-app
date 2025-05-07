from io import BytesIO
import os
from datetime import datetime
import base64

from flask import Flask, abort, redirect, render_template, request, send_file, send_from_directory, url_for, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__, static_folder='static')
csrf = CSRFProtect(app)

# WEBSITE_HOSTNAME exists only in production environment
if 'WEBSITE_HOSTNAME' not in os.environ:
    # local development, where we'll use environment variables
    print("Loading config.development and environment variables from .env file.")
    app.config.from_object('azureproject.development')
else:
    # production
    print("Loading config.production.")
    app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Initialize the database connection
db = SQLAlchemy(app)

# Enable Flask-Migrate commands "flask db init/migrate/upgrade" to work
migrate = Migrate(app, db)

# The import must be done after db initialization due to circular import issue
from models import ImageRecord

@app.route('/', methods=['GET'])
def list_images():
    images = ImageRecord.query.order_by(ImageRecord.created_at.desc()).all()
    return render_template('images_list.html', images=images)



@app.route('/<int:image_id>/data/<string:image_type>')
def get_image_data(image_id, image_type):
    image = db.session.get(ImageRecord, image_id)
    if not image:
        abort(404)
    
    if image_type == 'original':
        return send_file(BytesIO(image.image_data_original), mimetype='image/png')
    elif image_type == 'transformed':
        return send_file(BytesIO(image.image_data_transformed), mimetype='image/png')
    else:
        abort(400, description="Invalid image type. Use 'original' or 'transformed'.")


@app.route('/vaciar', methods=['GET','POST'])
@csrf.exempt
def vaciar_imagenes():
    try:
        # Borra todos los registros de la tabla images
        num_deleted = db.session.query(ImageRecord).delete()
        db.session.commit()
        return jsonify({
            "status": "ok",
            "message": f"Se eliminaron {num_deleted} imágenes."
        }), 200
    except Exception as e:
        db.session.rollback()
        app.logger.exception("Error al vaciar la tabla images")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
@app.route('/upload', methods=['POST'])
@csrf.exempt
def upload_image():
    try:
        data = request.get_json(force=True)
        img_b64   = data.get('image_base64', '')
        img_bytes = base64.b64decode(img_b64)
        img_b64_2   = data.get('image_base64_2', '')
        img_bytes_2 = base64.b64decode(img_b64)

     
        # Creamos el registro incluyendo el blob
        record = ImageRecord(
            red_pixels   = data.get('red_pixels'),
            green_pixels = data.get('green_pixels'),
            blue_pixels  = data.get('blue_pixels'),
            width        = data.get('width'),
            height       = data.get('height'),
            filename     = data.get('filename'),
            image_data_original   = img_bytes,
            image_data_transformed = img_bytes_2,
            created_at   = datetime.now()
        )
        db.session.add(record)
        db.session.commit()

        return jsonify({
            "status": "ok",
            "id":     record.id,
      
        }), 201

    except Exception as e:
        app.logger.exception("Error en /upload")
        return jsonify({
            "status":  "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    app.run()
