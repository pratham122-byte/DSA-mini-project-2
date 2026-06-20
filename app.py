from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='static')

# Social graph data
GRAPH = {
    "Arjun":     ["Meera", "Rohit", "Dev"],
    "Meera":     ["Arjun", "Nisha", "Kavya"],
    "Rohit":     ["Arjun", "Siddharth", "Tanvi", "Nikhil"],
    "Dev":       ["Arjun", "Priyanka"],
    "Nisha":     ["Meera", "Pooja", "Raj"],
    "Kavya":     ["Meera", "Ananya"],
    "Siddharth": ["Rohit", "Tanvi"],
    "Tanvi":     ["Rohit", "Siddharth", "Isha"],
    "Nikhil":    ["Rohit", "Priyanka"],
    "Priyanka":  ["Dev", "Nikhil"],
    "Pooja":     ["Nisha", "Raj"],
    "Raj":       ["Nisha", "Pooja"],
    "Ananya":    ["Kavya"],
    "Isha":      ["Tanvi"]
}


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/graph')
def get_graph():
    """Return the full social graph."""
    return jsonify(GRAPH)


@app.route('/api/people')
def get_people():
    """Return list of all people."""
    return jsonify(sorted(GRAPH.keys()))


@app.route('/api/recommend/<person>')
def recommend(person):
    """
    Compute friend recommendations for a given person using
    mutual-friend (2-hop BFS) logic.

    Returns:
      - recommendations: { rec_name: via_friend, ... }
      - highlight_edges:  [ [a, b], ... ]  (ordered path edges for animation)
    """
    if person not in GRAPH:
        return jsonify({"error": f"Person '{person}' not found."}), 404

    friends = set(GRAPH[person])
    recs = {}          # rec -> via_friend
    hl_edges = []      # ordered edges for front-end animation
    seen_edges = set()

    for friend in GRAPH[person]:
        for mutual in GRAPH[friend]:
            if mutual == person:
                continue
            if mutual in friends:
                continue
            if mutual not in recs:
                recs[mutual] = friend

                # Record the two edges, deduplicated
                e1 = tuple(sorted([person, friend]))
                e2 = tuple(sorted([friend, mutual]))
                if e1 not in seen_edges:
                    seen_edges.add(e1)
                    hl_edges.append([person, friend])
                if e2 not in seen_edges:
                    seen_edges.add(e2)
                    hl_edges.append([friend, mutual])

    return jsonify({
        "person": person,
        "recommendations": recs,
        "highlight_edges": hl_edges
    })


if __name__ == '__main__':
    os.makedirs('static', exist_ok=True)
    app.run(debug=True, port=5000)