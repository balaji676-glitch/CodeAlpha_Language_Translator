from flask import Flask, request, render_template_string
from deep_translator import GoogleTranslator

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Language Translator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg,#667eea,#764ba2);
            color: white;
            text-align: center;
            padding-top: 60px;
        }

        textarea {
            width: 320px;
            height: 100px;
            border-radius: 8px;
            border: none;
            padding: 10px;
        }

        select, button {
            padding: 8px;
            margin-top: 10px;
        }

        button {
            cursor: pointer;
        }

        .result {
            margin-top: 20px;
            font-size: 18px;
            font-weight: bold;
        }
    </style>
</head>
<body>

<h1>AI Language Translator</h1>

<form method="POST">
    <textarea name="text" placeholder="Enter text here..." required></textarea><br>

    <select name="source">
        <option value="auto">Auto Detect</option>
        <option value="en">English</option>
        <option value="ta">Tamil</option>
        <option value="hi">Hindi</option>
    </select>

    <select name="target">
        <option value="en">English</option>
        <option value="ta">Tamil</option>
        <option value="hi">Hindi</option>
    </select>

    <br>
    <button type="submit">Translate</button>
</form>

<div class="result">{{ result }}</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    if request.method == "POST":
        text = request.form["text"]
        source = request.form["source"]
        target = request.form["target"]

        try:
            result = GoogleTranslator(source=source, target=target).translate(text)
        except:
            result = "Translation failed"

    return render_template_string(HTML_PAGE, result=result)


if __name__ == "__main__":
    app.run(debug=True)
