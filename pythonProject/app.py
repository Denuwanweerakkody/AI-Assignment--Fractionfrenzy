from flask import Flask, render_template
import rdflib


# Initialize Flask app
app = Flask(__name__)

# Load the RDF ontology
ontology_path = "D:/app/pythonProject/app.owl"  # Update file path
graph = rdflib.Graph()
graph.parse(ontology_path, format="xml")

# Define the namespace for easier query access
namespace = "http://www.semanticweb.org/dell/ontologies/2024/11/untitled-ontology-39"

# @app.route('/')
# def home():
#     return "Welcome to the Fraction Learning Ontology API!"

@app.route('/')
def web():
    # SPARQL query to get all questions and their correct answers for display
    query = """
    PREFIX ont: <http://www.semanticweb.org/dell/ontologies/2024/11/untitled-ontology-39#>
    SELECT ?question ?questionText ?answer ?answerValue
    WHERE {
        ?question rdf:type ont:Question . 
        ?question ont:hasQuestionText ?questionText . 
        ?question ont:hasCorrectAnswer ?answer . 
        ?answer ont:hasValue ?answerValue .
    }
    """

    # Execute the SPARQL query
    results = graph.query(query)

    questions = []
    for row in results:
        questions.append({
            "questionText": row["questionText"],
            "correctAnswer": {
                "fractionValue": float(row["answerValue"])
            }
        })

    # Render the HTML page and pass the questions data
    return render_template('index.html', questions=questions)
@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

if __name__ == '__main__':
    app.run(debug=True)
