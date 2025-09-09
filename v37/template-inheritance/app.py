from flask import Flask, render_template
"""
Template inheritance can be used when multiple templates share a common structure 
such as headers, footers, and navigation menus.
"""
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def product():
    sneakers = [
        {'name': 'Nike Air Max', 'price': 120},
        {'name': 'Adidas Ultraboost', 'price': 140},
        {'name': 'Puma RS-X', 'price': 110},
        {'name': 'New Balance 990', 'price': 150}
    ]
    return render_template('products.html', sneakers=sneakers)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
