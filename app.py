from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Base de datos simulada
db = {
    'clientes': [],
    'proveedores': [],
    'productos': [],
    'stock': []
}
id_counter = {k: 1 for k in db}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<tipo>")
def get_items(tipo):
    return jsonify(db[tipo])

@app.route("/<tipo>/<int:item_id>")
def get_item(tipo, item_id):
    item = next((i for i in db[tipo] if i['id'] == item_id), None)
    return jsonify(item) if item else ('', 404)

@app.route("/<tipo>", methods=["POST"])
def create_item(tipo):
    data = request.json
    data["id"] = id_counter[tipo]
    id_counter[tipo] += 1
    db[tipo].append(data)
    return jsonify(data), 201

@app.route("/<tipo>/<int:item_id>", methods=["PUT"])
def update_item(tipo, item_id):
    item = next((i for i in db[tipo] if i["id"] == item_id), None)
    if not item:
        return '', 404
    item.update(request.json)
    return jsonify(item)

@app.route("/<tipo>/<int:item_id>", methods=["DELETE"])
def delete_item(tipo, item_id):
    db[tipo] = [i for i in db[tipo] if i["id"] != item_id]
    return '', 204

if __name__ == "__main__":
    app.run(debug=True)
