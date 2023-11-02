import random
import string
import matplotlib.pyplot as plt
from pde import CylindricalSymGrid, ScalarField
from bottle import Bottle, static_file, response, request



def generate_random_string(length):
  characters = string.ascii_letters + string.digit
  random_string = ''.join(random.choice(characters) for _ in range(length))
  return random_string

app = Bottle()

@app.route('/<filename>')
def serve_image(filename):
    # Replace 'path_to_your_image_folder' with the actual path to your image files
    return static_file(filename, root='static')

@app.route('/image')
def serve_image():
  # query param
  name = request.query.get('exp',"2")
  # pde diagram
  image_path = 'scalar_field_plot.png'
  try:
    grid = CylindricalSymGrid(radius=3, bounds_z=[0, 4], shape=16)
    field = ScalarField.from_expression(grid, "sqrt(z) * exp(-r**" + name + ")")
    fig, ax = plt.subplots()
    ax.imshow(field.data, origin="lower", cmap="viridis")
    ax.set_xlabel("Radius")
    ax.set_ylabel("Z")
    ax.set_title("Scalar Field")
    file_name = "tmp/hola.png"
    plt.savefig(file_name)
    #plt.show()
    image_path = file_name
    with open(image_path, 'rb') as image_file:
      response.content_type = 'image/png'
      response.set_header('Cache-Control', 'no-cache')
      return image_file.read()
  except FileNotFoundError:
    response.status = 404
    return 'Image not found'

if __name__ == '__main__':
    app.run(host='192.168.1.27', port=8080, debug=True)


'''
grid = CylindricalSymGrid(radius=3, bounds_z=[0, 4], shape=16)
field = ScalarField.from_expression(grid, "sqrt(z) * exp(-r**3)")
# Plot the field
fig, ax = plt.subplots()
ax.imshow(field.data, origin="lower", cmap="viridis")

# Add labels and title as needed
ax.set_xlabel("Radius")
ax.set_ylabel("Z")
ax.set_title("Scalar Field")

# Save the plot to a file (e.g., PNG)
plt.savefig("scalar_field_plot.png")

# Show the plot (optional)
#plt.show()
'''